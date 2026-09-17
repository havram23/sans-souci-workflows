import io
import json
from pathlib import Path
import tempfile
import unittest
from urllib.error import HTTPError
from clients.monitor_event import NoRedirect, flush_queue, payload_for, queue_event, send_event

URL = 'http://127.0.0.1:8771/ingest/wf_synthetic'
TOKEN = 'wm_synthetic_test_only'


class MonitorClientTests(unittest.TestCase):
    def test_retry_reuses_exact_payload_and_redirects_are_blocked(self):
        class Opener:
            requests = []
            def open(self, request, timeout):
                self.requests.append(request)
                if len(self.requests) == 1: raise HTTPError(URL,503,'Unavailable',{},None)
                return io.BytesIO(b'{"accepted":true,"duplicate":true}')
        opener = Opener()
        self.assertTrue(send_event(URL,TOKEN,opener=opener,sleep=lambda _:None)['accepted'])
        self.assertEqual(opener.requests[0].data,opener.requests[1].data)
        self.assertIsNone(NoRedirect().redirect_request(None,None,None,None,None,None))

    def test_bad_endpoints_and_non_retryable_auth_errors(self):
        for url in ('http://example.invalid/ingest/wf_test','https:///ingest/wf_test','https://u:p@example.invalid/ingest/wf_test',URL+'?key=x',URL+'/extra'):
            with self.assertRaises(ValueError): send_event(url,TOKEN)
        class Denied:
            count = 0
            def open(self,request,timeout):
                self.count += 1
                raise HTTPError(URL,401,'Denied',{},None)
        opener = Denied()
        with self.assertRaises(RuntimeError): send_event(URL,TOKEN,opener=opener)
        self.assertEqual(opener.count,1)

    def test_200_response_without_acceptance_is_not_success(self):
        class Rejected:
            def open(self,request,timeout):return io.BytesIO(b'{"accepted":false}')
        with self.assertRaises(RuntimeError):send_event(URL,TOKEN,opener=Rejected())

    def test_disk_queue_preserves_id_time_and_keeps_failed_events(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            event_id=queue_event(folder,'failure',code='SYNTHETIC_FAILURE')
            raw=(folder/(event_id+'.json')).read_bytes()
            self.assertNotIn(TOKEN.encode(),raw)
            calls=[]
            def fail(url,token,**payload):
                calls.append(payload)
                raise RuntimeError('offline')
            self.assertEqual(flush_queue(folder,URL,TOKEN,sender=fail),{'sent':0,'failed':1,'pending':1})
            self.assertEqual((folder/(event_id+'.json')).read_bytes(),raw)
            def succeed(url,token,**payload):
                calls.append(payload)
                return {'accepted':True,'duplicate':True}
            self.assertEqual(flush_queue(folder,URL,TOKEN,sender=succeed),{'sent':1,'failed':0,'pending':0})
            self.assertEqual(calls[0],calls[1])

    def test_queue_does_not_overwrite_or_send_unexpected_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory); event_id=queue_event(folder)
            with self.assertRaises(FileExistsError): queue_event(folder,event_id=event_id)
            path=folder/(event_id+'.json');payload=json.loads(path.read_text());payload['secret']='never send';path.write_text(json.dumps(payload))
            def forbidden(*args,**kwargs): self.fail('Malformed event must not be sent')
            result=flush_queue(folder,URL,TOKEN,sender=forbidden)
            self.assertEqual(result['failed'],1);self.assertTrue(path.exists())

    def test_queue_keeps_concurrently_changed_file_after_ack(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);event_id=queue_event(folder)
            path=folder/(event_id+'.json')
            def change(*args,**kwargs):path.write_text('{}');return {'accepted':True}
            self.assertEqual(flush_queue(folder,URL,TOKEN,sender=change)['failed'],1)
            self.assertTrue(path.exists())

    def test_payload_rejects_unbounded_codes_and_missing_timezone(self):
        for kwargs in ({'code':'private text'}, {'status':'unknown'}, {'occurred_at':'2026-01-01T00:00:00'}, {'event_id':'bad'}):
            with self.assertRaises(ValueError):payload_for(**kwargs)


if __name__=='__main__':unittest.main()
