import argparse
import time

def parse_disk_map(disk_map):
    blocks = []
    file_id = 0

    # Remove any whitespace and newlines
    disk_map = disk_map.strip()

    for i in range(0, len(disk_map), 2):
        file_length = int(disk_map[i])

        # Add file blocks
        for _ in range(file_length):
            blocks.append(file_id)

        # Add free space if there is a next number
        if i + 1 < len(disk_map):
            free_space_length = int(disk_map[i + 1])
            for _ in range(free_space_length):
                blocks.append('.')

        file_id += 1

    return blocks

def get_file_positions(blocks):
    file_positions = {}
    current_file = None
    start_pos = None
    
    # Get position range for each file block
    for pos, block in enumerate(blocks):
        if block != '.':
            if block != current_file:
                if current_file is not None:
                    file_positions[current_file] = (start_pos, pos - start_pos)
                current_file = block
                start_pos = pos
        elif current_file is not None:
            file_positions[current_file] = (start_pos, pos - start_pos)
            current_file = None

    # Handle the last file if it extends to the end
    if current_file is not None:
        file_positions[current_file] = (start_pos, len(blocks) - start_pos)

    return file_positions

def find_leftmost_space(blocks, required_length, start_pos=0):
    current_length = 0
    start_of_space = None

    # Get furthest left position with enough empty spaces
    for pos in range(start_pos, len(blocks)):
        if blocks[pos] == '.':
            if start_of_space is None:
                start_of_space = pos
            current_length += 1
            if current_length >= required_length:
                return start_of_space
        else:
            current_length = 0
            start_of_space = None

    return None

def compact_disk(blocks):
    result = blocks.copy()
    file_positions = get_file_positions(result)

    # Process files in decreasing order of file ID
    for file_id in sorted(file_positions.keys(), reverse=True):
        start_pos, length = file_positions[file_id]

        new_pos = find_leftmost_space(result, length)

        if new_pos is not None and new_pos < start_pos:
            # Copy the file to new position
            file_blocks = result[start_pos:start_pos + length]
            result[new_pos:new_pos + length] = file_blocks
            result[start_pos:start_pos + length] = ['.' for _ in range(length)]

    return result

def calculate_checksum(blocks):
    checksum = 0
    for pos, block in enumerate(blocks):
        if block != '.':
            checksum += pos * block
    return checksum

def main():
    start_time = time.perf_counter()

    parser = argparse.ArgumentParser(description="Process disk map and calculate checksum.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")

    args = parser.parse_args()

    with open(args.file_path, 'r') as file:
        disk_map = file.read().strip()

    initial_blocks = parse_disk_map(disk_map)
    compacted_blocks = compact_disk(initial_blocks)
    checksum = calculate_checksum(compacted_blocks)

    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.6f} seconds")
    print(f"Final checksum: {checksum}")

if __name__ == "__main__":
    main()