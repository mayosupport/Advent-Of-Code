import argparse
import time

# Antennas tuned to frequencies (arbitrary alphanumeric)
# We have a grid with antennas listed
# Must pair up each pair of antennas, find slope between them
# Put antinode one sloper away from each antenna.

def find_antinode_positions(pairs, grid):
    column_bounds = len(grid[0]) - 1
    row_bounds = len(grid) - 1

    antinode_positions = set()

    for char, pairs in pairs.items():
        for pair in pairs:
            pos1 = pair[0]
            pos2 = pair[1]
            
            rise = pos2[0] - pos1[0]
            run = pos2[1] - pos1[1]

            for pos in pair:
                potential_antinode_row = pos[0] + rise
                potential_antinode_col = pos[1] + run

                if not 0 <= potential_antinode_row <= row_bounds:
                    pass
                elif not 0 <= potential_antinode_col <= column_bounds:
                    pass
                elif grid[potential_antinode_row][potential_antinode_col] == char:
                    pass
                else:
                    antinode_positions.add((potential_antinode_row, potential_antinode_col))

                potential_antinode_row = pos[0] - rise
                potential_antinode_col = pos[1] - run

                if not 0 <= potential_antinode_row <= row_bounds:
                    pass
                elif not 0 <= potential_antinode_col <= column_bounds:
                    pass
                elif grid[potential_antinode_row][potential_antinode_col] == char:
                    pass
                else:
                    antinode_positions.add((potential_antinode_row, potential_antinode_col))

    return antinode_positions


def find_all_pairs(grid):
    identified_char_positions = {}
    identified_char_pairs = {}

    for idx, line in enumerate(grid):
        for jdx, char in enumerate(line):

            if char == '.':
                continue
            
            curr_position = (idx, jdx)
            if char in identified_char_positions.keys():
                for prev_position in identified_char_positions[char]:
                    identified_char_pairs[char].append((curr_position, prev_position))
                identified_char_positions[char].append(curr_position)
            else:
                identified_char_positions[char] = [(idx, jdx)]
                identified_char_pairs[char] = []

    from pprint import pprint
    pprint(identified_char_pairs)

    return identified_char_pairs


def main():
    start_time = time.perf_counter()
    
    parser = argparse.ArgumentParser(description="Process disk map and calculate checksum.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")
    
    args = parser.parse_args()
    
    # Read input file
    with open(args.file_path, 'r') as file:
        puzzle = [line.strip() for line in file.readlines()]

    pairs = find_all_pairs(puzzle)
    antinode_positions = find_antinode_positions(pairs, puzzle)

    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.6f} seconds")
    print(f"Number of unique antinode positions: {len(antinode_positions)}")

if __name__ == "__main__":
    main()