I ran GDB on this program. Since this program is stripped, I have to find a  way to stop the execution in order to see the password stored in one of the registers. What I achieved this is by setting a watch point:
```
catch syscall write
```
Because the program will ask for user input at some point, we can pinpoint the exact location of invoking the 'putc' call. Wait until user input is prompted:
```
(gdb) c
Continuing.
AAA

Catchpoint 1 (call to syscall write), 0x0000772eecc4a907 in __GI___libc_write (fd=1, buf=0x566c5aa7a2a0, nbytes=12) at ../sysdeps/unix/sysv/linux/write.c:26
26	in ../sysdeps/unix/sysv/linux/write.c
```
Then, we do backtrace to find the location of 'main' function:
```
(gdb) bt
#0  0x0000772eecc4a907 in __GI___libc_write (fd=1, buf=0x566c5aa7a2a0, nbytes=12)
    at ../sysdeps/unix/sysv/linux/write.c:26
#1  0x0000772eecbc0eed in _IO_new_file_write (f=0x772eecd51780 <_IO_2_1_stdout_>, data=0x566c5aa7a2a0, n=12)
    at ./libio/fileops.c:1180
#2  0x0000772eecbc29e1 in new_do_write (to_do=12, data=0x566c5aa7a2a0 "Thinking...\n secret\n",
    fp=0x772eecd51780 <_IO_2_1_stdout_>) at ./libio/libioP.h:947
#3  _IO_new_do_write (to_do=12, data=0x566c5aa7a2a0 "Thinking...\n secret\n",
    fp=0x772eecd51780 <_IO_2_1_stdout_>) at ./libio/fileops.c:425
#4  _IO_new_do_write (fp=fp@entry=0x772eecd51780 <_IO_2_1_stdout_>,
    data=0x566c5aa7a2a0 "Thinking...\n secret\n", to_do=12) at ./libio/fileops.c:422
#5  0x0000772eecbc2ec3 in _IO_new_file_overflow (f=0x772eecd51780 <_IO_2_1_stdout_>, ch=10)
    at ./libio/fileops.c:783
#6  0x0000772eecbb6faa in __GI__IO_puts (str=0x566c1cc4c057 "Thinking...") at ./libio/ioputs.c:41
#7  0x0000566c1cc4a3ae in ?? ()
#8  0x0000772eecb5fd90 in __libc_start_call_main (main=main@entry=0x566c1cc4a340, argc=argc@entry=1,
    argv=argv@entry=0x7fff9f4c0b98) at ../sysdeps/nptl/libc_start_call_main.h:58
#9  0x0000772eecb5fe40 in __libc_start_main_impl (main=0x566c1cc4a340, argc=1, argv=0x7fff9f4c0b98,
    init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fff9f4c0b88)
    at ../csu/libc-start.c:392
#10 0x0000566c1cc4a4b5 in ?? ()
```
The frame above '__libc_start_call_main' is our 'main' function. We then examine the instructions at that address
```
(gdb) x/40i 0x0000566c1cc4a3ae
   0x566c1cc4a3ae:	call   0x566c1cc4a5c0
   0x566c1cc4a3b3:	mov    %rax,%rdi
   0x566c1cc4a3b6:	mov    %rax,%r12
   0x566c1cc4a3b9:	call   0x566c1cc4a220 <strlen@plt>
   0x566c1cc4a3be:	mov    %r12,%rdx
   0x566c1cc4a3c1:	mov    %r13,%rsi
   0x566c1cc4a3c4:	xor    %edi,%edi
   0x566c1cc4a3c6:	mov    %rax,%rcx
   0x566c1cc4a3c9:	call   0x566c1cc4a8a0
   0x566c1cc4a3ce:	mov    %r13,%rsi
   0x566c1cc4a3d1:	mov    %rbp,%rdi
   0x566c1cc4a3d4:	call   0x566c1cc4a580
   0x566c1cc4a3d9:	mov    %eax,%r12d
   0x566c1cc4a3dc:	test   %eax,%eax
```
According to the decompiler, the 'strlen' function is called right before the password generation function is called. So we know '0x566c1cc4a3c9' is calling the password generation function, whereas '0x566c1cc4a3d4' is calling the checking password correctness function. I therefore set a breakpoint that the password checking function and before it's called, examining the content stored in $rsi to get the actual password.
```
Breakpoint 2, 0x0000566c1cc4a3d4 in ?? ()
(gdb) x/s $rsi
0x7fff9f4c08e0:	"1683f45630f4794b3aa00f37883e77ad4453d348"
```
Then, we insert the password and get the flag.
