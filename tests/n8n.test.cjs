const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const files = fs.readdirSync(path.join(root, 'n8n')).filter(x => x.endsWith('.json'));
assert.equal(files.length, 4);
for (const file of files) test(file, () => {
  const workflow = JSON.parse(fs.readFileSync(path.join(root, 'n8n', file), 'utf8'));
  assert.equal(workflow.active, false);
  assert.equal(workflow.nodes.length, 3);
  assert.equal(workflow.nodes[0].type, 'n8n-nodes-base.manualTrigger');
  assert.ok(!JSON.stringify(workflow).includes('credentials'));
  assert.ok(!workflow.nodes.some(node => /http|webhook|schedule/i.test(node.type)));
  let result = [];
  for (const node of workflow.nodes.filter(node => node.type === 'n8n-nodes-base.code')) {
    result = JSON.parse(JSON.stringify(new vm.Script(`(function(){${node.parameters.jsCode}\n})()`).runInNewContext({$input:{all:()=>result}}, {timeout:1000})));
    assert.ok(Array.isArray(result));
    assert.ok(result.every(item => item.json && typeof item.json === 'object' && !Array.isArray(item.json)));
  }
  assert.equal(result.length, 3);
  if (file.includes('required-fields')) assert.deepEqual(result.map(x=>x.json.validation.valid), [true,true,false]);
  if (file.includes('dedupe')) { assert.deepEqual(result.map(x=>x.json.duplicate), [false,true,false]); assert.equal(result[1].json.first_input_index,0); }
  if (file.includes('field-filter')) assert.ok(result.every(x=>!Object.hasOwn(x.json,'private_note') && !Object.hasOwn(x.json,'note')));
  if (file.includes('formula-values')) { assert.equal(result[2].json.note,"'=1+1"); assert.equal(result[2].json.amount,-12); }
});
