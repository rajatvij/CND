BITS 32
section .text
	global_start:
_start:
	mov ebx, 0x762510ff
	mov eax, 0
	mov eax, 4000
	push eax
	call ebx