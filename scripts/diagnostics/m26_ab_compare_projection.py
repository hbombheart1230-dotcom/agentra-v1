from typing import Any, Dict, List, Tuple


def _compare_metrics(*, a_label: str, b_label: str, a_score: Dict[str, Any], b_score: Dict[str, Any], facade: Any) -> Dict[str, Any]:
    metric_rules: List[Tuple[str, str]] = [
        ("total_pnl_proxy", "higher"), ("risk_adjusted.sortino_proxy", "higher"),
        ("risk_adjusted.sharpe_proxy", "higher"), ("drawdown.max_drawdown_ratio", "lower"), ("win_rate", "higher"),
    ]
    eps = 1e-12
    points: Dict[str, int] = {a_label: 0, b_label: 0}
    results: List[Dict[str, Any]] = []
    for metric, direction in metric_rules:
        a_val = facade._json_path_get(a_score, metric, 0.0)
        b_val = facade._json_path_get(b_score, metric, 0.0)
        winner = "tie"
        if direction == "higher":
            if b_val > a_val + eps: winner = b_label; points[b_label] += 1
            elif a_val > b_val + eps: winner = a_label; points[a_label] += 1
        else:
            if b_val + eps < a_val: winner = b_label; points[b_label] += 1
            elif a_val + eps < b_val: winner = a_label; points[a_label] += 1
        results.append({"metric": metric, "direction": direction, "a_value": float(a_val), "b_value": float(b_val), "delta_b_minus_a": float(b_val-a_val), "winner": winner})
    winner = b_label if points[b_label] > points[a_label] else a_label if points[a_label] > points[b_label] else "tie"
    a_pnl, b_pnl = facade._json_path_get(a_score, "total_pnl_proxy", 0.0), facade._json_path_get(b_score, "total_pnl_proxy", 0.0)
    a_sortino, b_sortino = facade._json_path_get(a_score, "risk_adjusted.sortino_proxy", 0.0), facade._json_path_get(b_score, "risk_adjusted.sortino_proxy", 0.0)
    a_dd, b_dd = facade._json_path_get(a_score, "drawdown.max_drawdown_ratio", 0.0), facade._json_path_get(b_score, "drawdown.max_drawdown_ratio", 0.0)
    recommended, reasons = "hold", []
    if winner == b_label:
        recommended = f"promote_{b_label}" if b_pnl >= a_pnl and b_sortino >= a_sortino and b_dd <= a_dd else f"no_promote_{b_label}"
        reasons.append("b beats or matches A on pnl/sortino and keeps drawdown no worse" if recommended.startswith("promote") else "b wins points but fails conservative promotion gate")
    elif winner == a_label:
        recommended = f"promote_{a_label}" if a_pnl >= b_pnl and a_sortino >= b_sortino and a_dd <= b_dd else f"no_promote_{a_label}"
        reasons.append("a beats or matches B on pnl/sortino and keeps drawdown no worse" if recommended.startswith("promote") else "a wins points but fails conservative promotion gate")
    else: reasons.append("tie result")
    return {"metric_results": results, "points": points, "winner": winner, "promotion_gate": {"recommended_action": recommended, "reasons": reasons}}
