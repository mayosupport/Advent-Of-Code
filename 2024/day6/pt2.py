import argparse
import time

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def predict_loop(puzzle, obstacle_pos, guard_start):
    # Precompute height/width for efficiency
    height_bound, width_bound = len(puzzle), len(puzzle[0])

    def in_bounds(line, char):
        return 0 <= line < height_bound and 0 <= char < width_bound

    # Instead of tracking points, track point + direction. This is a very simple way to detect loops!
    states_visited = set()
    curr_line, curr_char = guard_start
    curr_direction_idx = 0

    while in_bounds(curr_line, curr_char):
        state = (curr_line, curr_char, curr_direction_idx)
        if state in states_visited:
            # This is the only time we would ever have a loop
            return True

        states_visited.add(state)
        next_line = curr_line + DIRECTIONS[curr_direction_idx][0]
        next_char = curr_char + DIRECTIONS[curr_direction_idx][1]

        if not in_bounds(next_line, next_char):
            return False

        if puzzle[next_line][next_char] == '#' or (next_line, next_char) == obstacle_pos:
            curr_direction_idx = (curr_direction_idx + 1) & 3
        else:
            curr_line, curr_char = next_line, next_char

    return False

def count_loop_positions(puzzle, guard_start):
    loop_count = 0

    for line in range(len(puzzle)):
        for char in range(len(puzzle[0])):
            # Potential spot to place obstruction
            if puzzle[line][char] == '.':
                loop_count += predict_loop(puzzle, (line, char), guard_start)
    return loop_count

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