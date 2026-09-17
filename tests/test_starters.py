import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from datetime import datetime, timezone
from sans_starters import core
from sans_starters.__main__ import main

ROOT = Path(__file__).resolve().parents[1]


class StarterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def csv(self, body):
        path = self.root / 'input.csv'
        path.write_text(body, encoding='utf-8', newline='')
        return path

    def test_csv_audit_does_not_disclose_cell_contents(self):
        columns, rows = core.read_csv(self.csv('id,note\n1,=SECRET()\n2,\n'))
        result = core.audit_csv(columns, rows)
        self.assertEqual(result['fields'][1]['formula_like'], 1)
        self.assertEqual(result['fields'][1]['empty'], 1)
        self.assertNotIn('SECRET', json.dumps(result))

    def test_csv_handles_quoted_newlines_unicode_bom_and_semicolon(self):
        path = self.csv('\ufeffid;text\r\n1;"Grüße\nWien"\r\n')
        _, rows = core.read_csv(path, ';')
        self.assertEqual(rows[0]['text'], 'Grüße\nWien')

    def test_csv_rejects_duplicate_headers_short_rows_and_unclosed_quotes(self):
        for text in ('id,id\n1,2\n', 'id,name\n1\n', 'id,name\n1,"abc'):
            with self.subTest(text=text), self.assertRaises(core.InputError):
                core.read_csv(self.csv(text))

    def test_dedupe_keeps_missing_identifiers_and_first_record(self):
        columns, rows = core.read_csv(ROOT / 'examples/contacts.csv')
        result, report = core.dedupe(columns, rows, ['email'])
        self.assertEqual(len(result), 4)
        self.assertEqual(report['duplicate_row_numbers'], [4])
        self.assertEqual(result[0]['note'], 'Erstkontakt')

    def test_composite_key_dedupe_requires_all_key_parts(self):
        rows = [{'a':'1','b':''}, {'a':'1','b':''}, {'a':'2','b':'X'}, {'a':'2','b':' x '}]
        result, _ = core.dedupe(['a','b'], rows, ['a','b'])
        self.assertEqual(len(result), 3)

    def test_csv_formula_protection_includes_headers_and_whitespace(self):
        values = ['=1+1', '  +cmd', '-12', '@SUM(A1)', '\tformula', '\nformula']
        for value in values:
            with self.subTest(value=value): self.assertTrue(core.safe_cell(value).startswith("'"))
        self.assertEqual(core.safe_cell('normal'), 'normal')
        self.assertEqual(core.safe_cell("'=1"), "'=1")
        result = list(csv.reader(io.StringIO(core.csv_output(['=header'], [{'=header':'=body'}]))))
        self.assertEqual(result, [["'=header"], ["'=body"]])

    def test_mapping_uses_only_explicit_fields(self):
        columns, rows = core.map_csv(['id','private'], [{'id':'7','private':'secret'}], {'id':'identifier'})
        self.assertEqual(columns, ['identifier'])
        self.assertEqual(rows, [{'identifier':'7'}])
        for mapping in ({'missing':'id'}, {'id':'same','private':'same'}, {'id':[]}, []):
            with self.assertRaises(core.InputError): core.map_csv(['id','private'], [], mapping)

    def test_jsonl_filter_drops_unselected_fields_without_redaction_claim(self):
        result = core.filter_jsonl('{"id":1,"private":"x"}\n{"id":2}\n', ['id'])
        self.assertEqual([json.loads(line) for line in result.splitlines()], [{'id':1},{'id':2}])

    def test_json_rejects_duplicates_nonfinite_and_invalid_lines(self):
        for source in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '['):
            with self.assertRaises(core.InputError): core.strict_json(source)
        for source in ('{}\n\n{}', '[]'):
            with self.assertRaises(core.InputError): core.filter_jsonl(source, ['id'])

    def test_contract_distinguishes_boolean_integer_and_missing(self):
        result = core.check_contract([{'a':True}, {}, {'a':2}], {'a':'integer'})
        self.assertFalse(result['valid'])
        self.assertEqual([x['code'] for x in result['errors']], ['wrong_type','missing'])
        self.assertTrue(core.check_contract([{'a':10**400}], {'a':'number'})['valid'])
        for contract in ({'a':[]}, {'a':'unknown'}, {}):
            with self.assertRaises(core.InputError): core.check_contract([], contract)

    def test_utm_replaces_old_tags_preserves_query_fragment_and_encodes(self):
        rows = [{'url':'https://example.invalid/p?x=1&utm_source=old#detail','source':'news','medium':'email','campaign':'Grüße & mehr'}]
        result = core.utm_links(list(rows[0]), rows)[0]['url']
        self.assertIn('x=1&utm_source=news', result)
        self.assertNotIn('old', result)
        self.assertIn('Gr%C3%BC%C3%9Fe+%26+mehr', result)
        self.assertTrue(result.endswith('#detail'))

    def test_utm_rejects_executable_urls_credentials_and_bad_ports(self):
        for url in ('javascript:alert(1)', 'https://user:pass@example.invalid', 'https://example.invalid:bad', 'https://exam ple.invalid'):
            row = {'url':url,'source':'a','medium':'b','campaign':'c'}
            with self.subTest(url=url), self.assertRaises(core.InputError): core.utm_links(list(row), [row])

    def test_calendar_uses_utc_and_escapes_line_injection(self):
        row = {'title':'Test\nEND:VEVENT\nBEGIN:VEVENT','start':'2026-10-05T10:00:00+02:00','end':'2026-10-05T11:00:00+02:00'}
        text = core.calendar_export(list(row), [row], datetime(2026,1,1,tzinfo=timezone.utc))
        self.assertIn('DTSTART:20261005T080000Z', text)
        self.assertEqual(text.count('\r\nBEGIN:VEVENT\r\n'), 1)
        self.assertIn('SUMMARY:Test\\nEND:VEVENT\\nBEGIN:VEVENT', text)
        self.assertNotIn('ATTENDEE', text)

    def test_calendar_utf8_line_folding_is_valid_and_reversible(self):
        line = 'SUMMARY:' + 'Ö🙂' * 80
        folded = core.fold_ics(line)
        self.assertTrue(all(len(part.encode('utf-8')) <= 75 for part in folded.split('\r\n')))
        self.assertEqual(folded.replace('\r\n ', ''), line)

    def test_calendar_rejects_missing_timezone_reversed_dates_and_duplicate_ids(self):
        row = {'title':'Test','start':'2026-10-05T10:00:00','end':'2026-10-05T11:00:00'}
        with self.assertRaises(core.InputError): core.calendar_export(list(row), [row])
        row.update(start='2026-10-05T12:00:00Z', end='2026-10-05T11:00:00Z')
        with self.assertRaises(core.InputError): core.calendar_export(list(row), [row])
        row.update(start='2026-10-05T10:00:00Z')
        with self.assertRaises(core.InputError): core.calendar_export(list(row), [row, row])

    def test_manifest_detects_changed_and_missing_files(self):
        folder = self.root/'files'; folder.mkdir()
        (folder/'a.txt').write_text('one'); (folder/'b.txt').write_text('two')
        manifest = core.make_manifest(folder)
        self.assertTrue(core.verify_manifest(folder, manifest)['valid'])
        (folder/'a.txt').write_text('changed'); (folder/'b.txt').unlink()
        result = core.verify_manifest(folder, manifest)
        self.assertFalse(result['valid'])
        self.assertEqual({x['code'] for x in result['problems']}, {'changed','missing'})

    def test_manifest_rejects_traversal_absolute_duplicate_and_empty(self):
        entry = {'bytes':0,'sha256':'0'*64}
        for path in ('../private', '/etc/passwd', 'C:/secret', 'a\\b', './a', 'a//b'):
            with self.subTest(path=path), self.assertRaises(core.InputError):
                core.verify_manifest(self.root, {'format':'sans-souci-sha256-v1','files':[{**entry,'path':path}]})
        with self.assertRaises(core.InputError): core.verify_manifest(self.root, {'format':'sans-souci-sha256-v1','files':[]})
        manifest = {'format':'sans-souci-sha256-v1','files':[{**entry,'path':'A'}, {**entry,'path':'a'}]}
        with self.assertRaises(core.InputError): core.verify_manifest(self.root, manifest)

    def test_output_is_never_overwritten(self):
        output = self.root/'result.txt'
        core.write_new(output, 'first')
        with self.assertRaises(core.InputError): core.write_new(output, 'second')
        self.assertEqual(output.read_text(), 'first')

    def test_all_ten_cli_commands_with_real_fixtures(self):
        examples = ROOT/'examples'
        commands = [
            ['csv-audit',str(examples/'contacts.csv'),str(self.root/'audit.json')],
            ['csv-dedupe',str(examples/'contacts.csv'),str(self.root/'clean.csv'),'--keys','id'],
            ['csv-map',str(examples/'contacts.csv'),str(self.root/'mapped.csv'),'--mapping',str(examples/'mapping.json')],
            ['csv-safe-export',str(examples/'contacts.csv'),str(self.root/'safe.csv')],
            ['jsonl-filter',str(examples/'events.jsonl'),str(self.root/'events.jsonl'),'--fields','event_id','status'],
            ['json-contract',str(examples/'records.json'),str(self.root/'contract-report.json'),'--contract',str(examples/'contract.json')],
            ['utm-builder',str(examples/'campaigns.csv'),str(self.root/'links.csv')],
            ['calendar-export',str(examples/'appointments.csv'),str(self.root/'appointments.ics')],
            ['file-manifest',str(examples/'sample-files'),str(self.root/'manifest.json')],
            ['manifest-verify',str(examples/'sample-files'),str(self.root/'verification.json'),'--manifest',str(self.root/'manifest.json')],
        ]
        for args in commands:
            with self.subTest(command=args[0]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(args), 0)
                self.assertTrue(Path(args[2]).is_file())

    def test_cli_reports_findings_and_does_not_leak_bad_input(self):
        source = self.root/'records.json'; source.write_text('[{"private":"TOP_SECRET"}]')
        with contextlib.redirect_stdout(io.StringIO()):
            status = main(['json-contract',str(source),str(self.root/'report.json'),'--contract',str(ROOT/'examples/contract.json')])
        self.assertEqual(status, 2)
        self.assertNotIn('TOP_SECRET', (self.root/'report.json').read_text())
        source.write_text('TOP_SECRET invalid JSON')
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(main(['json-contract',str(source),str(self.root/'failed.json'),'--contract',str(ROOT/'examples/contract.json')]), 1)
        self.assertNotIn('TOP_SECRET', err.getvalue())
        self.assertFalse((self.root/'failed.json').exists())


if __name__ == '__main__': unittest.main()
