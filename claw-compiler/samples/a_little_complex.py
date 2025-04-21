# Generated Python code from Eazy language (Claw compiler V1)
# Source file: a_little_complex.ez

# Generated block functions:
def main():
    print(" Program starting in main block . ")
    num1 = 0
    num2 = 0
    sum_res = 0
    print(" Variables initialized . ")
    get_input()
    print(" Main : Returned from get_input flow . ")
    print(" Main : Placeholder values are : ")
    print(num1)
    print(num2)
    print(" Program finished in main . ")
    return

def get_input():
    print(" Entering get_input block . ")
    local_num1 = 15
    local_num2 = 27
    print(" Input received ( simulated ) : ")
    print(local_num1)
    print(local_num2)
    calculate_sum()
    print(" get_input : Returned from calculate_sum . ")
    return

def calculate_sum():
    print(" Entering calculate_sum block . ")
    calc_a = 50
    calc_b = 30
    print(" Calculating sum for : ")
    print(calc_a)
    print(calc_b)
    local_sum = calc_a + calc_b
    print_result()
    print(" calculate_sum : Returned from print_result . ")
    return

def print_result():
    print(" Entering print_result block . ")
    final_result = 80
    print(" - - - Calculation Result - - - ")
    print(final_result)
    print(" - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    return

# Entry point:
main()
