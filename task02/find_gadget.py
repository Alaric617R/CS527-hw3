from pwn import *

elf = ELF('./innocentflesh')
rop = ROP(elf)

print("pop rdi:", hex(rop.find_gadget(['pop rdi', 'ret']).address))
print("pop rsi:", hex(rop.find_gadget(['pop rsi', 'ret']).address))
print("pop rax:", hex(rop.find_gadget(['pop rax', 'ret']).address))
print('pop rdx, pop rbx, ret:', hex(rop.find_gadget(['pop rdx', 'pop rbx', 'ret']).address))
print("syscall:", hex(rop.find_gadget(['syscall', 'ret']).address))
