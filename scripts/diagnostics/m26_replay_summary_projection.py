from typing import Dict,List
def _num_summary(values: List[float]) -> Dict[str,float]:
 vals=sorted(float(v) for v in values if float(v)>=0.0)
 if not vals:return {"count":0.0,"avg":0.0,"p50":0.0,"p95":0.0,"max":0.0}
 n=len(vals)
 def pct(p:float)->float:
  if n==1:return float(vals[0])
  idx=int(round((n-1)*p));idx=max(0,min(n-1,idx));return float(vals[idx])
 return {"count":float(n),"avg":float(sum(vals)/n),"p50":pct(.50),"p95":pct(.95),"max":float(vals[-1])}
