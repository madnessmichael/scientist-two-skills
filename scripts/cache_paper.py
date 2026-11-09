#!/usr/bin/env python3
"""Cache pinned ScientistTwo sources and page-addressable exports. Never runs paper code."""
import argparse,datetime,hashlib,json,re,tarfile,time
from pathlib import Path
import requests
import fitz
ROOT=Path(__file__).resolve().parents[1];ID='2609.19644v1';CACHE=ROOT/'.cache';PAPER=ROOT/'paper'
SOURCES={'pdf':f'https://arxiv.org/pdf/{ID}','abstract':f'https://arxiv.org/abs/{ID}','html':f'https://arxiv.org/html/{ID}','tex_archive':f'https://arxiv.org/src/{ID}'}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write_json(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def fetch(key,url):
 suffix={'pdf':'.pdf','abstract':'.abs.html','html':'.html','tex_archive':'.tar'}[key];path=CACHE/'sources'/(ID+suffix)
 if path.exists():return path
 path.parent.mkdir(parents=True,exist_ok=True)
 r=requests.get(url,headers={'User-Agent':'ScientistTwo-Skills/0.1 (single-paper research archive)'},timeout=(20,150));r.raise_for_status()
 if key=='pdf' and not r.content.startswith(b'%PDF-'):raise ValueError('Source is not a PDF')
 tmp=path.with_suffix(path.suffix+'.part');tmp.write_bytes(r.content);tmp.replace(path);time.sleep(3);return path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--reextract',action='store_true');ap.add_argument('--render-all',action='store_true');a=ap.parse_args()
 manifest_path=PAPER/'manifest.json'
 if manifest_path.exists() and not a.reextract:
  m=json.loads(manifest_path.read_text());bad=[n for n,v in m['exports'].items() if not (ROOT/n).exists() or sha(ROOT/n)!=v['sha256']]
  if bad:raise SystemExit('Cached exports changed; inspect or re-extract locally: '+', '.join(bad))
  print(json.dumps({'state':'verified_cached_exports','network_requests':0,'pages':m['pdf']['pages']}));return
 PAPER.mkdir(parents=True,exist_ok=True);sources={};errors={}
 for key,url in SOURCES.items():
  try:sources[key]=fetch(key,url)
  except Exception as exc:
   errors[key]=type(exc).__name__
   if key in ['pdf','abstract']:raise
 license_match=re.search(r'href=[\"\'](https?://creativecommons\.org/licenses/[^\"\']+)',sources['abstract'].read_text())
 if not license_match:raise RuntimeError('Paper license not identified; do not publish derived source exports yet')
 license_url=license_match.group(1)
 if '/by/4.0' not in license_url:raise RuntimeError('Review the source license before publishing text exports')
 doc=fitz.open(sources['pdf']);page_rows=[];tables=[];image_records={};fonts=[]
 render=CACHE/'rendered';render.mkdir(parents=True,exist_ok=True)
 for i,page in enumerate(doc):
  text=page.get_text('text',sort=False);layout=page.get_text('text',sort=True)
  blocks=[{'bbox':list(b[:4]),'text':b[4]} for b in page.get_text('blocks') if b[6]==0]
  page_rows.append({'page':i+1,'characters':len(text),'text':text,'text_layout':layout,'blocks':blocks,'width':page.rect.width,'height':page.rect.height,'sparse_text':len(text.strip())<100})
  for block in page.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:
     if span['size']>=12:fonts.append({'page':i+1,'size':round(span['size'],2),'text':span['text']})
  try:
   for table in page.find_tables().tables:tables.append({'page':i+1,'bbox':list(table.bbox),'cells':table.extract()})
  except Exception as exc:tables.append({'page':i+1,'error':type(exc).__name__})
  for item in page.get_images(full=True):
   xref=item[0]
   if xref not in image_records:
    image=doc.extract_image(xref);path=CACHE/'images'/f"xref-{xref:05d}.{image['ext']}";path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(image['image']);image_records[xref]={'xref':xref,'width':image['width'],'height':image['height'],'path':str(path.relative_to(ROOT)),'pages':[],'sha256':sha(path)}
   image_records[xref]['pages'].append(i+1)
  if a.render_all:
   target=render/f'page-{i+1:03d}.png'
   if not target.exists():page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(target)
 with (PAPER/'pages.jsonl').open('w') as f:
  for row in page_rows:f.write(json.dumps(row,ensure_ascii=False)+'\n')
 header='# ScientistTwo — cached PDF text\n\nJaehyun Nam, Jinsung Yoon, Yanzhou Pan, Yubo Wang, Rui Meng, Parthasarathy Ranganathan, Tomas Pfister (2026). arXiv:2609.19644v1. Source: https://arxiv.org/abs/2609.19644v1. Original paper: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes: machine extraction, whitespace/layout conversion and page headings; no authorship or endorsement claimed. Equations/tables may lose layout; use cached TeX/PDF for exact forms.\n\n'
 (PAPER/'fulltext.md').write_text(header+'\n\n'.join('## PDF page '+str(p['page'])+'\n\n'+re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', p['text']) for p in page_rows))
 write_json(PAPER/'tables.json',tables);write_json(PAPER/'structure.json',{'pdf_bookmarks':doc.get_toc(),'large_type_spans':fonts})
 write_json(CACHE/'images.json',list(image_records.values()))
 tex_files=[];environments=[]
 if 'tex_archive' in sources:
  target=CACHE/'tex';target.mkdir(parents=True,exist_ok=True)
  try:
   with tarfile.open(sources['tex_archive'],'r:*') as archive:
    for member in archive.getmembers():
     relative=Path(member.name)
     if member.isfile() and not relative.is_absolute() and '..' not in relative.parts:
      fp=target/relative;fp.parent.mkdir(parents=True,exist_ok=True);fp.write_bytes(archive.extractfile(member).read())
    for path in sorted(target.rglob('*')):
     if path.is_file() and path.suffix.lower() in ['.tex','.bib','.bbl','.sty','.cls','.txt','.md']:
      rel=path.relative_to(target);dest=PAPER/'source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(path.read_bytes());tex_files.append(str(dest.relative_to(ROOT)))
      if path.suffix=='.tex':
       text=path.read_text(errors='replace')
       for kind in ['figure','table','algorithm','equation','align','lstlisting','tcolorbox']:
        pattern=r'\\begin\{'+kind+r'\*?\}.*?\\end\{'+kind+r'\*?\}'
        for n,m in enumerate(re.finditer(pattern,text,re.S),1):environments.append({'type':kind,'source':str(dest.relative_to(ROOT)),'ordinal':n,'latex':m.group()})
  except tarfile.TarError:errors['tex_archive_extraction']='not_a_supported_tar_archive'
 write_json(PAPER/'source_environments.json',environments)
 exports=[p for p in PAPER.rglob('*') if p.is_file() and p.name not in ['manifest.json','README.md','ATTRIBUTION.md','review-notes.md']]
 manifest={'paper_id':ID,'title':'ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI','authors':['Jaehyun Nam','Jinsung Yoon','Yanzhou Pan','Yubo Wang','Rui Meng','Parthasarathy Ranganathan','Tomas Pfister'],'fetched_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'license':license_url,'extractor':'cache_paper.py/0.1','pymupdf_version':fitz.VersionBind,'sources':{k:{'url':SOURCES[k],'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for k,p in sources.items()},'source_errors':errors,'pdf':{'pages':len(doc),'text_pages_exported':len(page_rows),'characters':sum(p['characters'] for p in page_rows),'sparse_pages':[p['page'] for p in page_rows if p['sparse_text']]},'tables_detected':len([t for t in tables if 'cells' in t]),'embedded_images':len(image_records),'tex_files':tex_files,'source_environments':len(environments),'rendered_pages':len(list(render.glob('*.png'))),'exports':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in exports},'limitations':['PDF text is not a lossless representation of formulas, charts or table structure.','Exact TeX is retained where source is available; PDF/page renders preserve visual information.','Embedded images are cached without claiming OCR or manual transcription of every label.']}
 write_json(manifest_path,manifest)
 print(json.dumps({k:manifest[k] for k in ['paper_id','pdf','tables_detected','embedded_images','source_environments','rendered_pages','source_errors']},ensure_ascii=False))
if __name__=='__main__':main()
