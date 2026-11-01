from pathlib import Path
from typing import Any, Dict


def _seed_demo_dataset(root: Path, *, facade: Any) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    csv_seed = "ts,symbol,open,high,low,close,volume\n2026-02-17T00:00:00+00:00,005930,70000,70500,69900,70300,120000\n"
    for name in ("ohlcv_1m.csv", "ohlcv_5m.csv", "ohlcv_1d.csv"):
        facade._write_text(root / "market" / name, csv_seed)
    facade._write_text(root / "market" / "corporate_actions.csv", "symbol,action,effective_date,ratio\n005930,split,2026-01-15,1.0\n")
    records = {
        "execution/intents.jsonl": {"ts": "2026-02-17T00:01:00+00:00", "intent_id": "demo-intent-1", "symbol": "005930", "action": "BUY", "qty": 1},
        "execution/order_status.jsonl": {"ts": "2026-02-17T00:01:05+00:00", "intent_id": "demo-intent-1", "status": "filled"},
        "execution/fills.jsonl": {"ts": "2026-02-17T00:01:05+00:00", "intent_id": "demo-intent-1", "fill_price": 70300, "fill_qty": 1},
        "microstructure/top_of_book.jsonl": {"ts": "2026-02-17T00:00:30+00:00", "symbol": "005930", "bid": 70200, "ask": 70300},
        "features/scanner_monitor_features.jsonl": {"ts": "2026-02-17T00:00:40+00:00", "symbol": "005930", "features": {"rsi14": 55.2, "ma20_gap": 0.01}},
        "news/headlines.jsonl": {"ts": "2026-02-17T00:00:50+00:00", "symbol": "005930", "title": "demo headline"},
        "news/sentiment_by_symbol.jsonl": {"ts": "2026-02-17T00:00:55+00:00", "symbol": "005930", "sentiment": 0.15},
        "news/sentiment_daily.jsonl": {"ts": "2026-02-17T00:00:59+00:00", "market_sentiment": 0.08},
    }
    for name, record in records.items():
        facade._write_text(root / name, facade.json.dumps(record, ensure_ascii=False) + "\n")
    manifest: Dict[str, Any] = {"schema_version": facade.SCHEMA_VERSION, "dataset_id": "m26-fixed-demo-v1", "generated_at": facade._utc_now_iso(), "components": {k: list(v) for k, v in facade.REQUIRED_COMPONENT_FILES.items()}}
    manifest_path = root / "manifest.json"
    facade._write_text(manifest_path, facade.json.dumps(manifest, ensure_ascii=False, indent=2))
    return manifest_path
