#!/usr/bin/env python3
"""Supplement native PDF text with cached full-page OCR; never fetches sources."""
import concurrent.futures, hashlib, json, os, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def one(path):
    dest = ROOT/'.cache/ocr'/f'{path.stem}.txt'
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(['tesseract', str(path), 'stdout', '-l', 'eng', '--psm', '3'], capture_output=True, check=True, env={**os.environ, 'OMP_THREAD_LIMIT':'1'})
        dest.write_bytes(result.stdout)
    return {'page':int(path.stem.split('-')[-1]), 'text':dest.read_text(), 'render_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def main():
    images=sorted((ROOT/'.cache/rendered').glob('page-*.png'))
    expected=json.loads((ROOT/'paper/manifest.json').read_text())['pdf']['pages']
    if len(images)!=expected: raise SystemExit('Render all cached PDF pages first; no network is used here.')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(one,images))
    target=ROOT/'paper/ocr_pages.jsonl'
    target.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    version=subprocess.check_output(['tesseract','--version'],stderr=subprocess.STDOUT,text=True).splitlines()[0]
    (ROOT/'paper/ocr_manifest.json').write_text(json.dumps({'engine':version,'language':'eng','psm':3,'render_dpi':108,'pages':len(rows),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'limitations':'Uncorrected OCR supplement. Not authoritative for numbers, formulas or table alignment; compare PDF/TeX.'},indent=2)+'\n')
    print(json.dumps({'ocr_pages':len(rows),'characters':sum(len(r['text']) for r in rows)}))
if __name__=='__main__': main()
