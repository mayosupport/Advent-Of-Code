import argparse

def get_enabled_mulstrings(string_to_tokenize):
    # Only get valid substrings (the bits after 'do()' and before 'dont()')
    return [part.split("don't()")[0] for part in string_to_tokenize.split('do()')]

def safe_int_conv(integer):
    try:
        return int(integer)
    except ValueError:
        return None

def tokenize_muls(string_to_tokenize):
    # For all muls, get the actual factors
    multiplications = []
    muls_to_tokenize = string_to_tokenize.split('mul(')
    for idx, mul in enumerate(muls_to_tokenize):
        factors = mul.split(')', 1)[0]
        nums = factors.split(',', 1)
        # Check that we have proper number of ints
        if len(nums) != 2:
            continue

        num1 = safe_int_conv(nums[0])
        num2 = safe_int_conv(nums[1])

        # Check that ints were actually ints
        if num1 is None or num2 is None:
            continue
            
        multiplications.append([num1, num2])

    return multiplications

def multiply_pairs(pairs):
    return [pair[0] * pair[1] for pair in pairs]

def main():
    parser = argparse.ArgumentParser(description="Process file and calculate sum of absolute differences.")
    parser.add_argument('file_path', type=str, help="Path to the input file.")
    
    args = parser.parse_args()

    # Open and read the file
    with open(args.file_path, 'r') as file:
        strng = file.read()
    
    # Remove invalid substrings
    do_strings = get_enabled_mulstrings(strng)
    strng = "".join(do_strings)

    # Now multiply everything
    multiplications = tokenize_muls(strng)
    products = multiply_pairs(multiplications)
    result = sum(products)

    print(f'Total sum of valid muls is {result}')

if __name__ == "__main__":
    main()