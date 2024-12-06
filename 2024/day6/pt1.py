import argparse
import time

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def predict_path(puzzle, guard_start):
    def in_bounds(line, char):
        return 0 <= line < len(puzzle) and 0 <= char < len(puzzle[0])
    
    points_visited = set()

    curr_line, curr_char = guard_start
    curr_direction_idx = 0

    max_iterations = len(puzzle) * len(puzzle[0]) * 4
    iterations = 0

    while in_bounds(curr_line, curr_char):
        points_visited.add((curr_line, curr_char))

        next_line = curr_line + DIRECTIONS[curr_direction_idx][0]
        next_char = curr_char + DIRECTIONS[curr_direction_idx][1]

        iterations += 1
        if iterations > max_iterations:
            break

        if not in_bounds(next_line, next_char) or puzzle[next_line][next_char] == '#':
            curr_direction_idx = (curr_direction_idx + 1 ) % 4
        else:
            curr_line, curr_char = next_line, next_char

        if not in_bounds(next_line, next_char):
            break
    
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

    print(f"Total distinct points touched by guard: {len(predicted_path)}")

    # Stop the timer after execution
    end_time = time.perf_counter()

    # Calculate elapsed time in seconds
    elapsed_time_sec = end_time - start_time
    print(f"Execution time: {elapsed_time_sec:.6f} seconds")

if __name__ == "__main__":
    main()