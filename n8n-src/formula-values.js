const risky = value => /^[\t\r\n]/.test(value) || /^[\s]*[=+\-@]/u.test(value);
return $input.all().map((item, index) => ({
  json: Object.fromEntries(Object.entries(item.json).map(([key, value]) => [key, typeof value === 'string' && risky(value) ? "'" + value : value])),
  pairedItem: {item: index},
}));
