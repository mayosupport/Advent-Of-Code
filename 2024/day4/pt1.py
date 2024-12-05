import argparse

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1),  # vertical and horizontal 
                (-1, -1), (-1, 1), (1, -1), (1, 1)]    # diagonals

def search_in_direction(puzzle, dirx, diry, word, col, row):
    word_len = len(word)

    for x in range(word_len):
        new_i, new_j = row + x * dirx, col + x * diry
        # Check if we're going out of bounds or if the character doesn't match
        if not (0 <= new_i < len(puzzle) and 0 <= new_j < len(puzzle[0])):
            return False
        if puzzle[new_i][new_j] != word[x]:
            return False
    return True

def count_occurrences(word, puzzle):
    word_count = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            for dir_x, dir_y in DIRECTIONS:
                if search_in_direction(puzzle, dir_x, dir_y, word, i, j):
                    word_count += 1

    return word_count

def main():
    parser = argparse.ArgumentParser(description="Process file and calculate sum of absolute differences.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")
    
    args = parser.parse_args()

    # Open and read the file
    with open(args.file_path, 'r') as file:
        puzzle = [line.strip() for line in file]

    print(puzzle)

    occ = count_occurrences('XMAS', puzzle)
    
    print(f'TOTAL OCCURENCES: {occ}')

    #print(f"Total sum of absolute differences: {total_sum}")

if __name__ == "__main__":
    main()