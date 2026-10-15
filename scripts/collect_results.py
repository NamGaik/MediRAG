"""
collect_results.py  -  gather every existing output into results/ in one go.

Put this in the MediRAG root folder and run:   python collect_results.py

It does NOT change or move your original files. It:
  1. searches the whole project for result files (.json, .csv, .txt, .png, .jpg)
  2. copies them into results/collected/<original folder path>/
  3. writes results/SUMMARY.md listing every file, where it came from,
     when it was last modified, and the numbers inside small JSON files.

Re-run it any time; it rebuilds the collected copy and summary from scratch.
"""
import csv
import json
import os
import shutil
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(ROOT, "results")
COLLECTED = os.path.join(RESULTS, "collected")

KEEP_EXT = {".json", ".csv", ".txt", ".png", ".jpg", ".jpeg"}
SKIP_DIRS = {".git", "venv", ".venv", "env", "__pycache__", "node_modules",
             "site-packages", ".idea", ".vscode"}
# model/tokenizer files that are not results
SKIP_FILES = {"config.json", "tokenizer.json", "tokenizer_config.json",
              "special_tokens_map.json", "vocab.txt", "merges.txt",
              "generation_config.json", "requirement.txt", "requirements.txt",
              "training_args.json", "adapter_config.json"}
MAX_MB = 20


def flat_numbers(d, prefix=""):
    """Flatten a JSON dict into (key, value) rows of simple values."""
    rows = []
    if isinstance(d, dict):
        for k, v in d.items():
            rows += flat_numbers(v, f"{prefix}{k}." if isinstance(v, dict) else f"{prefix}{k}")
    elif isinstance(d, (int, float, str, bool)) or d is None:
        rows.append((prefix.rstrip("."), d))
    return rows


def describe(path, ext):
    try:
        if ext == ".json":
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            rows = flat_numbers(data)
            if isinstance(data, list):
                return f"JSON list with {len(data)} items"
            if 0 < len(rows) <= 40:
                lines = ["| key | value |", "|---|---|"]
                for k, v in rows:
                    if isinstance(v, float):
                        v = round(v, 4)
                    lines.append(f"| {k} | {v} |")
                return "\n".join(lines)
            return f"JSON with {len(rows)} values (too large to show)"
        if ext == ".csv":
            with open(path, encoding="utf-8", errors="ignore") as f:
                r = list(csv.reader(f))
            head = ", ".join(r[0]) if r else ""
            return f"CSV, {max(len(r) - 1, 0)} rows. Columns: {head}"
        if ext == ".txt":
            with open(path, encoding="utf-8", errors="ignore") as f:
                txt = f.read(600)
            return "```\n" + txt + ("\n..." if len(txt) == 600 else "") + "\n```"
        return "Image / figure"
    except Exception as e:
        return f"(could not read: {e})"


def main():
    if os.path.exists(COLLECTED):
        shutil.rmtree(COLLECTED)
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith("checkpoint-")
                       and os.path.join(dirpath, d) != COLLECTED]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in KEEP_EXT or fn in SKIP_FILES:
                continue
            src = os.path.join(dirpath, fn)
            if os.path.getsize(src) > MAX_MB * 1024 * 1024:
                continue
            rel = os.path.relpath(src, ROOT)
            if rel == os.path.join("results", "SUMMARY.md"):
                continue
            if not rel.startswith("results" + os.sep):
                # files saved by save_result() are already in results/; copy the rest
                dst = os.path.join(COLLECTED, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
            found.append((rel, src, ext))

    found.sort()
    out = [f"# MediRAG results summary",
           f"Generated: {datetime.now().isoformat(timespec='seconds')}",
           f"Files found: {len(found)}", ""]
    current = None
    for rel, src, ext in found:
        folder = os.path.dirname(rel) or "(project root)"
        if folder != current:
            out += ["", f"## {folder}"]
            current = folder
        mtime = datetime.fromtimestamp(os.path.getmtime(src)).strftime("%Y-%m-%d %H:%M")
        out += ["", f"### {os.path.basename(rel)}",
                f"Original: `{rel}`  |  Last modified: {mtime}", "",
                describe(src, ext)]
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "SUMMARY.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"Collected {len(found)} files into results/collected/")
    print("Summary written to results/SUMMARY.md")


if __name__ == "__main__":
    main()