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
                # If either number isnt in sequence it is invalid
                valid = False
                break
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
    # Start with rule-set 
    current_list = rule_lines
    current_delimiter = '|'

    # Process lines
    for line in file_content.splitlines():
        # Skip empty lines and use them as a sectio delimiter
        if not line.strip():
            current_list = page_lines
            current_delimiter = ','
            continue
        
        # Parse numbers based on the first delimiter we find
        nums = [int(x) for x in (line.split(current_delimiter))]
        current_list.append(nums)
    
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
    print(len(valid_seqs))
    print(sum_of_mids)

    #print(f"Total sum of absolute differences: {total_sum}")

if __name__ == "__main__":
    main()