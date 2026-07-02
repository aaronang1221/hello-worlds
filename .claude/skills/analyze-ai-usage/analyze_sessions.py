#!/usr/bin/env python3
"""Parse Claude Code session transcripts (~/.claude/projects/**/*.jsonl) and
print aggregate usage statistics as markdown.

Usage:
  python3 analyze_sessions.py [--projects-dir DIR] [--project NAME] [--last N]

The script is deterministic and read-only. It emits:
  - a per-session table (task, duration, turns, tool calls, errors, idle time)
  - tool usage totals across sessions
  - top Bash command heads (first token of each command)
  - skills invoked
  - tools with the highest error rates
  - the first user message of every session (for semantic clustering upstream)
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

IDLE_GAP_SECONDS = 300  # gaps longer than this count as waiting/idle time


def parse_ts(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def first_line(text, limit=90):
    line = (text or "").strip().splitlines()[0] if (text or "").strip() else ""
    return line[:limit] + ("…" if len(line) > limit else "")


def analyze_session(path):
    s = {
        "file": path,
        "session_id": path.stem,
        "project": path.parent.name,
        "task": "",
        "start": None,
        "end": None,
        "user_turns": 0,
        "tools": Counter(),
        "bash_heads": Counter(),
        "skills": Counter(),
        "errors": Counter(),
        "idle_seconds": 0.0,
        "idle_gaps": 0,
        "user_messages": [],
    }
    prev_ts = None
    with open(path, encoding="utf-8") as f:
        for raw in f:
            try:
                rec = json.loads(raw)
            except json.JSONDecodeError:
                continue
            ts = parse_ts(rec.get("timestamp"))
            if ts:
                if s["start"] is None:
                    s["start"] = ts
                s["end"] = ts
                if prev_ts:
                    gap = (ts - prev_ts).total_seconds()
                    if gap > IDLE_GAP_SECONDS:
                        s["idle_seconds"] += gap
                        s["idle_gaps"] += 1
                prev_ts = ts

            msg = rec.get("message") or {}
            content = msg.get("content")

            if rec.get("type") == "user" and msg.get("role") == "user":
                # Plain human input has string content; tool results are lists
                # of tool_result blocks.
                if isinstance(content, str):
                    s["user_turns"] += 1
                    s["user_messages"].append(content)
                    if not s["task"]:
                        s["task"] = content
                elif isinstance(content, list):
                    human_text = []
                    for block in content:
                        if not isinstance(block, dict):
                            continue
                        if block.get("type") == "text":
                            human_text.append(block.get("text", ""))
                        elif block.get("type") == "tool_result" and block.get("is_error"):
                            s["errors"]["(unattributed)"] += 1
                    if human_text:
                        s["user_turns"] += 1
                        joined = "\n".join(human_text)
                        s["user_messages"].append(joined)
                        if not s["task"]:
                            s["task"] = joined

            if rec.get("type") == "assistant" and isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != "tool_use":
                        continue
                    name = block.get("name", "?")
                    s["tools"][name] += 1
                    inp = block.get("input") or {}
                    if name == "Bash":
                        cmd = (inp.get("command") or "").strip()
                        if cmd:
                            s["bash_heads"][cmd.split()[0]] += 1
                    elif name == "Skill":
                        s["skills"][inp.get("skill", "?")] += 1

            if rec.get("toolUseResult") and rec.get("type") == "user":
                pass  # already counted via tool_result blocks above
    return s


def fmt_duration(seconds):
    if seconds is None:
        return "-"
    m, sec = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m" if h else f"{m}m{sec:02d}s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--projects-dir", default=str(Path.home() / ".claude" / "projects"))
    ap.add_argument("--project", help="only analyze this project directory name")
    ap.add_argument("--last", type=int, default=50, help="max sessions, newest first")
    args = ap.parse_args()

    root = Path(args.projects_dir).expanduser()
    if not root.is_dir():
        sys.exit(f"projects dir not found: {root}")

    files = sorted(root.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if args.project:
        files = [p for p in files if p.parent.name == args.project]
    files = files[: args.last]
    if not files:
        sys.exit("no session transcripts found")

    sessions = [analyze_session(p) for p in files]
    sessions = [s for s in sessions if s["user_turns"] or s["tools"]]

    print(f"# Claude Code usage report — {len(sessions)} sessions\n")

    print("## Sessions (newest first)\n")
    print("| # | Project | Task (first message) | Duration | Turns | Tool calls | Errors | Idle |")
    print("|---|---------|----------------------|----------|-------|------------|--------|------|")
    for i, s in enumerate(sessions, 1):
        dur = (s["end"] - s["start"]).total_seconds() if s["start"] and s["end"] else None
        print(
            f"| {i} | {s['project']} | {first_line(s['task'])} | {fmt_duration(dur)} "
            f"| {s['user_turns']} | {sum(s['tools'].values())} "
            f"| {sum(s['errors'].values())} | {fmt_duration(s['idle_seconds']) if s['idle_gaps'] else '-'} |"
        )

    all_tools, all_bash, all_skills, all_errors = Counter(), Counter(), Counter(), Counter()
    for s in sessions:
        all_tools += s["tools"]
        all_bash += s["bash_heads"]
        all_skills += s["skills"]
        all_errors += s["errors"]

    print("\n## Tool usage totals\n")
    for name, n in all_tools.most_common(25):
        err = all_errors.get(name, 0)
        print(f"- {name}: {n}" + (f"  ({err} errors)" if err else ""))

    if all_bash:
        print("\n## Top Bash commands (first token)\n")
        for cmd, n in all_bash.most_common(20):
            print(f"- {cmd}: {n}")

    if all_skills:
        print("\n## Skills invoked\n")
        for name, n in all_skills.most_common():
            print(f"- {name}: {n}")

    print("\n## First message of every session (for clustering)\n")
    for i, s in enumerate(sessions, 1):
        print(f"{i}. [{s['project']}] {first_line(s['task'], 200)}")


if __name__ == "__main__":
    main()
