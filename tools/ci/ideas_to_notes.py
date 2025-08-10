#!/usr/bin/env python3
import csv, sys, re, pathlib

"""
Input:
  - CSV: charter_valuable_ideas_missing_in_outline.csv
    必須列: id, chapter, title, summary (列名は柔軟に拾う)
  - MD : outline/publisher_outline_2025-08-06.md

Output:
  - outline/publisher_outline_2025-08-06.notes.md
    （元本文は変更せず、各章末に "### Notes (Charter Ideas)" を追補）
"""

CSV_PATH = "charter/charter_valuable_ideas_missing_in_outline.csv"
MD_IN    = "outline/publisher_outline_2025-08-06.md"
MD_OUT   = "outline/publisher_outline_2025-08-06.notes.md"

def pick(row, keys):
    for k in keys:
        if k in row and row[k].strip():
            return row[k].strip()
    return ""

def load_ideas():
    ideas_by_ch = {}
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            ch   = pick(r, ["chapter","chap","ch","chapter_id"])
            iid  = pick(r, ["id","idea_id","#"])
            ttl  = pick(r, ["title","idea","name"])
            summ = pick(r, ["summary","desc","description","value"])
            if not ch or not ttl:
                continue
            ideas_by_ch.setdefault(ch, []).append((iid, ttl, summ))
    return ideas_by_ch

def split_by_chapters(md):
    # 章見出し "## Chapter N:" で分割（アウトラインの既存形式に合わせる）
    parts = re.split(r'(\n## Chapter\s+\d+:[^\n]*\n)', md)
    # parts: ["前書き", "見出し1", "本文1", "見出し2", "本文2", ...]
    chunks = []
    if parts[0]:
        chunks.append(("", parts[0]))
    for i in range(1, len(parts), 2):
        header = parts[i]
        body   = parts[i+1] if i+1 < len(parts) else ""
        m = re.search(r'## Chapter\s+(\d+):', header)
        ch_id = m.group(1) if m else ""
        chunks.append((ch_id, header + body))
    return chunks

def append_notes(ch_body, ideas):
    if not ideas:
        return ch_body
    lines = []
    lines.append(ch_body.rstrip())
    lines.append("\n### Notes (Charter Ideas)\n")
    for iid, ttl, summ in ideas:
        line = f"- **{ttl}**"
        if iid:  line = f"- **[{iid}] {ttl}**"
        if summ: line += f": {summ}"
        lines.append(line)
    lines.append("")  # trailing newline
    return "\n".join(lines)

def main():
    md_text = pathlib.Path(MD_IN).read_text(encoding="utf-8")
    ideas   = load_ideas()
    out_chunks = []
    for ch_id, chunk in split_by_chapters(md_text):
        if ch_id and ch_id in ideas:
            out_chunks.append( append_notes(chunk, ideas[ch_id]) )
        else:
            out_chunks.append(chunk)
    pathlib.Path(MD_OUT).write_text("".join(out_chunks), encoding="utf-8")
    print(f"OK: wrote {MD_OUT}")

if __name__ == "__main__":
    main()
