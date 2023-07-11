assert.strictEqual(binomialTheorem('a', 'b', 0), '1');
assert.strictEqual(binomialTheorem('a', 'b', 1), '1 * a^1 * b^0 + 1 * a^0 * b^1');
assert.strictEqual(binomialTheorem('a', 'b', 2), '1 * a^2 * b^0 + 2 * a^1 * b^1 + 1 * a^0 * b^2');
assert.strictEqual(binomialTheorem('a', 'b', 3), '1 * a^3 * b^0 + 3 * a^2 * b^1 + 3 * a^1 * b^2 + 1 * a^0 * b^3');

assert.strictEqual(binomialCoefficient(0, 0), 1);
assert.strictEqual(binomialCoefficient(5, 0), 1);
assert.strictEqual(binomialCoefficient(5, 3), 10);
assert.strictEqual(binomialCoefficient(10, 5), 252);