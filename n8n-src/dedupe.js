const seen = new Map();
return $input.all().map((item, index) => {
  const key = typeof item.json.id === 'string' ? item.json.id.trim().toLocaleLowerCase('en-US') : '';
  const first = key ? seen.get(key) : undefined;
  if (key && first === undefined) seen.set(key, index);
  return {json: {...item.json, duplicate: first !== undefined, first_input_index: first ?? index}, pairedItem: {item: index}};
});
