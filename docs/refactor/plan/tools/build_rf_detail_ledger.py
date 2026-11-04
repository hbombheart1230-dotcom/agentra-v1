#!/usr/bin/env python3
"""Regenerate evidence-first RF detail CSV from a local checkout of integration/p1.5.
Never changes RF contracts or claims tests passed. Run after git fetch.
"""
import csv, pathlib, re, subprocess, collections
ROOT=pathlib.Path(__file__).resolve().parents[3]
DETAILS=ROOT/'docs/refactor/plan/rf_details'
QUEUE=ROOT/'docs/refactor/plan/queue'
OUT=ROOT/'docs/refactor/plan/reports'
HEADERS=['RF 번호','작업 항목','구현 상태','독립 검증','통합·런 검증','남은 작업','차단 원인','담당','증거 SHA·링크','문서상 큐','증거 수준']
def git(*args):
    return subprocess.run(['git',*args],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
def main():
    if git('branch','--show-current')!='integration/p1.5':
        raise SystemExit('STOP: checkout integration/p1.5 first')
    sha=git('rev-parse','HEAD')
    OUT.mkdir(parents=True,exist_ok=True)
    stages=collections.defaultdict(list)
    for f in QUEUE.rglob('RF-*.md'):
        m=re.fullmatch(r'RF-(\d{3})\.md',f.name)
        if m: stages['RF-'+m.group(1)].append(str(f.relative_to(ROOT)))
    rows=[]; seen=set()
    for f in sorted(DETAILS.glob('RF-*_IMPLEMENTATION.md')):
        m=re.fullmatch(r'RF-(\d{3})_IMPLEMENTATION\.md',f.name)
        if not m: continue
        rf='RF-'+m.group(1); content=f.read_text(encoding='utf-8')
        stage='; '.join(stages.get(rf,[])) or '큐 미확인'
        # Each original SOURCE::function is an item; avoid historical duplicates.
        entries=[]
        for line in content.splitlines():
            if not line.startswith('|'): continue
            cells=[x.strip() for x in line.strip('|').split('|')]
            if len(cells)<3 or cells[0].startswith(('---','원본 함수','SOURCE_PATH')):continue
            source=cells[0].strip('\\\x60 ')
            target=cells[2].strip('\\\x60 ') if len(cells)>2 else ''
            if '::' in source and ('MOVE' in ' '.join(cells) or 'KEEP' in ' '.join(cells)):
                entries.append((source,target,'MOVE' if 'MOVE' in ' '.join(cells) else 'KEEP'))
        # Include file-level KEEP/MOVE items, but don't double count a file with function items.
        for line in content.splitlines():
            if not line.startswith('|'):continue
            cells=[x.strip() for x in line.strip('|').split('|')]
            if len(cells)<4 or not cells[0].startswith('\\x60'):continue
            source=cells[0].strip('\\x60 ')
            if '::' in source or not source.endswith('.py'):continue
            if any(source in x[0] for x in entries):continue
            entries.append((source,cells[1].strip('\\x60 '),'FILE_REVIEW'))
        for source,target,kind in entries:
            key=(rf,source,target)
            if key in seen:continue
            seen.add(key)
            rows.append([rf,source+' → '+target if target else source,'미확인','미확인','미확인',
                '실제 코드·테스트·통합 증거 대조 필요','', '미확인',
                'https://github.com/hbombheart1230-dotcom/agentra/blob/'+sha+'/'+str(f.relative_to(ROOT)),
                stage,'상세설계 항목; 실행 증거 미대조'])
    with (OUT/'RF_DETAIL_LEDGER.csv').open('w',encoding='utf-8-sig',newline='') as h:
        w=csv.writer(h);w.writerow(HEADERS);w.writerows(rows)
    by=collections.Counter(r[0] for r in rows)
    with (OUT/'RF_SUMMARY.csv').open('w',encoding='utf-8-sig',newline='') as h:
        w=csv.writer(h);w.writerow(['RF 번호','전체 항목(추출)','완료(검증)','진행','미착수','차단','미확인','물리 큐'])
        for i in range(1,94):
            rf=f'RF-{i:03d}'; n=by[rf]
            w.writerow([rf,n,'','','','',n,'; '.join(stages.get(rf,[])) or '미확인'])
    print('HEAD',sha,'RF_DETAILS',len(by),'ITEMS',len(rows),'QUEUE_RF',len(stages))
    print('NOTE: all extracted items remain unverified until evidence reconciliation.')
if __name__=='__main__':main()
