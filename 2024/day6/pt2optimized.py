import argparse
import time
from multiprocessing import Pool
from array import array

# Essentially acts as an enum with an extremely small footprint
DIRS_Y = array('b', [-1, 0, 1, 0])
DIRS_X = array('b', [0, 1, 0, -1])
NEXT_DIR = array('b', [1, 2, 3, 0])

def pack_guard_state(y, x, dir_idx):
    # Pack state of guard position/direction into single integer
    return (y << 16) | (x << 8) | dir_idx

def check_position(puzzle, y_pos, x_pos, y_start, x_start, width, height):

    # Pre-allocate a sorted array for state management
    states = set()
    state_count = 0

    y, x = y_start, x_start
    dir_idx = 0

    max_states = width * height * 4

    while len(states) < max_states:
        state = pack_guard_state(y, x, dir_idx)

        if state in states:
            return 1
        
        states.add(state)

        next_y = y + DIRS_Y[dir_idx]
        next_x = x + DIRS_X[dir_idx]

        if next_y < 0 or next_y >= height or next_x < 0 or next_x >= width:
            return 0
        
        if puzzle[next_y][next_x] == '#' or (next_y == y_pos and next_x == x_pos):
            dir_idx = NEXT_DIR[dir_idx]
        else:
            y, x = next_y, next_x
    
    return 0
    
def process_chunk(args):
    puzzle, positions, y_start, x_start, width, height = args
    count = 0

    puzzle_array = [array('B', (ord(c) for c in row)) for row in puzzle]

    for pos_y, pos_x in positions:
        count += check_position(puzzle_array, pos_y, pos_x, y_start, x_start, width, height)
    
    return count

def find_empty_positions(puzzle):
    positions = []
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if puzzle[y][x] == '.':
                positions.append((y, x))
    return positions

def count_loop_positions(puzzle, guard_start):
    height = len(puzzle)
    width = len(puzzle[0])

    empty_positions = find_empty_positions(puzzle)

    # Parallel process for speed
    cpu_count = Pool()._processes

    chunk_size = max(1, len(empty_positions) // cpu_count)

    position_chunks = [empty_positions[i:i + chunk_size] for i in range(0, len(empty_positions), chunk_size)]

    args = [(puzzle, chunk, guard_start[0], guard_start[1], width, height) for chunk in position_chunks]

    with Pool() as pool:
        results = pool.map(process_chunk, args)
    
    return sum(results)

def main():
    start_time = time.perf_counter()
    
    # Open and read the file
    parser = argparse.ArgumentParser(description="Process file and calculate sum of absolute differences.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")
    args = parser.parse_args()

    puzzle = []
    with open(args.file_path, 'r') as file:
        for line_num, line in enumerate(file):
            puzzle.append(line.strip())

            if '^' in line:
                guard_coords = (line_num, line.index('^'))

    loop_count = count_loop_positions(puzzle, guard_coords)

    # Stop the timer after execution
    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.6f} seconds")
    print(f"Number of obstructions that could cause guard loop: {loop_count}")

if __name__ == "__main__":
    main()

    