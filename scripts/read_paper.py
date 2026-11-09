#!/usr/bin/env python3
"""Read the pinned paper cache without network access or PDF extraction dependencies."""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def page_ids(spec,total):
 result=set()
 for part in spec.split(','):
  bounds=part.split('-');lo=int(bounds[0]);hi=int(bounds[-1]);result.update(range(lo,hi+1))
 if not result or min(result)<1 or max(result)>total:raise ValueError('Page selection outside cached PDF')
 return result

def main():
 a=argparse.ArgumentParser(description=__doc__);g=a.add_mutually_exclusive_group();g.add_argument('--pages');g.add_argument('--search');g.add_argument('--outline',action='store_true');g.add_argument('--stats',action='store_true');a.add_argument('--ocr',action='store_true',help='Read OCR supplement instead of native PDF text');a.add_argument('--layout',action='store_true');a.add_argument('--limit',type=int,default=8);a.add_argument('--context',type=int,default=350);args=a.parse_args()
 path=ROOT/('paper/ocr_pages.jsonl' if args.ocr else 'paper/pages.jsonl')
 if not path.exists():raise SystemExit('No cached pages: run scripts/cache_paper.py once in the prepared environment.')
 if args.outline:print((ROOT/'paper/structure.json').read_text());return
 if args.stats or not(args.pages or args.search):
  m=json.loads((ROOT/'paper/manifest.json').read_text());print(json.dumps({k:m[k] for k in ['paper_id','title','license','pdf','tables_detected','source_errors']},ensure_ascii=False,indent=2));return
 rows=[json.loads(line) for line in path.read_text().splitlines()]
 if args.pages:
  chosen=page_ids(args.pages,len(rows))
  for row in rows:
   if row['page'] in chosen:print(f"\n## PDF page {row['page']}\n\n"+row['text_layout' if args.layout and not args.ocr else 'text'])
 else:
  count=0
  for row in rows:
   text=re.sub(r'\s+',' ',row['text']);matches=list(re.finditer(re.escape(args.search),text,re.I))
   for m in matches:
    print(f"\nPDF page {row['page']}: "+text[max(0,m.start()-args.context):m.end()+args.context]);count+=1
    if count>=args.limit:return
  if not count:print('No literal match in extracted text. Check TeX or rendered pages for hyphenated/math/image text.')
if __name__=='__main__':main()
