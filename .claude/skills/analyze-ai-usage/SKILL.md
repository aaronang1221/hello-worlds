---
name: analyze-ai-usage
description: Analyze past Claude Code work sessions to find recurring tasks, time sinks, and workflow bottlenecks, then recommend high-leverage improvements (new skills, scheduled automation, CLAUDE.md tuning, permission allowlists). Use when the user asks to review how they use AI, audit their Claude usage, or optimize their workflow.
---

# Analyze AI usage

Analyze the user's past Claude Code sessions and produce an optimization report.
Reply in the user's language.

## Important: where transcripts live

Session transcripts are JSONL files under `~/.claude/projects/<project-dir>/*.jsonl`.
They exist on the machine where the sessions ran. In a cloud/remote container only
the current session exists — tell the user to run this skill on their local machine
if you find fewer than ~3 transcripts.

## Step 1 — Collect statistics

Run the bundled parser (read-only, no network):

```bash
python3 .claude/skills/analyze-ai-usage/analyze_sessions.py --last 50
```

Useful flags: `--project <dir-name>` to scope to one project, `--projects-dir` if
transcripts live elsewhere. The report includes a per-session table, tool totals,
top Bash commands, skill usage, error counts, and every session's first message.

## Step 2 — Cluster the tasks semantically

The script cannot judge meaning — you do that. From the "first message of every
session" list, group sessions into task types (e.g. "weekly report generation",
"dependency bumps", "debugging test failures", "email triage"). Count each
cluster. If first messages are too thin, read the 2–3 largest transcripts
directly (Grep for `"origin":{"kind":"human"}` lines) to see the real back-and-forth.

## Step 3 — Find the waste

Look for these specific patterns:

- **Repeated tasks**: same cluster appearing ≥3 times → candidate for a new skill.
- **Repeated instructions**: the user re-explains the same context/preferences in
  many sessions (build commands, code style, deploy steps) → belongs in CLAUDE.md.
- **High idle time**: sessions with large "Idle" values were blocked waiting on the
  user — usually permission prompts or ambiguous requests. Repeated safe commands
  should go into a permission allowlist (`/fewer-permission-prompts` automates this).
- **High error counts** on one tool: flaky setup, wrong env, or missing docs —
  a SessionStart hook or CLAUDE.md note usually fixes it.
- **Many turns for routine work**: >10 turns on a task type that should be one-shot
  means the prompt or CLAUDE.md lacks context.
- **Time-anchored tasks** ("every Monday…", "daily…"): candidates for scheduled
  automation (Claude Code on the web scheduled sessions, or local cron invoking
  `claude -p`).

## Step 4 — Write the report

Deliver a markdown report with, in this order:

1. **TL;DR** — the 3 highest-leverage changes, ranked by estimated time saved.
2. **Usage profile** — task clusters with counts, total/average session time, top tools.
3. **Bottlenecks** — each waste pattern found, with the evidence (session numbers).
4. **Concrete recommendations** — for each one, do the work, don't just suggest it:
   - New skill → draft the `SKILL.md` (offer to create it in `.claude/skills/`).
   - Scheduled automation → give the exact schedule + prompt to configure.
   - CLAUDE.md → propose the exact lines to add (offer to apply them).
   - Permissions → list the exact `allow` rules for `.claude/settings.json`.

Ask before writing anything outside the report itself.
