def divide(dividend, divisor):
    try:
        result = dividend / 0
        return result
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")