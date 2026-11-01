from pathlib import Path
from typing import Any, Dict, List

def _validate_dataset(root: Path, *, facade: Any) -> Dict[str, Any]:
    manifest_path=root/"manifest.json"; failures: List[str]=[]; missing_files: List[str]=[]; schema_version=""; dataset_id=""; manifest: Dict[str,Any]={}
    if not manifest_path.exists(): failures.append("missing:manifest.json")
    else:
        try: manifest=facade.json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as e: failures.append(f"invalid:manifest.json ({e})")
    if manifest:
        schema_version=str(manifest.get("schema_version") or ""); dataset_id=str(manifest.get("dataset_id") or "")
        if schema_version != facade.SCHEMA_VERSION: failures.append(f"invalid:schema_version (expected={facade.SCHEMA_VERSION}, got={schema_version or 'empty'})")
        if not dataset_id: failures.append("invalid:dataset_id (empty)")
        components=manifest.get("components")
        if not isinstance(components,dict): failures.append("invalid:components (must be object)"); components={}
        for comp,expected in facade.REQUIRED_COMPONENT_FILES.items():
            listed=components.get(comp)
            if not isinstance(listed,list): failures.append(f"missing_component:{comp}"); listed=[]
            listed_set={str(x).replace("\\","/") for x in listed}
            for rel in expected:
                if rel not in listed_set: failures.append(f"missing_manifest_ref:{rel}")
                if not (root/rel).exists(): missing_files.append(rel)
    else:
        for expected in facade.REQUIRED_COMPONENT_FILES.values():
            for rel in expected:
                if not (root/rel).exists(): missing_files.append(rel)
    missing_files=sorted(set(missing_files))
    out={"ok":len(failures)==0 and len(missing_files)==0,"dataset_root":str(root),"manifest_path":str(manifest_path),"schema_version":schema_version,"dataset_id":dataset_id,"component_total":len(facade.REQUIRED_COMPONENT_FILES),"required_file_total":int(sum(len(v) for v in facade.REQUIRED_COMPONENT_FILES.values())),"present_file_total":0,"missing_file_total":len(missing_files),"missing_files":missing_files,"failure_total":len(failures),"failures":failures}
    out["present_file_total"]=int(out["required_file_total"])-int(out["missing_file_total"])
    return out
