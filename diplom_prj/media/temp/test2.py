import pytest
# from main.py import factorial
def test_factorial():
    # Testing factorial of positive numbers
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24
    assert factorial(5) == 120

    # Testing factorial of negative numbers
    with pytest.raises(ValueError):
        factorial(-1)

    # Testing factorial of non-integer inputs
    with pytest.raises(TypeError):
        factorial(2.5)
    with pytest.raises(TypeError):
        factorial("a")