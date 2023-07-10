// Test the binomialTheorem() function
test('binomialTheorem() function should return the correct expansion', () => {
  expect(binomialTheorem('a', 'b', 0)).toBe('1');
  expect(binomialTheorem('a', 'b', 1)).toBe('1 * a^1 * b^0 + 1 * a^0 * b^1');
  expect(binomialTheorem('a', 'b', 2)).toBe('1 * a^2 * b^0 + 2 * a^1 * b^1 + 1 * a^0 * b^2');
  expect(binomialTheorem('a', 'b', 3)).toBe('1 * a^3 * b^0 + 3 * a^2 * b^1 + 3 * a^1 * b^2 + 1 * a^0 * b^3');
});

// Test the binomialCoefficient() function
test('binomialCoefficient() function should return the correct coefficient', () => {
  expect(binomialCoefficient(0, 0)).toBe(1);
  expect(binomialCoefficient(5, 0)).toBe(1);
  expect(binomialCoefficient(5, 3)).toBe(10);
  expect(binomialCoefficient(10, 5)).toBe(252);
});
