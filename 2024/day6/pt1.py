import argparse
import time

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def predict_path(puzzle, guard_start):
    points_visited = set()

    curr_line, curr_char = guard_start
    curr_direction_idx = 0
    while True:
        points_visited.add((curr_line, curr_char))

        ln_mov, char_mov = DIRECTIONS[curr_direction_idx]

        next_line = curr_line + ln_mov
        next_char = curr_char + char_mov

        # Check if the new position is out of bounds
        if not (0 <= next_line < len(puzzle) and 0 <= next_char < len(puzzle[0])):
            break  # Stop if the guard moves out of bounds

        next_pos = puzzle[next_line][next_char]

        if next_pos == '#':
            curr_direction_idx = (curr_direction_idx + 1) % 4
        else:
            curr_line = next_line
            curr_char = next_char
    
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
                for char_num, char in enumerate(line):
                    if char == '^':
                        guard_coords = (line_num, char_num)

    predicted_path = predict_path(puzzle, guard_coords)

    print(f"Total distinct points touched by guard: {len(predicted_path)}")

    # Stop the timer after execution
    end_time = time.perf_counter()

    # Calculate elapsed time in seconds
    elapsed_time_sec = end_time - start_time
    print(f"Execution time: {elapsed_time_sec:.6f} seconds")

if __name__ == "__main__":
    main()