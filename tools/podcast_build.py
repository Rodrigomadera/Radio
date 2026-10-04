"""Builds everything the podcast needs to be shared from podcast/episodios.json:
a share page per episode (preview card for Facebook/WhatsApp), chapters, RSS feeds (all + per show), M3U lists
and the covers. Episodes whose `disponible` is still in the future are left out until the next run.

    python3 tools/podcast_build.py            # then commit + push
"""
import html
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

SITE = 'https://rodrigomadera.com'
ROOT = Path(__file__).resolve().parent.parent
POD = ROOT / 'podcast'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
COLORS = {'rosa': '#FF3B6B', 'cian': '#2FE3C8', 'ambar': '#F5A623'}
SPOTIFY = 'https://open.spotify.com/show/6IsvrUUjdikxReJRv9Vgd2'
SHOWS = {  # slug → description for the feed
    'hypeando': ('Hypeando', 'El impulso disruptivo: lo que se viralizó, tecnología, estrenos y chismecito internacional. '
                             'Jueves 8:00 pm por Impulso FM 107.3.'),
    'cronicas-migajeras': ('Crónicas Migajeras', 'Porque alguien tenía que ponerle música a lo que no dijiste. Amor, '
                                                 'desamor y dedicatorias. Viernes 8:00 pm por Impulso FM 107.3.'),
    'sabado-de-rush': ('Sábado de Rush', 'Electrónica y toda la cultura que la rodea. Sábado 8:00 pm por Impulso FM 107.3.'),
}
e_ = html.escape


def clock(s):
    s = int(s)
    return f'{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}' if s >= 3600 else f'{s // 60}:{s % 60:02d}'


def fecha_larga(f):
    d = datetime.fromisoformat(f)
    dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
             'noviembre', 'diciembre']
    return f'{dias[d.weekday()]} {d.day} de {meses[d.month - 1]} de {d.year}'


def cover(slug, name, color, w, h, out):
    """Show cover rendered by headless Chrome so it uses the site's fonts."""
    if out.exists():
        return
    big = min(w, h)
    page = f'''<html><head><link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112,900&family=Space+Grotesk:wght@500;700&display=block" rel="stylesheet">
<style>*{{margin:0}}body{{width:{w}px;height:{h}px;background:#09090B;color:#F2EFE9;font-family:'Space Grotesk';position:relative;overflow:hidden}}
.top{{position:absolute;left:0;right:0;top:0;height:{big * .02:.0f}px;background:{color}}}
h1{{position:absolute;left:{big * .08:.0f}px;bottom:{big * .26:.0f}px;font-family:Archivo;font-stretch:112%;font-weight:900;
font-size:{min(big * .2, w * .84 / (.74 * max(map(len, name.split())))):.0f}px;line-height:.98;max-width:{w * .86:.0f}px}}
h1 span{{background:linear-gradient(transparent 66%,{color} 66% 97%,transparent 97%);-webkit-box-decoration-break:clone}}
p{{position:absolute;left:{big * .08:.0f}px;bottom:{big * .1:.0f}px;font-size:{w * .03:.0f}px;letter-spacing:.12em;text-transform:uppercase;font-weight:700}}
p b{{color:{color}}}</style></head><body><div class="top"></div><h1><span>{e_(name)}</span></h1>
<p>Rodrigo Madera · <b>Impulso FM 107.3</b></p></body></html>'''
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(page)
    subprocess.run([CHROME, '--headless=new', '--hide-scrollbars', '--virtual-time-budget=4000', f'--window-size={w},{h}',
                    f'--screenshot={out}', f'file://{f.name}'], capture_output=True, check=True)


