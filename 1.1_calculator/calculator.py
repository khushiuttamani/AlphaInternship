def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error" #Cannot divide by zero
    return x / y

print("Simple Calculator!")

# Main loop
while True:
    operation = input("Enter operation (+, -, *, /) or 'q' to quit: ")

    if operation.lower() == 'q': # to not continue further
        print("Goodbye!")
        break

    if operation not in ['+', '-', '*', '/']: # if other operations are used make it invalid
        print("Invalid operation. Please choose +, -, *, /.")
        continue

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid input. Please enter numbers only.") # if not a number, it will be invalid
        continue

    if operation == '+':
        result = add(num1, num2)
    elif operation == '-':
        result = subtract(num1, num2)
    elif operation == '*':
        result = multiply(num1, num2)
    elif operation == '/':
        result = divide(num1, num2)

    print("Result:", result) #result
    print("-" * 30)  # print vertical lines