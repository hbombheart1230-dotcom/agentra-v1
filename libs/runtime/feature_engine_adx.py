from typing import Any, List, Optional

def _adx(highs: List[float], lows: List[float], closes: List[float], period: int = 14, facade: Any = None) -> Optional[float]:
    p=max(2,int(period))
    if len(highs)<p+1 or len(lows)<p+1 or len(closes)<p+1: return None
    trs=[]; plus=[]; minus=[]
    for i in range(1,len(closes)):
        up=float(highs[i]-highs[i-1]); down=float(lows[i-1]-lows[i]); plus.append(up if up>down and up>0 else 0.0); minus.append(down if down>up and down>0 else 0.0); trs.append(float(max(float(highs[i]-lows[i]),abs(float(highs[i]-closes[i-1])),abs(float(lows[i]-closes[i-1])))))
    tr=sum(trs[-p:])/float(p) if trs else 0.0; pd=sum(plus[-p:])/float(p) if plus else 0.0; md=sum(minus[-p:])/float(p) if minus else 0.0
    if tr<=0: return 0.0
    pdi=pd/tr*100.0; mdi=md/tr*100.0; den=pdi+mdi
    return 0.0 if den<=0 else float(abs(pdi-mdi)/den*100.0)
