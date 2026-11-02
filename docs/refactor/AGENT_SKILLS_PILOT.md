# Agentra P1.5 — optional skills pilot

This is a **non-executing proposal**, not a replacement work order, policy update, or automatic plugin installation. Current D00, CURRENT, C01/C02, C03/C04/C05 and the existing FAST-3 schedules remain unchanged.

## Portable skill files
- `.agents/skills/agentra-rf-executor/SKILL.md`: use with Codex B / Claude A only after their existing single-entrypoint order; no self-assignment.
- `.agents/skills/agentra-contract-guard/SKILL.md`: read-only contract and owner-boundary analysis.
- `.agents/skills/agentra-done-verifier/SKILL.md`: read-only evidence audit for C04/C05/C06.

## Deployment notes
ChatGPT-side Superpowers, Context7 and GitHub connections **do not automatically propagate** to scheduled cloud actors, local Hermes/Pi, or Claude. Before enabling, confirm the specific runtime supports skill loading and the exact discoverable path, then opt in on one isolated invocation. If that runtime does not support this path, explicitly supply the skill text instead; do not claim it loaded.

Recommended pilot: one newly authorized C01/C02 pure-owner item. Capture initial order, actual runtime skill availability, one changed-scope targeted test (normal exit 0), non-force actor remote SHA, and no additional gate. Compare with prior actor evidence for premature stop, repeated unchanged tests, successful push, and newly closed RFs. This pilot does not itself grant write permission or change the currently running C01 order.

## Rollout gates
1. Review this PR against current D00 and updated HEAD; no policy edits.
2. Confirm skill discovery in each runtime **independently**, without assuming ChatGPT installation means cloud installation.
3. Lead C03, not this pilot, embeds only relevant brief guidance into future C01/C02 order if explicitly authorized. No A/B document writes.
4. C04/C05 retain exact SHA integration and G1/G2/G3 ownership; C06 measures RF_DONE_DELTA separately from BODY MOVEs.
5. If agent responsiveness worsens or extra mandatory gates appear, disable pilot with no dependency in production execution.

## Safety
No live trades, Guard/approval edits, operational state/database, credentials, RunLab, CI workflow, or frozen oracle modifications are authorized by these skills.
