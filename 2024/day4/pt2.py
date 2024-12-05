import argparse 

def valid_x_mas(puzzle, row, col):
    rows = len(puzzle)
    cols = len(puzzle[0]) if rows > 0 else 0

    if row <= 0 or row >= rows - 1 or col <= 0 or col >= cols - 1:
        return False
    
    top_left = puzzle[row - 1][col - 1]
    bottom_right = puzzle[row + 1][col + 1]

    top_right = puzzle[row - 1][col + 1]
    bottom_left = puzzle[row + 1][col - 1]

    if {top_left, bottom_right} == {'M', 'S'} and {top_right, bottom_left} == {'M', 'S'}:
        return True
    
    return False

def count_occurrences(puzzle):
    word_count = 0
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == 'A':
                if valid_x_mas(puzzle, row, col):
                    word_count += 1
    return word_count


def main():
    parser = argparse.ArgumentParser(description="Count the total number of X'ed MAS's.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")
    
    args = parser.parse_args()

    # Open and read the file
    with open(args.file_path, 'r') as file:
        puzzle = [line.strip() for line in file]

    print(puzzle)

    occ = count_occurrences(puzzle)
    
    print(f"Number of X'ed MAS's: {occ}")

if __name__ == "__main__":
    main()