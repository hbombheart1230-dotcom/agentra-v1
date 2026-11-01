from typing import Any, Dict


def _markdown(out: Dict[str, Any], *, facade: Any) -> str:
    lines = [f"# Log Archive Integrity ({out.get('day')})", "", f"- ok: **{bool(out.get('ok'))}**", f"- archive_dir: `{out.get('archive_dir')}`", f"- manifest_path: `{out.get('manifest_path')}`", f"- file_total: **{int(out.get('file_total') or 0)}**", f"- verified_total: **{int(out.get('verified_total') or 0)}**", "", "## Integrity Totals", "", f"- missing_file_total: {int(out.get('missing_file_total') or 0)}", f"- hash_mismatch_total: {int(out.get('hash_mismatch_total') or 0)}", f"- bytes_mismatch_total: {int(out.get('bytes_mismatch_total') or 0)}", f"- line_count_mismatch_total: {int(out.get('line_count_mismatch_total') or 0)}", "", "## Retention", "", f"- retention_days: {int(out.get('retention_days') or 0)}", f"- stale_archive_total: {int(out.get('stale_archive_total') or 0)}"]
    stale = out.get("stale_archive_days") if isinstance(out.get("stale_archive_days"), list) else []
    lines.append(f"- stale_archive_days: {', '.join(str(x) for x in stale)}" if stale else "- stale_archive_days: (none)")
    lines += ["", "## Failures", ""]
    failures = out.get("failures") if isinstance(out.get("failures"), list) else []
    lines.extend(f"- {msg}" for msg in failures) if failures else lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)