def episode_card(e, color, out):
    """Facebook/WhatsApp card for one episode: show name, episode and a big play button."""
    if out.exists():
        return
    page = f'''<html><head><link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112,900&family=Space+Grotesk:wght@500;700&display=block" rel="stylesheet">
<style>*{{margin:0}}body{{width:1200px;height:630px;background:#09090B;color:#F2EFE9;font-family:'Space Grotesk';position:relative;overflow:hidden}}
.top{{position:absolute;left:0;right:0;top:0;height:12px;background:{color}}}
.k{{position:absolute;left:60px;top:70px;font-size:24px;letter-spacing:.2em;text-transform:uppercase;font-weight:700;color:{color}}}
h1{{position:absolute;left:60px;top:120px;width:700px;font-family:Archivo;font-stretch:112%;font-weight:900;font-size:{min(118, 700 / (.74 * max(map(len, e['show'].split())))):.0f}px;line-height:1}}
h1 span{{background:linear-gradient(transparent 66%,{color} 66% 97%,transparent 97%);-webkit-box-decoration-break:clone}}
.ep{{position:absolute;left:60px;bottom:120px;font-size:40px;font-weight:700}}
.f{{position:absolute;left:60px;bottom:66px;font-size:24px;color:#C6C3BE}}
.play{{position:absolute;right:90px;top:50%;transform:translateY(-50%);width:230px;height:230px;border-radius:50%;background:{color};
box-shadow:0 0 0 22px rgba(255,255,255,.06)}}
.play:after{{content:"";position:absolute;left:88px;top:62px;border-style:solid;border-width:53px 0 53px 88px;border-color:transparent transparent transparent #09090B}}
.lbl{{position:absolute;right:90px;width:230px;text-align:center;bottom:66px;font-size:24px;letter-spacing:.2em;font-weight:700;text-transform:uppercase}}
</style></head><body><div class="top"></div><div class="k">Escucha ahora</div><h1><span>{e_(e['show'])}</span></h1>
<div class="ep">{e_(e['ep'])}</div><div class="f">{e_(fecha_larga(e['fecha']).capitalize())} · Impulso FM 107.3</div>
<div class="play"></div><div class="lbl">Dale play</div></body></html>'''
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(page)
    subprocess.run([CHROME, '--headless=new', '--hide-scrollbars', '--virtual-time-budget=4000', '--window-size=1200,630',
                    f'--screenshot={out}', f'file://{f.name}'], capture_output=True, check=True)


def main():
    now = datetime.now(timezone.utc)
    eps = json.loads((POD / 'episodios.json').read_text())
    live = [e for e in eps if not e.get('disponible') or datetime.fromisoformat(e['disponible']) <= now]
    (POD / 'img').mkdir(exist_ok=True)
    for slug, (name, _) in SHOWS.items():
        color = COLORS[next((e['color'] for e in eps if e['slug'] == slug), 'rosa')]
        cover(slug, name, color, 1400, 1400, POD / 'img' / f'{slug}.png')
        cover(slug, name, color, 1200, 630, POD / 'img' / f'{slug}-og.png')
    cover('podcast', 'Rodrigo Madera', COLORS['rosa'], 1400, 1400, POD / 'img' / 'podcast.png')

    for e in live:
        name = e['show']
        title = f"{name} {e['ep']}"
        page = f"{SITE}/podcast/{e['slug']}/{e['num']}/"
        desc = f"Transmitido el {fecha_larga(e['fecha'])} por Impulso FM 107.3 · {clock(e['dur'])}. Escúchalo completo aquí."
        card = f"{e['slug']}-{e['num']}-og.png"
        episode_card(e, COLORS[e['color']], POD / 'img' / card)
        d = POD / e['slug'] / str(e['num'])
        d.mkdir(parents=True, exist_ok=True)
        (d / 'index.html').write_text(f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>{e_(title)} · Rodrigo Madera</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e_(desc)}">
