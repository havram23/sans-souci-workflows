const required = ['id', 'company'];
return $input.all().map((item, index) => {
  const missing = required.filter(field => typeof item.json[field] !== 'string' || !item.json[field].trim());
  return {json: {...item.json, validation: {valid: missing.length === 0, missing_fields: missing}}, pairedItem: {item: index}};
});
