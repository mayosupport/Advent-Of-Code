import argparse

def is_valid_row(row):
    # Check if the row is increasing or decreasing and if all adjacent differences are between 1 and 3
    increasing = None

    for i in range(1, len(row)):
        diff = abs(row[i] - row[i - 1])

        # Check if the difference is between 1 and 3
        if diff < 1 or diff > 3:
            return False
        
        # Determine if the row is increasing or decreasing
        if row[i] > row[i - 1]:
            if increasing is None:
                increasing = True
            elif increasing is False:
                return False  # Bad direction
        elif row[i] < row[i - 1]:
            if increasing is None:
                increasing = False
            elif increasing is True:
                return False  # Bad direction
    
    # If we reach here, it means the row satisfies all conditions
    return True

def can_be_fixed_by_removal(row):
    # Try removing each element and check if the modified row is valid
    for i in range(len(row)):
        modified_row = row[:i] + row[i+1:]
        if is_valid_row(modified_row):
            return True
    return False

def count_valid_rows(rows):
    count = 0
    for row in rows:
        # First check if the row is valid without any removal
        if is_valid_row(row):
            count += 1
        # If not valid, check if it can be fixed by removing one element
        elif can_be_fixed_by_removal(row):
            count += 1
    return count

def main():
    parser = argparse.ArgumentParser(description="Process file and calculate valid rows with Problem Dampener.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")
    
    args = parser.parse_args()

    # Open and read the file
    with open(args.file_path, 'r') as file:
        vals = [list(map(int, line.strip().split())) for line in file]
    
    valid_rows = count_valid_rows(vals)
    
    print(f"Total valid rows: {valid_rows}")

if __name__ == "__main__":
    main()