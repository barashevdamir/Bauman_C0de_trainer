// Функция для тестирования чисел Фибоначчи
void testFibonacci() {
    assert(fibonacci(0) == 0);
    assert(fibonacci(1) == 1);
    assert(fibonacci(2) == 1);
    assert(fibonacci(3) == 2);
    assert(fibonacci(4) == 3);
    assert(fibonacci(5) == 5);
    assert(fibonacci(6) == 8);
    assert(fibonacci(7) == 13);
    std::cout << "All Fibonacci tests passed.\n";
}

// Тестовый код для проверки корректности функции вычисления чисел Фибоначчи
int main() {
    testFibonacci();
    return 0;
}
