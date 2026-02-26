I noticed that from the decompiler output, the program locate a RWX memory region for doing the JIT technique. This portion of the program:
```
  local_48[0] = 0x48;
  local_48[1] = 0x89;
  local_48[2] = 4;
  local_48[3] = 0x25;
  local_48[4] = 0xf0;
  local_48[5] = 0xf;
  local_48[6] = 0x20;
  local_48[7] = 0;
  local_48[8] = 0xc3;
  local_48[9] = 0x90;
  local_48[10] = 0x48;
  local_48[0xb] = 0x31;
  local_48[0xc] = 0xc0;
  local_48[0xd] = 0x48;
  local_48[0xe] = 199;
  local_48[0xf] = 0xc1;
  local_48[0x10] = 0;
  local_48[0x11] = 0;
  local_48[0x12] = 0x20;
  local_48[0x13] = 0;
  local_48[0x14] = 0xff;
  local_48[0x15] = 0xe1;
  lVar4 = 0;
  do {
    lVar1 = lVar4 + 1;
    *(undefined1 *)(lVar4 + 0x200f00) = local_48[lVar4];
    lVar4 = lVar1;
  } while (lVar1 != 0x16);
```
This is writing the assembly for:
```
mov [0x200ff0], rax
ret
nop
xor rax, rax
mov rcx, 0x200000
jmp rcx
```
And the next for loop is effectively writing the following assembly to memory:
```
mov rbx, num1
add rax, rbx
mov rbx, num2
add rax, rbx
mov rbx, num3
add rax, rbx
```
which the program then jumps to that portion of executable memory by '(*(code *)0x200f0a)();'
I therefore noticed that it is possible to overwrite the function pointer at 0x200f0a, because the program allows a maximum of 297 numbers. But each iteration the program writes 13 bytes of assembly, 296*13=3848=0xf08, which means the 297th iteration, the 8 bytes of user input number start exactly at 0x200f0a. Hence, I am able to overwrite the function pointer to jump to my injected code. Since I'm only able to write 8 bytes at each iteration, I used JMP chaining, in which I used a relative jump "jmp +5"(\xeb\x05) to jump to the next 8-byte payload. This is helpful also to skip the adds which are modifying register values. 
Another challenge is the program is compiled with PIE, so it's not possible to hardcode the string '/bin/sh' to a fixed memory address. So I used a 'call/pop' trick 
```
0: call $+5 /* lands exactly to the next instruction */
5: pop rdi
```
'call' will push the address of next instruction onto the stack, and then we pop the value from the stack and store it into %rdi. Therefore, I have the dynamic address and the static offset is known. Hence, I point %rdi to the string '/bin/sh' successfully.
I therefore called "setreuid()" and "execve()" by this chaining technique and got the flag.