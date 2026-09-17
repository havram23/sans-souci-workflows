const allowed = ['id', 'company'];
return $input.all().map((item, index) => ({
  json: Object.fromEntries(allowed.filter(field => Object.hasOwn(item.json, field)).map(field => [field, item.json[field]])),
  pairedItem: {item: index},
}));
