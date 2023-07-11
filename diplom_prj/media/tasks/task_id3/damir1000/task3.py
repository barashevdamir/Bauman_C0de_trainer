def factorial(n):
    if n == 0:
        return 1
    elif n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    else:
        return n