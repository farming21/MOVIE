#!/usr/bin/env python3
import html, json, os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "videos.json")
TEMPLATES = os.path.join(BASE, "templates")
OUT = os.path.join(BASE, "videos")
SITE_URL = "https://farming21.github.io/movie"
LEGACY_SITE = "https://farming21.github.io/indonesia"
DEFAULT_COVER = "assets/img/no-cover.svg"
VALID_CATEGORIES = ("indonesia", "papua", "barat")

def load():
    with open(DATA, encoding="utf-8") as f:
        videos = json.load(f)
    if not isinstance(videos, list):
        raise ValueError("videos.json harus berupa array")
    for i, v in enumerate(videos):
        for k in ("slug","judul","driveId","tanggal","deskripsi","kategori"):
            if not v.get(k):
                raise ValueError(f"Video {i} kekurangan field {k}")
        if v["kategori"] not in VALID_CATEGORIES:
            raise ValueError(f"Kategori tidak valid: {v['kategori']}")
        v.setdefault("jam", "00:00")
    return videos

def pub_dt(v):
    raw = f"{v.get('tanggal','')}T{v.get('jam','00:00')}"
    try:
        return datetime.strptime(raw, "%Y-%m-%dT%H:%M")
    except ValueError:
        try:
            return datetime.strptime(v.get("tanggal",""), "%Y-%m-%d")
        except ValueError:
            return datetime.min

def display_dt(v):
    d = pub_dt(v)
    return d.strftime("%d-%m-%Y %H:%M") if d != datetime.min else f"{v.get('tanggal','-')} {v.get('jam','00:00')}"

def esc(s):
    return html.escape(str(s), quote=True)

def cover_path(v, detail=False):
    cover = str(v.get("cover") or "").strip() or DEFAULT_COVER
    if cover.startswith(("http://","https://")):
        return cover
    local = os.path.join(BASE, cover.lstrip("/"))
    if os.path.exists(local):
        return ("../" if detail else "") + cover.lstrip("/")
    return f"{LEGACY_SITE}/{cover.lstrip('/')}"

def absolute_cover(v):
    cover = str(v.get("cover") or "").strip() or DEFAULT_COVER
    if cover.startswith(("http://","https://")):
        return cover
    local = os.path.join(BASE, cover.lstrip("/"))
    if os.path.exists(local):
        return f"{SITE_URL}/{cover.lstrip('/')}"
    return f"{LEGACY_SITE}/{cover.lstrip('/')}"

def card(v):
    slug, title, cat = v["slug"], v["judul"], v["kategori"]
    return f'''<a href="videos/{esc(slug)}.html" class="video-card" data-category="{esc(cat)}">
<img src="{esc(cover_path(v))}" alt="{esc(title)}" loading="lazy">
<div class="card-body"><h3>{esc(title)}</h3>
<p style="color:#64748b;font-size:.85rem;margin-bottom:.5rem;">{esc(display_dt(v))}</p>
<span class="badge">{esc(cat)}</span></div></a>'''

def related_card(v):
    slug, title, cat = v["slug"], v["judul"], v["kategori"]
    return f'''<a href="{esc(slug)}.html" class="related-card">
<div class="related-thumb"><img src="{esc(cover_path(v, True))}" alt="{esc(title)}" loading="lazy"><span class="related-play" aria-hidden="true">▶</span></div>
<div class="related-body"><h3>{esc(title)}</h3><p>{esc(display_dt(v))}</p><span class="badge">{esc(cat)}</span></div></a>'''

def main():
    videos = load()
    ordered = sorted(videos, key=pub_dt, reverse=True)
    with open(os.path.join(TEMPLATES, "index.html"), encoding="utf-8") as f:
        it = f.read()
    cards = "\n".join(card(v) for v in ordered) or '<p style="grid-column:1/-1;text-align:center">Belum ada video.</p>'
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(it.replace("{{ VIDEO_CARDS }}", cards))

    os.makedirs(OUT, exist_ok=True)
    for fn in os.listdir(OUT):
        if fn.endswith(".html"):
            os.remove(os.path.join(OUT, fn))
    with open(os.path.join(TEMPLATES, "video.html"), encoding="utf-8") as f:
        vt = f.read()
    for v in videos:
        title, desc, drive, cat = v["judul"], v["deskripsi"], v["driveId"], v["kategori"]
        out = vt.replace("{{ JUDUL }}", esc(title)).replace("{{ DESKRIPSI }}", esc(desc))
        out = out.replace("{{ DRIVE_ID }}", esc(drive)).replace("{{ KATEGORI }}", esc(cat))
        out = out.replace("{{ TANGGAL }}", esc(display_dt(v))).replace("{{ COVER }}", esc(cover_path(v, True)))
        out = out.replace("{{ OG_COVER }}", esc(absolute_cover(v)))
        out = out.replace("{{ PAGE_URL }}", esc(f'{SITE_URL}/videos/{v["slug"]}.html'))
        rel = [x for x in ordered if x["slug"] != v["slug"]]
        parts = []
        for i, x in enumerate(rel, 1):
            parts.append(related_card(x))
            if i % 4 == 0 and i < len(rel):
                parts.append('<div class="related-ad-slot" aria-label="Iklan"><div class="related-ad-inner">\n<script>atOptions={"key":"6b78fdf35c5dd58ae54f80dbde15a0a7","format":"iframe","height":250,"width":300,"params":{}};</script>\n<script src="https://www.highrevenueformat.com/6b78fdf35c5dd58ae54f80dbde15a0a7/invoke.js"></script>\n</div></div>')
        out = out.replace("{{ RELATED_VIDEOS }}", "\n".join(parts) or '<p class="related-empty">Belum ada video lainnya.</p>')
        with open(os.path.join(OUT, f'{v["slug"]}.html'), "w", encoding="utf-8") as f:
            f.write(out)
    print(f"Generated {len(videos)} videos")

if __name__ == "__main__":
    main()
