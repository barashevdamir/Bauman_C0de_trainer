function binomialTheorem(a, b, n) {
  if (n === 0) {
    return '1';
  }

  const coefficients = [];

  for (let k = 0; k <= n; k++) {
    const coefficient = binomialCoefficient(n, k);
    const term = `${coefficient} * ${a}^${n - k} * ${b}^${k}`;
    coefficients.push(term);
  }

  return coefficients.join(' + ');
}

function binomialCoefficient(n, k) {
  if (k === 0 || k === n) {
    return 1;
  }

  let coefficient = 1;
  for (let i = 1; i <= k; i++) {
    coefficient *= (n - i + 1) / i;
  }

  return coefficient;
}