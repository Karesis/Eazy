# Generated Python code from Eazy language (Claw compiler V1)
# Source file: my_program.ez

# Generated block functions:
def helper():
    print(" This is the helper block ")
    return

def main():
    print(" Starting main ")
    helper()
    print(" Returned from helper ")
    result = 10 * 2
    print(result)
    return

def another_block():
    print(" This won ' t run unless called ")
    return

# Entry point:
main()
