assert.strictEqual(divide(10, 2), 5);
assert.strictEqual(divide(5, 2), 2.5);
assert.strictEqual(divide(100, 10), 10);

  // Тест для деления на ноль (ожидается генерация ошибки)
assert.throws(() => divide(10, 0), Error, "Error: Division by zero is not allowed.");
