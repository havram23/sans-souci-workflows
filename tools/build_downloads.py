"""Build reproducible public ZIPs from an explicit source allowlist."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site/downloads'
TOP_FILES={'README.md','LICENSE','SECURITY.md','CONTRIBUTING.md','catalog.json','site-config.json','preview.py','.gitignore'}
DIRECTORIES={'sans_starters','clients','examples','docs','n8n','n8n-src','tools','tests','github-templates','.github'}


def source_files():
    selected=[]
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.is_symlink():continue
        relative=path.relative_to(ROOT)
        if '__pycache__' in relative.parts or path.suffix=='.pyc':continue
        if (len(relative.parts)==1 and path.name in TOP_FILES) or relative.parts[0] in DIRECTORIES or relative.parts[:2]==('site','assets'):
            selected.append(path)
    return sorted(selected)


def write_zip(path, entries):
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,body in sorted(entries.items()):
            info=zipfile.ZipInfo('sans-souci-starters/'+name,date_time=(2026,9,17,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            archive.writestr(info,body)
    return {'filename':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    catalog=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
    all_files={path.relative_to(ROOT).as_posix():path.read_bytes() for path in source_files()}
    manifest={'all-starters':write_zip(OUT/'all-starters.zip',all_files)}
    for item in catalog:
        files={'LICENSE':(ROOT/'LICENSE').read_bytes(),'README.md':(ROOT/'docs/starters'/f"{item['id']}.md").read_bytes()}
        prefixes=['sans_starters/','examples/'] if item['format']=='Python' else []
        if item['id']=='monitor-event':prefixes=['clients/']
        for name,body in all_files.items():
            if any(name.startswith(prefix) for prefix in prefixes) or name==f"n8n/{item['id']}.json":files[name]=body
        manifest[item['id']]=write_zip(OUT/f"{item['id']}.zip",files)
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'SHA256SUMS.txt').write_text(''.join(f"{entry['sha256']}  {entry['filename']}\n" for entry in manifest.values()),encoding='utf-8')
    print(json.dumps({'archives':len(manifest),'total_bytes':sum(x['bytes'] for x in manifest.values())}))


if __name__=='__main__':main()
