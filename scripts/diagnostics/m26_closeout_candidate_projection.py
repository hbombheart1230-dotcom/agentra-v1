from pathlib import Path
from typing import Any


def _prepare_candidate_dataset(candidate_root: Path, *, day: str, facade: Any) -> None:
    facade._write_jsonl(candidate_root / "execution" / "intents.jsonl", [{"ts": f"{day}T00:01:00+00:00", "intent_id": "c-intent-1", "symbol": "005930", "action": "BUY", "qty": 1}, {"ts": f"{day}T00:02:00+00:00", "intent_id": "c-intent-2", "symbol": "005930", "action": "SELL", "qty": 1}])
    facade._write_jsonl(candidate_root / "execution" / "order_status.jsonl", [{"ts": f"{day}T00:01:05+00:00", "intent_id": "c-intent-1", "status": "filled"}, {"ts": f"{day}T00:02:05+00:00", "intent_id": "c-intent-2", "status": "filled"}])
    facade._write_jsonl(candidate_root / "execution" / "fills.jsonl", [{"ts": f"{day}T00:01:05+00:00", "intent_id": "c-intent-1", "fill_price": 100, "fill_qty": 1}, {"ts": f"{day}T00:02:05+00:00", "intent_id": "c-intent-2", "fill_price": 115, "fill_qty": 1}])
    (candidate_root / "market" / "ohlcv_1d.csv").write_text(f"ts,symbol,open,high,low,close,volume\n{day}T00:00:00+00:00,005930,100,116,99,115,1000\n", encoding="utf-8")
