import argparse

def take_in_and_add(path):
    file = open(path, 'r')

    col1 = []
    col2 = []
    for line in file:
        values = line.strip().split()

        col1.append(int(values[0]))
        col2.append(int(values[1]))

    # Now we have a list of each column
    col1.sort()
    col2.sort()

    total_distance = 0
    # Pair up the numbers in sorted order
    for num1, num2 in zip(col1, col2):
        total_distance += abs(num1 - num2)

    return total_distance


def main():
    parser = argparse.ArgumentParser(description="Process file and calculate sum of absolute differences.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")
    
    args = parser.parse_args()

    total_sum = take_in_and_add(args.file_path)
    
    print(f"Total sum of absolute differences: {total_sum}")

if __name__ == "__main__":
    main()


