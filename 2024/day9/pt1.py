import argparse
import time

def compact_disk(disk_map):
    # Convert the disk map into a list of file lengths and free space lengths
    blocks = []
    for i in range(0, len(disk_map), 2):
        file_length = int(disk_map[i])  # file block length (digit)
        try:
            free_space_length = int(disk_map[i + 1])
        except IndexError:
            free_space_length = None
        
        # Add file blocks to the list
        for _ in range(file_length):
            blocks.append(i // 2)  # Add file block with its ID (i//2 is the ID of the file)
        
        # Add free spaces to the list
        if not free_space_length:
            continue
        for _ in range(free_space_length):
            blocks.append('.')

    compact_blocks = blocks.copy()
    for i, char in enumerate(reversed(blocks)):
        if char == '.':
            continue

        replace_idx = compact_blocks.index('.')
        print(f'BLOCK AT {replace_idx} BEFORE REPLACE: {compact_blocks[replace_idx]}')
        compact_blocks[replace_idx] = char
        print(f'BLOCK AT {replace_idx} AFTER REPLACE: {compact_blocks[replace_idx]}')
        compact_blocks[-i] = '.'

        print(f'START OF LIST: {compact_blocks[0:20]}')
        print(f'END OF LIST (INDEX {-i}): {compact_blocks[i]}')
    
    return compact_blocks


def calculate_checksum(compaction):
    # Calculate checksum: position * file_id for each file block
    checksum = 0
    for pos, block in enumerate(compaction):
        if block != '.':
            checksum += pos * block  # Multiply the position with the file ID
    return checksum

def main():
    start_time = time.perf_counter()
    
    # Open and read the file
    parser = argparse.ArgumentParser(description="Process file and calculate sum of absolute differences.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")
    
    args = parser.parse_args()
    puzzle = []
    with open(args.file_path, 'r') as file:
        disk_map = file.read()

    compaction = compact_disk(disk_map)
    checksum = calculate_checksum(compaction)

    # Stop the timer after execution
    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.6f} seconds")
    print(f"Total checksum: {checksum}")

if __name__ == "__main__":
    main()