#!/usr/bin/env python3
"""Run the benchmark for THIS repository. Standard library only, no network beyond the agent CLI.

    python bench/run.py --arm bare                 # the control: nothing installed
    python bench/run.py --arm facts                # with this repository's fact sheet injected
    python bench/run.py --arm facts --rep r2       # the second replicate
    python bench/run.py --arm bare --case case-003 # one case

Each run writes one JSON row per case under `results/<arm>-<rep>/`. `bench/analyse.py` then compares
two arms. Nothing here depends on the vendor's own tooling: the agent is invoked through its CLI, the
scoring is arithmetic, and every file this produces is yours.

WHY THE SHAPE IS LIKE THIS
--------------------------
Two arms, two replicates, and an answer key that was fixed before any run — because the alternative
produces numbers that look solid and are not. The campaign this kit comes out of published a result
and had to retract it: a context file was being written into every session and `bytes_written` proved
it, while exactly 1 session in 106 ever read it. Two behaviourally identical arms then differed by
enough to pass a ten-seed bootstrap. So:

  * a mechanism is only ever counted by an EVENT it logs itself, never by its own installation;
  * each arm runs TWICE, and the two replicates sit at opposite ends of the run, so the difference
    between them measures the drift of the day;
  * and `analyse.py` treats that difference as a VETO: if an arm differs from itself on a metric,
    that metric is not read for this repository. Not explained. Not read.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(HERE, "cases")
RESULTS = os.path.join(HERE, "results")
#: the tree the agent works in. By default the repository this kit sits beside; override to point at
#: a pristine checkout you keep elsewhere.
TREE = os.environ.get("KIT_TREE") or os.path.join(HERE, "repo")

QUESTION_INSTRUCTION = (
    "Answer the question above about this repository. End your reply with the heading FILES: "
    "followed by every repository-relative file path your answer involves, one per line and "
    "nothing else on those lines. Be complete: a path you omit counts as missed.")
FIX_INSTRUCTION = (
    "Fix the problem described above by editing the source. Do not add or modify any test.")

#: the hook that injects the fact sheet. UserPromptSubmit, once per session, and it LOGS the
#: injection: a sheet that is written but never delivered is the exact defect this kit guards
#: against, and the log line is the only honest proof that it arrived.
HOOK = '''import json, os, sys
SHEET, LEDGER = %s, %s
sys.stdin.read()
try:
    body = open(SHEET, encoding="utf-8").read()
except OSError:
    sys.exit(0)
if not body.strip():
    sys.exit(0)
try:
    n = sum(1 for _ in open(LEDGER, encoding="utf-8"))
except OSError:
    n = 0
if n:
    sys.exit(0)
try:
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8") as lg:
        lg.write(str(len(body)) + chr(10))
except OSError:
    pass
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                         "additionalContext": body}}))
sys.exit(0)
'''


def cases() -> list[str]:
    if not os.path.isdir(CASES):
        sys.exit(f"no cases directory at {CASES}")
    return sorted(d for d in os.listdir(CASES) if d.startswith("case-"))


def gold(case: str) -> dict:
    with open(os.path.join(CASES, case, "gold.json"), encoding="utf-8") as f:
        return json.load(f) or {}


def build_tree(case: str, dest: str) -> None:
    """A fresh copy of the tree for this case, with its inversion applied if it has one.

    A case with no `inversion.patch` is a QUESTION: it changes no code, so there is nothing to
    invert and the pristine tree is the task.
    """
    shutil.copytree(TREE, dest, ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules"))
    p = os.path.join(CASES, case, "inversion.patch")
    patch = ""
    if os.path.isfile(p):
        with open(p, encoding="utf-8") as f:
            patch = f.read()
    if not patch.strip():
        return
    subprocess.run(["git", "-C", dest, "init", "-q"], capture_output=True, timeout=120)
    # BINARY stdin deliberately: text mode rewrites every newline on Windows and `git apply` then
    # rejects every hunk, which turns a whole run into build errors that look like agent failures.
    r = subprocess.run(["git", "-C", dest, "apply", "-R", "-"], input=patch.encode("utf-8"),
                       capture_output=True, timeout=180)
    shutil.rmtree(os.path.join(dest, ".git"), ignore_errors=True)
    if r.returncode != 0:
        raise RuntimeError("inversion did not apply: "
                           + (r.stderr or b"").decode("utf-8", "replace")[:200])


def install(arm: str, cwd: str, ledger: str) -> dict:
    """Install what the arm names, and prove it can speak before the session starts."""
    fire = {"arm": arm, "sheet_bytes": 0, "selftest": 0}
    if arm == "bare":
        return fire
    sheet_src = os.path.join(HERE, "facts.md")
    if not os.path.isfile(sheet_src):
        raise RuntimeError("arm 'facts' needs facts.md beside this kit")
    with open(sheet_src, encoding="utf-8") as f:
        body = f.read()
    if len(body.strip()) < 200:
        raise RuntimeError("facts.md is empty or near-empty")
    sheet = os.path.join(cwd, ".kit", "facts.md")
    os.makedirs(os.path.dirname(sheet), exist_ok=True)
    with open(sheet, "w", encoding="utf-8") as f:
        f.write(body)
    hook = os.path.join(cwd, ".kit", "hook.py")
    with open(hook, "w", encoding="utf-8") as f:
        f.write(HOOK % (json.dumps(sheet), json.dumps(ledger)))
    sp = os.path.join(cwd, ".claude", "settings.json")
    os.makedirs(os.path.dirname(sp), exist_ok=True)
    st = {}
    if os.path.isfile(sp):
        try:
            with open(sp, encoding="utf-8") as f:
                st = json.load(f)
        except Exception:
            st = {}
    hooks = dict(st.get("hooks") or {})
    cmd = f'"{sys.executable}" "{hook}"'
    hooks["UserPromptSubmit"] = list(hooks.get("UserPromptSubmit") or []) + [
        {"hooks": [{"type": "command", "command": cmd}]}]
    st["hooks"] = hooks
    with open(sp, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)
    fire["sheet_bytes"] = len(body)
    # FIRE IT NOW. An installation is not a delivery, and this kit exists because that distinction
    # was once got wrong at the cost of a published result.
    probe = json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": "x", "cwd": cwd})
    sr = subprocess.run([sys.executable, hook], input=probe, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=60)
    ctx = ""
    for ln in (sr.stdout or "").splitlines():
        if ln.startswith("{"):
            ctx = ((json.loads(ln).get("hookSpecificOutput") or {}).get("additionalContext") or "")
    if body[:80] not in ctx:
        raise RuntimeError("the fact-sheet hook did not return the sheet; refusing to run an arm "
                           "that cannot deliver what it claims")
    fire["selftest"] = len(ctx)
    try:
        os.remove(ledger)            # the self-test counts itself; the measurement is the session's
    except OSError:
        pass
    return fire


def injections(ledger: str) -> int:
    try:
        with open(ledger, encoding="utf-8") as f:
            return sum(1 for ln in f if ln.strip())
    except OSError:
        return 0


def recall(answer: str, files: list) -> float:
    """How much of the answer key the reply named, 0..1.

    Matching requires directory evidence: a bare `config.go` earns nothing, because a generic
    basename would otherwise score against any repository.
    """
    if not files:
        return 0.0
    text = (answer or "").replace("\\", "/")
    raw = re.findall(r"[A-Za-z0-9_./+-]+", text)
    toks = set(raw) | {t.rstrip(".,;:)]}'\"`") for t in raw}
    hit = 0
    for g in files:
        g = str(g).replace("\\", "/")
        if any(t == g or t.endswith("/" + g) or ("/" in t and g.endswith("/" + t)) for t in toks):
            hit += 1
    return round(hit / len(files), 4)


def run_tests(cwd: str, want: list) -> dict:
    """Run the tests the case declared failing. Returns a result only when the suite really ran.

    A grader that cannot run must never report success. This refuses to score unless it sees a
    return code and a summary it can parse — the alternative once reported a pass from a suite that
    had failed to import.
    """
    if not want:
        return {}
    cmd = os.environ.get("KIT_TEST_CMD") or ""
    if not cmd:
        return {"tests_ran": False, "tests_error": "KIT_TEST_CMD is not set"}
    r = subprocess.run(cmd.split() + list(want), cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=int(os.environ.get("KIT_TEST_TIMEOUT", "1800")))
    out = (r.stdout or "") + (r.stderr or "")
    failed = {ln.split(" - ")[0][len("FAILED "):].strip()
              for ln in out.splitlines() if ln.startswith("FAILED ")}
    ran = r.returncode in (0, 1) and ("passed" in out or "failed" in out or failed)
    still = sorted(w for w in want if any(w in f or f in w for f in failed))
    return {"tests_ran": bool(ran), "tests_still_failing": still,
            "resolved": bool(ran and not still),
            "tests_error": "" if ran else out[-400:]}


def isolated_config(tmp: str) -> dict:
    """An environment where the measurement is of the repository and the arm, and nothing else.

    AN INSTRUMENT MUST CONTROL ITS ENVIRONMENT. Run without this, the agent inherits whatever the
    operator has installed globally — hooks, MCP servers, session state. On the machine this kit was
    built on, that produced a control session of ONE turn whose reply began "I've already provided
    the complete analysis", scoring zero while costing as much as a real run. A control arm that
    does not do the task makes the treatment look excellent for free, which is the worst defect a
    measuring tool can have.

    Set KIT_USE_HOST_CONFIG=1 if you deliberately want to measure your own global setup — that is a
    legitimate question, just a different one.
    """
    env = dict(os.environ)
    if os.environ.get("KIT_USE_HOST_CONFIG") == "1":
        return env
    cfg = os.path.join(tmp, "agentconf")
    os.makedirs(cfg, exist_ok=True)
    # carry ONLY the credential, so the agent can authenticate and inherits no behaviour
    for name in (".credentials.json", "credentials.json"):
        src = os.path.join(os.path.expanduser("~"), ".claude", name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(cfg, ".credentials.json"))
            break
    env["CLAUDE_CONFIG_DIR"] = cfg
    for k in ("CLAUDE_CODE_SESSION_ID", "ANTHROPIC_LOG"):
        env.pop(k, None)
    return env


def one(case: str, arm: str, rep: str, model: str, timeout: int) -> dict:
    out_dir = os.path.join(RESULTS, f"{arm}-{rep}")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "_row", case + ".json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.isfile(dest):
        return json.load(open(dest, encoding="utf-8"))      # resume-safe
    g = gold(case)
    tmp = tempfile.mkdtemp(prefix="kit-")
    cwd = os.path.join(tmp, "t")
    ledger = os.path.join(tmp, "ledger.log")
    row = {"case": case, "arm": arm, "rep": rep, "model": model}
    try:
        build_tree(case, cwd)
        row["fire"] = install(arm, cwd, ledger)
        with open(os.path.join(CASES, case, "prompt.md"), encoding="utf-8") as f:
            prose = f.read().strip()
        is_q = not (g.get("fail_to_pass") or [])
        prompt = prose + "\n\n" + (QUESTION_INSTRUCTION if is_q else FIX_INSTRUCTION)
        tools = "Read,Grep,Glob,Bash" + ("" if is_q else ",Edit,Write,MultiEdit")
        t0 = time.time()
        r = subprocess.run(["claude", "-p", prompt, "--model", model, "--output-format", "json",
                            "--allowedTools", tools, "--strict-mcp-config"],
                           cwd=cwd, env=isolated_config(tmp), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        row["seconds"] = round(time.time() - t0, 1)
        d = {}
        try:
            d = json.loads(r.stdout or "{}")
        except Exception:
            pass
        if r.returncode != 0 or d.get("is_error") or not d:
            row["error"] = ("agent failed: " + str(d.get("result") or (r.stderr or "")[:200]))[:300]
        elif int(d.get("num_turns") or 0) <= 1 and not str(d.get("result") or "").strip():
            # a single turn with an empty answer is a failed session, not a score of zero. Scoring
            # it would quietly credit the other arm.
            row["error"] = "agent returned one turn and no answer"
        row["answer"] = str(d.get("result") or "")
        row["cost"] = float(d.get("total_cost_usd") or 0.0)
        row["turns"] = int(d.get("num_turns") or 0)
        row["injections"] = injections(ledger)
        row["task"] = "question" if is_q else "fix"
        if is_q:
            # scored over the subset of the key the fact sheet does NOT itself name, so an arm
            # carrying the sheet gets no free marks; the subset was fixed before any run
            key = g.get("files_unleaked") or g.get("files") or []
            row["recall"] = recall(row["answer"], key)
            row["key_size"] = len(key)
        else:
            row.update(run_tests(cwd, g.get("fail_to_pass") or []))
    except Exception as e:
        row["error"] = f"{type(e).__name__}: {str(e)[:260]}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(row, f, indent=1)
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arm", required=True, choices=["bare", "facts"])
    ap.add_argument("--rep", default="r1", help="r1 or r2; run BOTH, they are the noise floor")
    ap.add_argument("--case", default="", help="one case id, for a smoke")
    ap.add_argument("--model", default=os.environ.get("KIT_MODEL", "claude-sonnet-4-5"))
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()
    if not os.path.isdir(TREE):
        sys.exit(f"no tree at {TREE} — set KIT_TREE to your checkout")
    todo = [a.case] if a.case else cases()
    print(f"{len(todo)} case(s) · arm {a.arm}-{a.rep} · model {a.model}")
    for c in todo:
        row = one(c, a.arm, a.rep, a.model, a.timeout)
        bits = [f"{c}", f"${row.get('cost', 0):.3f}", f"{row.get('turns', 0)}t",
                f"inj={row.get('injections', 0)}"]
        if row.get("task") == "question":
            bits.append(f"recall={row.get('recall')}")
        elif "resolved" in row:
            bits.append(f"resolved={row.get('resolved')}")
        if row.get("error"):
            bits.append("ERROR " + str(row["error"])[:80])
        print("  " + "  ".join(bits), flush=True)
    print(f"\nrows under {os.path.join(RESULTS, a.arm + '-' + a.rep, '_row')}")
    print("run the other arm and both replicates, then: python bench/analyse.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
