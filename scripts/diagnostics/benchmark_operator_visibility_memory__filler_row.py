from typing import Any, Dict

def _filler_row(day: str, i: int, facade: Any) -> Dict[str, Any]:
    even=i%2==0
    return {"run_id":f"q9_comparison_forward_recovery_{day.replace('-', '')}_{i:06d}_1","ts":f"{day}T01:{(i//3600)%60:02d}:{i%60:02d}+00:00","stage":"skill_execute" if even else "skill_result","event":"call" if even else "ok","event_name":"skill_execute.call" if even else "skill_result.ok","level":"info","trade_id":"","session_id":"","cycle_id":"","agent":"skill_execute" if even else "skill_result","phase":"","symbol":"","payload":{"skill":"market.minute_ohlcv","api_id":"ka10080","step":0,"path":"/api/dostk/chart","outputs":"MinuteOHLCVDTO"}}
