"""Check the generated public release without accessing any private project."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import urlsplit, unquote
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
FORBIDDEN={'API_KEYS.md','sans.md','CHATVERLAUF.md','runtime','.env','.git','node_modules','__pycache__','paywall'}
TOKEN=re.compile(rb'(?:gh[pousr]_[A-Za-z0-9_]{24,}|github_pat_[A-Za-z0-9_]{30,}|(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}|wm_[A-Za-z0-9_-]{30,})')


def assert_public(name,body):
    parts=PurePosixPath(name).parts
    assert not any(part in FORBIDDEN or part.startswith('.env.') or part.endswith(('.sqlite3','.sqlite','.db','.pyc')) for part in parts), f'Forbidden package member: {name}'
    assert not any(part in {'.','..'} for part in parts) and not name.startswith('/') and '\\' not in name
    assert not TOKEN.search(body), f'Credential-like value in {name}'


class Page(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[];self.h1=0;self.in_title=False;self.title=''
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='h1':self.h1+=1
        if tag=='title':self.in_title=True
        for attr in ('href','src'):
            if attr in attrs:self.links.append(attrs[attr])
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
    def handle_data(self,data):
        if self.in_title:self.title+=data


def main():
    manifest=json.loads((SITE/'downloads/manifest.json').read_text(encoding='utf-8'))
    assert len(manifest)==16
    members=0
    for name,item in manifest.items():
        path=SITE/'downloads'/item['filename']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
            names=archive.namelist()
            assert len(names)==len(set(names))
            assert 'sans-souci-starters/README.md' in names and 'sans-souci-starters/LICENSE' in names
            for member in names:
                assert_public(member,archive.read(member));members+=1
    titles=set();pages=0;links=0
    for file in SITE.rglob('*.html'):
        parser=Page();parser.feed(file.read_text(encoding='utf-8'))
        assert parser.h1==1 and parser.title not in titles and len(parser.ids)==len(set(parser.ids)), str(file)
        titles.add(parser.title);pages+=1
        for href in parser.links:
            url=urlsplit(href)
            if url.scheme or url.netloc:continue
            if not url.path:
                assert not url.fragment or url.fragment in parser.ids, href
                continue
            assert url.path.startswith('/gratis-workflows/'), href
            relative=unquote(url.path.removeprefix('/gratis-workflows/'))
            target=SITE/relative
            if target.is_dir():target=target/'index.html'
            assert target.resolve().is_relative_to(SITE.resolve()) and target.is_file(), href
            if url.fragment:
                destination=Page();destination.feed(target.read_text(encoding='utf-8'))
                assert url.fragment in destination.ids, href
            links+=1
    assert pages==16
    workflows=list((ROOT/'.github/workflows').glob('*.yml'))
    assert len(workflows)>=2
    for file in workflows:
        text=file.read_text(encoding='utf-8')
        assert 'pull_request_target' not in text
        assert 'contents: read' in text and 'persist-credentials: false' in text
        for action in re.findall(r'uses:\s*([^\s#]+)',text):assert re.fullmatch(r'[^@\s]+@[0-9a-f]{40}',action), action
    report={'archives':len(manifest),'archive_members_checked':members,'html_pages':pages,'local_links_checked':links,'ci_workflows':len(workflows),'secret_scan':'no matching credentials in public packages'}
    (ROOT/'evidence').mkdir(exist_ok=True)
    (ROOT/'evidence/release-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
