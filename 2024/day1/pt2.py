import argparse

def take_in_and_add(path):
    file = open(path, 'r')

    col1 = []
    col2 = []
    for line in file:
        values = line.strip().split()

        col1.append(int(values[0]))
        col2.append(int(values[1]))
    
    sim_scores = []
    for num in col1:
        occurences = col2.count(num)
        sim_scores.append(num * occurences)
    
    return sum(sim_scores)


def main():
    parser = argparse.ArgumentParser(description="Process file and calculate sum of absolute differences.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")
    
    args = parser.parse_args()

    total_sum = take_in_and_add(args.file_path)
    
    print(f"Total sum of sim scores: {total_sum}")

if __name__ == "__main__":
    main()