#!/usr/bin/env python3
"""Fail if any text states a different odd/even -> form mapping than forms.json.

usage: python3 scripts/check_forms.py [extra_dir_or_file ...]
Scans labs/weekNN-*/worksheet.md and slides/weekNN.md (and any .md under the extra paths whose name or folder
carries a week number, e.g. instructor/classroom/week05-material.md), plus the general statements in
SUBMISSION.md and syllabus.md. Exit 0 = every statement agrees, 1 = at least one disagrees.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from forms_rule import ROOT, forms_for, load  # noqa: E402

CFG = load()


def classify(label):
    t = label.lower()
    if "air-sec" in t or re.search(r"parts?\s*3", t):
        return "air-sec"
    if "conventional" in t or re.search(r"part\s*2", t):
        return "conventional"
    return None


# Each pattern captures (what odd does, what even does).
PATTERNS = [
    re.compile(r"\*\*odd\s*=\s*([^*]+?)\*\*,\s*\*\*even\s*=\s*([^*]+?)\*\*"),
    re.compile(r"\*\*เลขคี่\s*=\s*([^*]+?)\*\*,\s*\*\*เลขคู่\s*=\s*([^*]+?)\*\*"),
    re.compile(r"ID ends (?:in an )?\*\*odd\*\*(?: digit)?\s*→\s*(\S+)\s*·\s*\*\*even\*\*\s*→\s*(\S+)"),
    re.compile(r"odd IDs do (Parts? [0-9 and]+?)[;,.] even IDs do (Parts? [0-9 and]+?)[.;,]"),
    re.compile(r"odd ID = (\S+) sheet, even ID = (\S+) sheet"),
    re.compile(r"เลขคี่ทำ (Part [0-9 และ]+?) เลขคู่ทำ (Part [0-9 และ]+)"),
]


def week_of(path):
    p = path.replace(os.sep, "/")
    for rx in (r"labs/week(\d\d)-", r"slides/week(\d\d)\.md", r"week(\d\d)-material", r"lessons/week(\d\d)"):
        m = re.search(rx, p)
        if m:
            return int(m.group(1))
    return None


def check_text(text, week, where):
    """Return (problems, statements_found) for one file's text."""
    problems, found = [], 0
    want = forms_for(week, CFG)
    for n, line in enumerate(text.splitlines(), 1):
        for rx in PATTERNS:
            for m in rx.finditer(line):
                found += 1
                odd, even = classify(m.group(1)), classify(m.group(2))
                if want is None:
                    problems.append(f"{where}:{n}: Week {week} has no form split in forms.json, but this line states a mapping")
                elif (odd, even) != (want["odd"], want["even"]):
                    problems.append(
                        f"{where}:{n}: Week {week} says odd={odd} even={even}; forms.json says odd={want['odd']} even={want['even']}")
    return problems, found


def check_general(path, text):
    """SUBMISSION.md lists weeks per mapping; syllabus.md states the rule in words."""
    problems = []
    name = os.path.basename(path)
    if name == "SUBMISSION.md":
        lists = list(re.finditer(r"[Ii]n Weeks ([0-9,\sand]+?)\s*\([^)]*\)\s*odd = ([A-Za-z-]+)", text, flags=re.S))
        if len(lists) != 2:
            problems.append(f"{path}: expected two 'In Weeks ... odd = <form>' lists, found {len(lists)}")
        for m in lists:
            form = classify(m.group(2))
            for w in map(int, re.findall(r"\d+", m.group(1))):
                want = forms_for(w, CFG)
                if want is None or want["odd"] != form:
                    problems.append(f"{path}: lists Week {w} under odd={form}; forms.json says {want}")
    if name == "syllabus.md":
        flip = CFG["flip_from_week"]
        even_w = flip + 1 if flip % 2 == 1 else flip
        odd_w = flip if flip % 2 == 1 else flip + 1
        for rx, week in ((r"in even-numbered weeks an odd digit does (\w[\w-]*)", even_w),
                         (r"in odd-numbered\s+weeks from Week \d+ an odd digit does (\w[\w-]*)", odd_w)):
            m = re.search(rx, text, flags=re.S)
            if m and classify(m.group(1)) != forms_for(week, CFG)["odd"]:
                problems.append(f"{path}: rule sentence says odd digit does {m.group(1)}; forms.json says {forms_for(week, CFG)['odd']}")
    return problems


def md_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for dp, dn, fn in os.walk(p):
            dn[:] = [d for d in dn if d not in (".git", "node_modules", "backup", "research", "__pycache__")]
            for f in sorted(fn):
                if f.endswith(".md"):
                    yield os.path.join(dp, f)


def main(argv):
    targets = [os.path.join(ROOT, "labs"), os.path.join(ROOT, "slides")] + [os.path.abspath(a) for a in argv]
    problems, scanned, with_statement = [], 0, 0
    for path in md_files(targets):
        w = week_of(path)
        if w is None:
            continue
        if os.path.basename(path) != "worksheet.md" and "/slides/" not in path.replace(os.sep, "/") and "-material" not in path:
            continue
        scanned += 1
        with open(path, encoding="utf8") as f:
            probs, found = check_text(f.read(), w, os.path.relpath(path, ROOT))
        problems += probs
        with_statement += 1 if found else 0
    for g in ("SUBMISSION.md", "syllabus.md"):
        gp = os.path.join(ROOT, g)
        if os.path.exists(gp):
            with open(gp, encoding="utf8") as f:
                problems += check_general(g, f.read())
    for p in problems:
        print("MISMATCH", p)
    print(f"checked {scanned} files ({with_statement} state a mapping), {len(problems)} mismatch(es)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
