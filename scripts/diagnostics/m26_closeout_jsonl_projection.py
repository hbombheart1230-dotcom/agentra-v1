from typing import Any,Dict,List
from pathlib import Path
def _write_jsonl(path:Path,rows:List[Dict[str,Any]],*,facade:Any)->None:
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open("w",encoding="utf-8",newline="\n") as f:
  for row in rows:f.write(facade.json.dumps(row,ensure_ascii=False)+"\n")
