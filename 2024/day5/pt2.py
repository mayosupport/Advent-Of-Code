import argparse

def correct_sequence(rules, sequence):
    # Needs to be some topological sort

    # Create mapping where each number maps to the number(s) that must come after it
    dependencies = {x: set() for x in sequence}
    unique_nums = set(sequence)

    # Fill the mapping
    for before, after in rules:
        if before in unique_nums and after in unique_nums:
            dependencies[before].add(after)
    
    # Count prereqs (how many nums must come before each num in the sequence)
    prereq_count = {x: 0 for x in sequence}
    for num in dependencies:
        for dependent in dependencies[num]:
            prereq_count[dependent] += 1
    
    # Start with numbers with no prereqs
    ready_now = [num for num, count in prereq_count.items() if count == 0]
    result = []

    # Process until we have no ready numbers
    while ready_now:
        current = ready_now.pop()
        result.append(current)

        # Update prereqs
        for dependent in dependencies[current]:
            prereq_count[dependent] -= 1
            # If number now has all prereqs, count it ready
            if prereq_count[dependent] == 0:
                ready_now.append(dependent)
    
    # Return empty list if a loop is found (this should not happen!)
    return result if len(result) == len(sequence) else []

def count_valid_lists(rules, page_sequences):

    valid_sequences = []
    validated_sequences = []
    for sequence in page_sequences:
        # Check if sequence satisfies rule conditions
        valid = True
        for before, after in rules:
            
            try:
                pos_before = sequence.index(before)
                pos_after = sequence.index(after)
                
                if pos_before >= pos_after:
                    valid = False

            except ValueError:
                # If either number isnt in sequence
                continue
        if valid:
            valid_sequences.append(sequence)
        else:
            corrected = correct_sequence(rules, sequence)
            if corrected:
                validated_sequences.append(corrected)
    
    return valid_sequences, validated_sequences

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
        # Skip empty lines and use them as a section delimiter
        if not line.strip():
            current_list = page_lines
            current_delimiter = ','  # Page numbers are separated by commas
            continue
        
        # Parse numbers based on the current delimiter
        nums = line.split(current_delimiter)
        if current_delimiter == '|':  # For rules, split on the '|' symbol
            before, after = map(int, nums)
            rule_lines.append((before, after))  # Store the rule as a tuple
            print(f"Rule parsed: {before} before {after}")  # Debug print
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
    
    valid_seqs, validated_seqs = count_valid_lists(rules, page_lists)
    sum_of_mids = sum_midpoints(validated_seqs)
    print(len(validated_seqs))
    print(sum_of_mids)

    print(f"Total sum of corrected sequence midpoints: {sum_of_mids}")

if __name__ == "__main__":
    main()