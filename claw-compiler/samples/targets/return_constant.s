    .text                          # Code section
    .global _start                 # Make _start visible to linker
_start:
    # Skipping: return 42
    movq $0, %rdi                  # Default exit code 0 (no explicit back)
    movq $60, %rax                 # syscall number for exit
    syscall                        # Exit the program