<link rel="canonical" href="{page}">
<meta property="og:type" content="music.radio_station"><meta property="og:site_name" content="Rodrigo Madera">
<meta property="og:locale" content="es_MX"><meta property="og:url" content="{page}">
<meta property="og:title" content="▶ {e_(title)}"><meta property="og:description" content="{e_(desc)}">
<meta property="og:image" content="{SITE}/podcast/img/{card}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="{e_(name)}" href="{SITE}/podcast/{e['slug']}/feed.xml">
<script>location.replace("/podcast/?ep={e['slug']}-{e['num']}" + location.search.replace("?", "&") + location.hash);</script>
</head><body style="background:#09090B;color:#F2EFE9;font-family:sans-serif;padding:40px">
<p><a style="color:#F2EFE9" href="/podcast/?ep={e['slug']}-{e['num']}">Escuchar {e_(title)}</a></p></body></html>
''', encoding='utf-8')
        (d / 'chapters.json').write_text(json.dumps(
            {'version': '1.2.0', 'chapters': [{'startTime': s, 'title': t} for s, t in e['ch']]},
            ensure_ascii=False, indent=1), encoding='utf-8')

    def feed(path, title, about, image, items, link):
        rows = []
        for e in sorted(items, key=lambda x: x['fecha'], reverse=True):
            t = f"{e['show']} {e['ep']}"
            pub = datetime.fromisoformat(e.get('disponible') or e['fecha'] + 'T21:00:00-05:00')
            notes = (f"Transmitido el {fecha_larga(e['fecha'])} por Impulso FM 107.3.\n\n"
                     + '\n'.join(f'{clock(s)} {c}' for s, c in e['ch'])
                     + f"\n\nEscúchalo en {SITE}/podcast/{e['slug']}/{e['num']}/")
            rows.append(f'''  <item>
   <title>{e_(t)}</title>
   <link>{SITE}/podcast/{e['slug']}/{e['num']}/</link>
   <guid isPermaLink="false">rodrigomadera-{e['slug']}-{e['temp']}-{e['num']}</guid>
   <pubDate>{format_datetime(pub)}</pubDate>
   <description>{e_(notes)}</description>
   <enclosure url="{e_(e['src'])}" length="{e['bytes']}" type="audio/mpeg"/>
   <itunes:duration>{e['dur']}</itunes:duration>
   <itunes:season>{e['temp']}</itunes:season><itunes:episode>{e['num']}</itunes:episode>
   <itunes:image href="{SITE}/podcast/img/{e['slug']}.png"/>
   <podcast:chapters url="{SITE}/podcast/{e['slug']}/{e['num']}/chapters.json" type="application/json+chapters"/>
  </item>''')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:podcast="https://podcastindex.org/namespace/1.0" xmlns:atom="http://www.w3.org/2005/Atom">
 <channel>
  <title>{e_(title)}</title>
  <link>{link}</link>
  <atom:link href="{SITE}/{path.relative_to(ROOT).as_posix()}" rel="self" type="application/rss+xml"/>
  <description>{e_(about)}</description>
  <language>es-mx</language>
  <itunes:author>Rodrigo Madera</itunes:author>
  <itunes:image href="{image}"/>
  <image><url>{image}</url><title>{e_(title)}</title><link>{link}</link></image>
  <itunes:category text="Music"/>
  <itunes:explicit>false</itunes:explicit>
  <itunes:block>Yes</itunes:block>
  <podcast:locked>yes</podcast:locked>
{chr(10).join(rows)}
 </channel>
</rss>
''', encoding='utf-8')

    def m3u(path, items):
        path.write_text('#EXTM3U\n' + ''.join(f"#EXTINF:{e['dur']},Rodrigo Madera - {e['show']} {e['ep']}\n{e['src']}\n"
                                              for e in sorted(items, key=lambda x: x['fecha'], reverse=True)),
                        encoding='utf-8')

    feed(POD / 'feed.xml', 'Rodrigo Madera · Impulso FM 107.3',
         'Hypeando, Crónicas Migajeras y Sábado de Rush completos, con Rodrigo Madera.',
         f'{SITE}/podcast/img/podcast.png', live, f'{SITE}/podcast/')
    m3u(POD / 'lista.m3u', live)
    for slug, (name, about) in SHOWS.items():
        mine = [e for e in live if e['slug'] == slug]
        feed(POD / slug / 'feed.xml', f'{name} · Rodrigo Madera', about, f'{SITE}/podcast/img/{slug}.png', mine,
             f'{SITE}/podcast/')
        m3u(POD / slug / 'lista.m3u', mine)
    print('publicados:', ', '.join(f"{e['show']} {e['ep']}" for e in live))
    print('pendientes:', ', '.join(f"{e['show']} {e['ep']} ({e['disponible']})" for e in eps if e not in live) or '—')


if __name__ == '__main__':
    main()
