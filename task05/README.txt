In this task, I noticed that from the decompiled code that there is a check against any characters in ['b','i','n','s','h'] and '0x0f' which is a byte from the assembly of 'syscall', without which I cannot call "execve('bin/sh')". 
To deal with the string '/bin/sh', I hardcoded the NOTed version of '//bin/sh', and then NOT it back to bypass the check:
```
/* Push '//bin/sh' */
    mov rbx, 0x978cd091969dd0d0 
    not rbx
    push rbx
```
In order to make the 'syscall', I used self modifying code like the following:
```
lea r10, [rip + 7]  /* calculate the address of '0x0e'
    incb [r10]
    incb [r10+1]
    .byte 0x0e, 0x04
```
The 'incb' will increment the '0x0e' to '0x0f' and '0x04' to '0x05' which in combine is the 'syscall' we wanted, and it bypass the check perfectly. 
After bypassing the check, I crafted the payload for our buffer overflow attack. Since the program leaks the address of the buffer, I just overwrite the return address with that stack address and put the shellcode at the very beginning of the buffer. The shellcode first calls 'setreuid(task05flag,task05flag)' to escalate privilege and then do 'execve' to spawn a shell. Then I was able to get the flag.