import argparse
import time

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def predict_path(puzzle, guard_start):
    # Precompute height/width for efficiency
    height_bound, width_bound = len(puzzle), len(puzzle[0])

    def in_bounds(line, char):
        return 0 <= line < height_bound and 0 <= char < width_bound

    points_visited = set()
    curr_line, curr_char = guard_start
    curr_direction_idx = 0

    while True:
        points_visited.add((curr_line, curr_char))

        next_line = curr_line + DIRECTIONS[curr_direction_idx][0]
        next_char = curr_char + DIRECTIONS[curr_direction_idx][1]
        
        if not in_bounds(next_line, next_char):
            break

        if puzzle[next_line][next_char] == '#':
            # Using the bitwise AND for efficiency
            curr_direction_idx = (curr_direction_idx + 1) & 3
        else:
            curr_line, curr_char = next_line, next_char
    
    return points_visited

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

    predicted_path = predict_path(puzzle, guard_coords)

    # Stop the timer after execution
    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.6f} seconds")
    print(f"Total distinct points touched by guard: {len(predicted_path)}")

if __name__ == "__main__":
    main()