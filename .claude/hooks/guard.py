"""PreToolUse guard: enforce CLAUDE.md token/safety rules mechanically.

deny  -> exit 2 + stderr (model sees reason, must change approach)
ask   -> JSON permissionDecision=ask (user decides)
"""
import json
import os
import re
import sys

BIG_BYTES = 24_000  # ~6k tokens; reading above this without a range is wasteful
KB_HINT = "Pakai KB dulu: rag-kb `kb ask '<pertanyaan>'` (lihat docs/harness-kb.md), atau baca dengan offset/limit."


def deny(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(2)


def ask(msg):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": msg}}))
    sys.exit(0)


def check_read(inp):
    path = inp.get("file_path", "")
    if inp.get("limit"):
        return
    try:
        size = os.path.getsize(path)
    except OSError:
        return
    if size > BIG_BYTES and path.lower().endswith((".md", ".log", ".txt", ".json", ".yml", ".yaml", ".sql")):
        deny(f"DIBLOKIR: {os.path.basename(path)} {size // 1024} KB dibaca penuh tanpa limit. {KB_HINT}")


def check_bash(cmd):
    if re.search(r"\b(cat|type|Get-Content|gc|less|more)\b[^|;&\n]*CHANGELOG", cmd) and not re.search(
            r"\b(head|tail|-TotalCount|-Tail|grep|rg|Select-String)\b", cmd):
        deny("DIBLOKIR: jangan baca CHANGELOG penuh. Pakai `head -n 30 CHANGELOG.md` atau `kb ask`.")
    if re.search(r"\bwhile\b[^\n]*\bsleep\b|\buntil\b[^\n]*\bsleep\b|\bsleep\s+\d+\s*(&&|;)\s*\S", cmd):
        deny("DIBLOKIR: dilarang polling/sleep-loop (CLAUDE.md 2.5). Jalankan di background lalu berhenti memanggil tool.")
    if re.search(r"\bgit\s+push\b[^\n]*(--force\b|--force-with-lease|\s-f\b)|\bgit\s+reset\s+--hard\b|\bgit\s+clean\s+-[a-z]*f", cmd):
        ask("Perintah git destruktif: butuh konfirmasi eksplisit user (CLAUDE.md safety).")


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # never break the session on malformed input
    tool, inp = data.get("tool_name"), data.get("tool_input", {})
    if tool == "Read":
        check_read(inp)
    elif tool in ("Bash", "PowerShell"):
        check_bash(inp.get("command", ""))
    sys.exit(0)


if __name__ == "__main__":
    main()
