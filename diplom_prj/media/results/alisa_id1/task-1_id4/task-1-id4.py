def divide(dividend, divisor):
    try:
        result = dividend / divisor -1
        return result
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")