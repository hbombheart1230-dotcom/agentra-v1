from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SCHEMA_VERSION = "m26.dataset_manifest.v1"
REQUIRED_COMPONENT_FILES: Dict[str, List[str]] = {
    "market": [
        "market/ohlcv_1m.csv",
        "market/ohlcv_5m.csv",
        "market/ohlcv_1d.csv",
        "market/corporate_actions.csv",
    ],
    "execution": [
        "execution/intents.jsonl",
        "execution/order_status.jsonl",
        "execution/fills.jsonl",
    ],
    "microstructure": [
        "microstructure/top_of_book.jsonl",
    ],
    "features": [
        "features/scanner_monitor_features.jsonl",
    ],
    "news": [
        "news/headlines.jsonl",
        "news/sentiment_by_symbol.jsonl",
        "news/sentiment_daily.jsonl",
    ],
}


def _utc_now_iso() -> str:
    from scripts.diagnostics import m26_manifest_now_projection as _b1_owner
    return _b1_owner._utc_now_iso(facade=sys.modules[__name__])


def _write_text(path: Path, content: str) -> None:
    from scripts.diagnostics import m26_manifest_write_projection as _b2_owner
    return _b2_owner._write_text(path, content, facade=sys.modules[__name__])


def _seed_demo_dataset(root: Path) -> Path:
    from scripts.diagnostics import m26_manifest_seed_projection as _c03_11_k3_owner
    return _c03_11_k3_owner._seed_demo_dataset(root, facade=sys.modules[__name__])


def _validate_dataset(root: Path) -> Dict[str, Any]:
    from scripts.diagnostics import m26_manifest_validate_projection as _b06_c2_owner
    return _b06_c2_owner._validate_dataset(root, facade=sys.modules[__name__])


def _build_parser() -> argparse.ArgumentParser:
    from scripts.diagnostics import m26_manifest_parser_projection as _b5_owner
    return _b5_owner._build_parser(facade=sys.modules[__name__])


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    root = Path(str(args.dataset_root).strip())
    if bool(args.seed_demo):
        _seed_demo_dataset(root)

    out = _validate_dataset(root)
    if bool(args.json):
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(
            f"ok={out['ok']} dataset_root={out['dataset_root']} "
            f"required_file_total={out['required_file_total']} missing_file_total={out['missing_file_total']} "
            f"failure_total={out['failure_total']}"
        )
        for msg in list(out.get("failures") or []):
            print(msg)
        for rel in list(out.get("missing_files") or []):
            print(f"missing_file:{rel}")
    return 0 if bool(out.get("ok")) else 3


if __name__ == "__main__":
    raise SystemExit(main())
