import argparse

def count_valid_lists(rules, page_sequences):

    valid_count = 0

    valid_sequences = []
    for sequence in page_sequences:
        # Check if sequence satisfies rule conditions
        valid = True
        for before, after in rules:
            try:
                pos_before = sequence.index(before)
                pos_after = sequence.index(after)

                if pos_before >= pos_after:
                    valid = False
                    break

            except ValueError:
                # If either number isnt in sequence it is ignored
                continue
        if valid:
            valid_sequences.append(sequence)
            valid_count += 1
    
    return valid_sequences

def sum_midpoints(sequences):
    total = 0

    for sequence in sequences:
        length = len(sequence)
        if length == 0:
            continue

        if length % 2 == 1:
            mid = sequence[length // 2]
        else:
            print('We shouldnt get even numbers right???')

        total += mid
    return total

def get_rule_and_page_lists(file_content):
    rule_lines = []
    page_lines = []
    
    # Start with rule-set (delimited with '|')
    current_delimiter = '|'

    # Process lines
    for line in file_content.splitlines():
        # Skip empty lines and use them as a section delimiter
        if not line.strip():
            current_delimiter = ',' 
            continue
        
        # Parse numbers based on the current delimiter
        nums = line.split(current_delimiter)
         # For rules, split on the '|' symbol
        if current_delimiter == '|':
            before, after = map(int, nums)
            rule_lines.append((before, after))  # Store the rule as a tuple
        else:
            # For page sequences, split by commas and store them as lists of integers
            page_lines.append(list(map(int, nums)))
    
    return rule_lines, page_lines


def main():
    parser = argparse.ArgumentParser(description="Process file and calculate sum of absolute differences.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")
    
    args = parser.parse_args()

    # Open and read the file
    with open(args.file_path, 'r') as file:
        content = file.read()
        rules, page_lists = get_rule_and_page_lists(content)
    
    valid_seqs = count_valid_lists(rules, page_lists)
    sum_of_mids = sum_midpoints(valid_seqs)
    print(f"Total sum of valid sequence midpoints: {sum_of_mids}")

if __name__ == "__main__":
    main()