dd = 0x0f
def string_to_ascii_hex(input_string):
    """
    Converts a string into a space-separated string of hex values.
    """
    hex_list = []
    
    for char in input_string:
        # Get the integer ASCII value
        ascii_val = ord(char)
        # Convert to hex, remove '0x' prefix, and ensure 2 digits with zfill
        hex_val = hex(ascii_val)[2:].zfill(2).upper()
        hex_list.append(hex_val)
    
    # Join the list into a single string for readability
    return " ".join(hex_list)

# Implementation / Usage
if __name__ == "__main__":
    user_input = input("Enter a string: ")
    xored_input = bytes([ c if c==dd^10 or c==10 else c^dd for c in user_input.encode('utf-8')]).__str__
    result = string_to_ascii_hex(xored_input)
    
    print(f"Original: {user_input}")
    print(f"XORed: {xored_input}")
    print(f"ASCII Hex: {result}")