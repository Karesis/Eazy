	.text
	.file	"test.temp.ll"
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$5, 4(%rsp)
	movl	$.str.int_format, %edi
	movl	$100, %esi
	xorl	%eax, %eax
	callq	printf@PLT
	movl	$.str.int_format, %edi
	movl	$300, %esi                      # imm = 0x12C
	xorl	%eax, %eax
	callq	printf@PLT
	movl	$.str.int_format, %edi
	movl	$400, %esi                      # imm = 0x190
	xorl	%eax, %eax
	callq	printf@PLT
	movl	$.str.int_format, %edi
	movl	$600, %esi                      # imm = 0x258
	xorl	%eax, %eax
	callq	printf@PLT
	movl	$.str.int_format, %edi
	movl	$700, %esi                      # imm = 0x2BC
	xorl	%eax, %eax
	callq	printf@PLT
	xorl	%eax, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	.str.int_format,@object         # @.str.int_format
	.section	.rodata,"a",@progbits
.str.int_format:
	.asciz	"%d\n"
	.size	.str.int_format, 4

	.section	".note.GNU-stack","",@progbits
