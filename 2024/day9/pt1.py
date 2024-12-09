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

def compact_disk(blocks):
    result = blocks.copy()
    
    # Iterate through the blocks from right to left
    right_idx = len(blocks) - 1
    while right_idx >= 0:
        # Skip free space at the end
        while right_idx >= 0 and result[right_idx] == '.':
            right_idx -= 1
            
        if right_idx < 0:
            break
            
        # Find leftmost free space
        left_idx = 0
        while left_idx < right_idx and result[left_idx] != '.':
            left_idx += 1
            
        if left_idx >= right_idx:
            break
            
        # Move the file block
        result[left_idx] = result[right_idx]
        result[right_idx] = '.'
        right_idx -= 1
        
    return result

def calculate_checksum(blocks):
    # Add up all ID * pos
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

    # Read input file
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
