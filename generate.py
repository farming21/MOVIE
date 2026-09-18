#!/usr/bin/env python3
import html,json,os
from datetime import datetime
BASE=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(BASE,"videos.json"); TEMPLATES=os.path.join(BASE,"templates"); OUT=os.path.join(BASE,"videos")
SITE_URL="https://farming21.github.io/MOVIE"; LEGACY="https://farming21.github.io/indonesia"; DEFAULT="assets/img/no-cover.svg"; CATS=("indonesia","papua","barat")
def load():
    with open(DATA,encoding="utf-8") as f:v=json.load(f)
    if not isinstance(v,list): raise ValueError("videos.json harus array")
    for i,x in enumerate(v):
        for k in ("slug","judul","driveId","tanggal","deskripsi","kategori"):
            if not x.get(k): raise ValueError(f"Video {i}: field {k} kosong")
        if x["kategori"] not in CATS: raise ValueError("Kategori tidak valid: "+str(x["kategori"]))
        x.setdefault("jam","00:00")
    return v
def dt(v):
    try:return datetime.strptime(f'{v.get("tanggal","")}T{v.get("jam","00:00")}','%Y-%m-%dT%H:%M')
    except ValueError:
        try:return datetime.strptime(v.get("tanggal",""),'%Y-%m-%d')
        except ValueError:return datetime.min
def dtext(v): return dt(v).strftime("%d-%m-%Y %H:%M") if dt(v)!=datetime.min else f'{v.get("tanggal","-")} {v.get("jam","00:00")}'
def esc(s):return html.escape(str(s),quote=True)
def cover(v,detail=False):
    c=str(v.get("cover") or "").strip() or DEFAULT
    if c.startswith(("http://","https://")):return c
    local=os.path.join(BASE,c.lstrip("/"))
    if os.path.exists(local):return ("../" if detail else "")+c.lstrip("/")
    return LEGACY+"/"+c.lstrip("/")
def og(v):
    c=str(v.get("ogCover") or "").strip()
    if c.startswith(("http://","https://")):return c
    if not c:c=f'covers/og/{v["slug"]}.jpg'
    local=os.path.join(BASE,c.lstrip("/"))
    return (SITE_URL+"/"+c.lstrip("/")) if os.path.exists(local) else LEGACY+"/"+c.lstrip("/")
def card(v):
    return f'<a href="videos/{esc(v["slug"])}.html" class="video-card" data-category="{esc(v["kategori"])}"><img src="{esc(cover(v))}" alt="{esc(v["judul"])}" loading="lazy"><div class="card-body"><h3>{esc(v["judul"])}</h3><p class="meta-date">{esc(dtext(v))}</p><span class="badge">{esc(v["kategori"])}</span></div></a>'
def rel(v):
    return f'<a href="{esc(v["slug"])}.html" class="related-card"><div class="related-thumb"><img src="{esc(cover(v,True))}" alt="{esc(v["judul"])}" loading="lazy"><span class="related-play">▶</span></div><div class="related-body"><h3>{esc(v["judul"])}</h3><p>{esc(dtext(v))}</p><span class="badge">{esc(v["kategori"])}</span></div></a>'
def main():
    vs=load(); ordered=sorted(vs,key=dt,reverse=True)
    it=open(os.path.join(TEMPLATES,"index.html"),encoding="utf-8").read()
    open(os.path.join(BASE,"index.html"),"w",encoding="utf-8").write(it.replace("{{ VIDEO_CARDS }}","\n".join(card(v) for v in ordered)))
    os.makedirs(OUT,exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".html"):os.remove(os.path.join(OUT,f))
    vt=open(os.path.join(TEMPLATES,"video.html"),encoding="utf-8").read()
    for v in vs:
        out=vt.replace("{{ JUDUL }}",esc(v["judul"])).replace("{{ DESKRIPSI }}",esc(v["deskripsi"])).replace("{{ DRIVE_ID }}",esc(v["driveId"])).replace("{{ KATEGORI }}",esc(v["kategori"])).replace("{{ TANGGAL }}",esc(dtext(v))).replace("{{ COVER }}",esc(cover(v,True))).replace("{{ OG_COVER }}",esc(og(v))).replace("{{ PAGE_URL }}",esc(f'{SITE_URL}/videos/{v["slug"]}.html'))
        out=out.replace("{{ RELATED_VIDEOS }}","\n".join(rel(x) for x in ordered if x["slug"]!=v["slug"]) or '<p>Belum ada video lainnya.</p>')
        open(os.path.join(OUT,v["slug"]+".html"),"w",encoding="utf-8").write(out)
    print("Generated",len(vs),"videos")
if __name__=="__main__":main()
