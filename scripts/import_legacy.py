#!/usr/bin/env python3
"""One-time migration helper for the public farming21/indonesia videos.json.
It does not download or inspect cover files. Legacy cover paths remain referenced
to the old public site until a new cover is uploaded through admin/.
"""
import json, urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/farming21/indonesia/main/videos.json"
OUT = Path(__file__).resolve().parents[1] / "videos.json"

with urllib.request.urlopen(URL, timeout=30) as r:
    data = json.load(r)

for v in data:
    v.setdefault("jam", "00:00")

OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Imported {len(data)} videos into {OUT}")
