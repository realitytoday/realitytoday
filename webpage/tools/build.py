#!/usr/bin/env python3
"""Static site builder: python tools/build.py  (run from anywhere).
Reads content/*.md, writes HTML next to them (index.html, de/, projects/...)."""
import re, html
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parent.parent
BLUEPRINT = "https://github.com/realitytoday/home-information-screen-blueprint"
GITHUB = "https://github.com/realitytoday"
VF_BLUEPRINT = "https://github.com/realitytoday/vps-fleet"
VF_CODE = "https://github.com/realitytoday/vps-fleet-tui"
def _vf_preview():
    """Terminal preview for the vps-fleet card, coloured like the real TUI (Lip Gloss palette)."""
    def sp(text, color, bold=False):
        st = f"color:{color}" + (";font-weight:700" if bold else "")
        return f'<span style="{st}">{html.escape(text)}</span>'
    def mix(a, b, t):
        pa = [int(a[i:i+2], 16) for i in (1, 3, 5)]; pb = [int(b[i:i+2], 16) for i in (1, 3, 5)]
        return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(pa, pb))
    def bar(pct, n=4):
        filled = round(pct / 100 * n)
        out = ""
        for i in range(n):
            if i < filled:
                out += sp("█", mix("#5A56E0", "#EE6FF8", i / max(1, n - 1)))
            else:
                out += sp("░", "#4e5a85")
        return out
    def pct(v):
        return sp(f"{v:>3}%", "#ff5f5f" if v >= 90 else "#cfe9ff")
    CY, LIME, GREEN, GRAY = "#00d7ff", "#d7ff00", "#00ff00", "#8c97c2"
    rows = [("▌web-1", LIME, True, "● online", GREEN, 82, 97), (" db-1 ", "#cfe9ff", False, "● online", GREEN, 12, 41),
            (" vpn-1", "#cfe9ff", False, "● online", GREEN, 8, 23)]
    out = [sp("vps-fleet v0.1.0", CY, True) + sp(" · default", GRAY), "",
           sp("NAME      STATUS    CPU       MEM", CY, True)]
    for name, nc, nb, st, sc, cpu, mem in rows:
        out.append(sp(f"{name:<10}", nc, nb) + sp(f"{st:<10}", sc) + bar(cpu) + pct(cpu) + "  " + bar(mem) + pct(mem))
    out += ["", sp("enter", LIME) + sp(" dash  ", GRAY) + sp("t", LIME) + sp(" top  ", GRAY) + sp("s", LIME) + sp(" ssh  ", GRAY) + sp("f", LIME) + sp(" files", GRAY)]
    return "\n".join(out)

VF_PREVIEW = _vf_preview()
SHOTS = ["screen-idle", "screen-calendar", "screen-order-dialog", "screen-weather",
         "screen-tasks", "screen-orders", "screen-sensors", "screen-notes"]

L = {
 "en": dict(
  lang="en", home="/", other="/de/", other_label="DE", projects="Projects", about="Approach",
  title="Reality Today – projects, ideas and blueprints built with AI",
  desc="Projects, ideas and blueprints built with AI as a real partner – from first idea to working product. Architecture and prompts included.",
  h1="It is <span>reality</span> today.",
  lead="For years we watched AI get better and better. Today it has arrived in our everyday life as developers. It isn't a vision of the future anymore.",
  intro=["Reality Today is a collection of projects, ideas and blueprints that came out of this new way of building: from a first idea to a working product, with AI as a real partner in the process. Here you'll find what I built, how it works, and the architecture and prompts behind it, so you can build it yourself.",
         "What you find here are recent projects, or renewals of old ones, realized with artificial intelligence in a few days or weekends, often in the evening after work."],
  projects_h="Projects", more="Read the guide", soon_t="More on the way", soon_p="Weekend-sized projects: developer tooling, AI agents and everyday tools for home and family.",
  card_t="Home Information Screen", card_p="A calm wall dashboard for the family on a Raspberry Pi: calendar, weather, who is home, chores, sensors and sticky notes. A blueprint plus the prompts – not the code.",
  tags=["Raspberry Pi","Go","Svelte","AI agents"],
  approach_h="How these projects work",
  principles=[("Blueprint, not codebase","Your setup differs from mine. So I share the idea, architecture, design rules and the prompts that build each part."),
              ("AI as a real partner","Coding agents like Claude, GitHub Copilot, JetBrains Junie or Mistral Vibe build your own instance from the material."),
              ("Honest about gaps","Every project lists what is not finished, so you never rely on something that doesn't exist.")],
  proj_path="projects/home-information-screen/", proj_title="Home Information Screen",
  gallery="Screens of the finished dashboard. All names, appointments and notes are invented demo data; the UI is German because the household is.",
  cta_h="Get the blueprint", cta_p="Architecture, design system, hardware notes, lessons learned, all prompts and reference files on GitHub.",
  cta_b="Open on GitHub", other_page="Deutsche Version dieser Anleitung", home_b="All projects",
  guide_desc="Build a calm wall dashboard with a Raspberry Pi, a touchscreen and an AI coding agent. A blueprint and the prompts, no code to download.",
  llm_t="Which AI model and agent?", llm_p="Choosing a model for the blueprints: why Opus-class models give the best results, where mid-tier is enough, and tips for Mistral Vibe and other agents.",
  llm_tags=["Claude Opus","Mistral Vibe","Agent tips"], llm_note="Not every model can do the same. Read which AI model and agent to use before you start.",
  vf_t="VPS Fleet", vf_p="Your whole server fleet in one terminal window: health, processes, services and files for all your servers over plain SSH, with nothing installed on them. The prompts plus the finished Go code.",
  vf_tags=["Go","SSH","Terminal UI","AI agents"], vf_path="projects/vps-fleet/",
  vf_desc="A keyboard-driven terminal cockpit for a fleet of Linux servers over plain SSH. Build it with an AI coding agent from the prompts, or use the finished Go code.",
  vf_cta_h="Get the blueprint and the code", vf_cta_p="The prompts, architecture, key map and lessons learned are in the blueprint repo; the finished Go implementation is in the code repo.",
  vf_cta_b="Blueprint on GitHub", vf_code_b="Code on GitHub",
  llm_h="Guide", contact="Contact", license="Content: CC BY 4.0 unless stated otherwise in the repos.", aria="Language"),
 "de": dict(
  lang="de", home="/de/", other="/", other_label="EN", projects="Projekte", about="Ansatz",
  title="Reality Today – Projekte, Ideen und Blueprints, gebaut mit KI",
  desc="Projekte, Ideen und Blueprints, gebaut mit KI als echtem Partner – von der ersten Idee bis zum funktionierenden Produkt. Mit Architektur und Prompts.",
  h1="Es ist <span>Realität</span> – heute.",
  lead="Jahrelang haben wir zugesehen, wie KI immer besser wird. Heute ist sie im Alltag von Entwicklerinnen und Entwicklern angekommen. Das ist keine Zukunftsvision mehr.",
  intro=["Reality Today ist eine Sammlung von Projekten, Ideen und Blueprints, die aus dieser neuen Art zu bauen entstanden sind: von der ersten Idee bis zum funktionierenden Produkt, mit KI als echtem Partner im Prozess. Hier findest du, was ich gebaut habe, wie es funktioniert und welche Architektur und Prompts dahinterstecken, damit du es selbst nachbauen kannst.",
         "Es sind aktuelle Projekte oder Neuauflagen alter Projekte, die mit künstlicher Intelligenz in wenigen Tagen oder an Wochenenden entstanden sind, oft abends nach der Arbeit."],
  projects_h="Projekte", more="Zur Anleitung", soon_t="Weitere folgen", soon_p="Projekte in Wochenendgröße: Entwickler-Werkzeuge, KI-Agenten und Alltagshelfer für Haus und Familie.",
  card_t="Home Information Screen", card_p="Ein ruhiges Wand-Dashboard für die Familie auf dem Raspberry Pi: Kalender, Wetter, wer zu Hause ist, Aufgaben, Sensoren und Notizzettel. Ein Bauplan samt Prompts – ohne Code.",
  tags=["Raspberry Pi","Go","Svelte","KI-Agenten"],
  approach_h="So entstehen die Projekte",
  principles=[("Bauplan statt Code","Dein Setup ist anders als meins. Ich teile deshalb Idee, Architektur, Design-Regeln und die Prompts, die jedes Teil bauen."),
              ("KI als echter Partner","Coding-Agenten wie Claude, GitHub Copilot, JetBrains Junie oder Mistral Vibe bauen aus dem Material deine eigene Instanz."),
              ("Ehrlich über Lücken","Jedes Projekt nennt, was noch fehlt, damit du dich nicht auf etwas verlässt, das es nicht gibt.")],
  proj_path="projekte/home-information-screen/", proj_title="Home Information Screen",
  gallery="Bildschirme des fertigen Dashboards. Alle Namen, Termine und Notizen sind erfundene Demodaten.",
  cta_h="Den Bauplan holen", cta_p="Architektur, Design-System, Hardware-Notizen, Lessons Learned, alle Prompts und Referenzdateien auf GitHub.",
  cta_b="Auf GitHub öffnen", other_page="English version of this guide", home_b="Alle Projekte",
  guide_desc="Ein ruhiges Wand-Dashboard mit Raspberry Pi, Touchscreen und KI-Coding-Agent bauen. Bauplan und Prompts, kein Code zum Herunterladen.",
  llm_t="Welches KI-Modell und welcher Agent?", llm_p="Modellwahl für die Blueprints: warum Opus-Klasse die besten Ergebnisse liefert, wo die Mittelklasse reicht, und Tipps für Mistral Vibe und andere Agenten.",
  llm_tags=["Claude Opus","Mistral Vibe","Agent-Tipps"], llm_note="Nicht jedes Modell kann dasselbe. Lies vor dem Start, welches KI-Modell und welcher Agent geeignet ist.",
  vf_t="VPS Fleet", vf_p="Die ganze Server-Flotte in einem Terminalfenster: Zustand, Prozesse, Dienste und Dateien aller Server über normales SSH, ohne etwas auf ihnen zu installieren. Die Prompts und dazu der fertige Go-Code.",
  vf_tags=["Go","SSH","Terminal-UI","KI-Agenten"], vf_path="projekte/vps-fleet/",
  vf_desc="Ein tastaturgesteuertes Terminal-Cockpit für eine Flotte von Linux-Servern über normales SSH. Mit einem KI-Coding-Agenten aus den Prompts bauen oder den fertigen Go-Code nutzen.",
  vf_cta_h="Bauplan und Code holen", vf_cta_p="Prompts, Architektur, Tastenbelegung und Lessons Learned liegen im Blueprint-Repo, die fertige Go-Implementierung im Code-Repo.",
  vf_cta_b="Blueprint auf GitHub", vf_code_b="Code auf GitHub",
  llm_h="Anleitung", contact="Kontakt", license="Inhalte: CC BY 4.0, sofern in den Repos nicht anders angegeben.", aria="Sprache"),
}

def rel(depth): return "../" * depth if depth else "./"

def layout(lang, depth, title, desc, body, alt_path, path):
    t = L[lang]; r = rel(depth)
    other = "en" if lang == "de" else "de"
    # alt_path: path of the other-language page relative to site root
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://reality-today.de/assets/img/social-preview.jpg">
<link rel="alternate" hreflang="{other}" href="{r}{alt_path}">
<link rel="icon" type="image/png" href="{r}assets/favicon.png">
<link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">
<link rel="stylesheet" href="{r}assets/style.css">
</head>
<body>
<header class="site"><div class="wrap">
<a class="brand" href="{r}{'de/' if lang=='de' else ''}"><img src="{r}assets/img/logo.png" alt="" width="40" height="40"><span>Reality Today</span></a>
<nav class="site" aria-label="Main">
<a href="{r}{'de/' if lang=='de' else ''}#projects">{t['projects']}</a>
<a class="hide-s" href="{r}{'de/' if lang=='de' else ''}#approach">{t['about']}</a>
<a class="hide-s" href="{GITHUB}">GitHub</a>
<a class="lang" href="{r}{alt_path}" hreflang="{other}" lang="{other}" aria-label="{t['aria']}">{t['other_label']}</a>
</nav></div></header>
<main>
{body}
</main>
<footer class="site"><div class="wrap">
<span>© Reality Today · {t['license']}</span>
<span><a href="{GITHUB}">GitHub</a></span>
</div></footer>
</body></html>
"""

def home(lang):
    t = L[lang]; depth = 1 if lang == "de" else 0; r = rel(depth)
    proj = f"{r}{t['proj_path']}" if lang == "en" else f"{t['proj_path']}"
    thumbs = "".join(f'<img src="{r}assets/img/{s}.webp" alt="" loading="lazy">' for s in SHOTS[:3])
    tags = "".join(f"<span>{x}</span>" for x in t["tags"])
    llm_href = (r + "guides/choosing-an-llm/") if lang == "en" else "anleitungen/llm-auswahl/"
    vf_href = (r + t["vf_path"]) if lang == "en" else t["vf_path"]
    vf_tags = "".join(f"<span>{x}</span>" for x in t["vf_tags"])
    body = f"""<section class="hero"><div class="wrap">
<h1>{t['h1']}</h1>
<p class="lead">{t['lead']}</p>
{''.join(f'<p class="narrow" style="margin-left:0">{p}</p>' for p in t['intro'])}
<a class="btn" href="#projects">{t['projects_h']}</a><a class="btn alt" href="{GITHUB}">GitHub</a>
</div></section>
<section id="projects"><div class="wrap">
<h2>{t['projects_h']}</h2>
<div class="grid">
<a class="card" href="{proj}"><div class="thumb">{thumbs}</div><div class="body">
<h3>{t['card_t']}</h3><p>{t['card_p']}</p><div class="tags">{tags}</div></div></a>
<a class="card" href="{vf_href}"><div class="thumb term"><pre>{VF_PREVIEW}</pre></div><div class="body">
<h3>{t['vf_t']}</h3><p>{t['vf_p']}</p><div class="tags">{vf_tags}</div></div></a>
<a class="card guide" href="{llm_href}"><div class="body" style="border-top:6px solid var(--pink)">
<h3>{t['llm_t']}</h3><p>{t['llm_p']}</p><div class="tags">{''.join(f"<span>{x}</span>" for x in t['llm_tags'])}</div></div></a>
<div class="card soon"><div><h3>{t['soon_t']}</h3><p>{t['soon_p']}</p></div></div>
</div></div></section>
<section id="approach"><div class="wrap">
<h2>{t['approach_h']}</h2>
<div class="principles">{''.join(f'<div><b>{a}</b>{b}</div>' for a,b in t['principles'])}</div>
</div></section>"""
    alt = "" if lang == "de" else "de/"
    return layout(lang, depth, t["title"], t["desc"], body, alt if alt else "./", "")

def md_to_html(text):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    return md.convert(text)

GUIDES = {
 "his": {"en": "projects/home-information-screen/", "de": "de/projekte/home-information-screen/",
         "src": "home-information-screen", "shots": True, "cta": True, "note": True,
         "desc": "guide_desc", "back": "projects"},
 "vf": {"en": "projects/vps-fleet/", "de": "de/projekte/vps-fleet/",
        "src": "vps-fleet", "shots": False, "cta": True, "note": False,
        "desc": "vf_desc", "back": "projects"},
 "llm": {"en": "guides/choosing-an-llm/", "de": "de/anleitungen/llm-auswahl/",
         "src": "llm-guidance", "shots": False, "cta": False, "note": False,
         "desc": "llm_p", "back": "projects"},
}

def guide(key, lang):
    t = L[lang]; g = GUIDES[key]
    path = g[lang]
    depth = len([x for x in path.split("/") if x])
    r = rel(depth)
    src = (ROOT / "content" / f"{g['src']}.{lang}.md").read_text(encoding="utf-8")
    lines = src.split("\n")
    title = re.sub(r"^#\s+", "", lines[0]).strip()
    sub = ""
    rest = []
    for ln in lines[1:]:
        if not sub and re.match(r"^\*[^*].*\*$", ln.strip()):
            sub = ln.strip().strip("*"); continue
        if re.match(r"^\*\*(Cover photo|Titelbild):\*\*", ln.strip()): continue
        if re.match(r"^\*(A German version|Die englische Version)", ln.strip()): continue
        if re.match(r"^\*Picture:", ln.strip()): continue
        rest.append(ln)
    text = "\n".join(rest)
    text = re.split(r"^## (?:Get the blueprint|Den Bauplan holen)\s*$", text, flags=re.M)[0]
    body_html = md_to_html(text)
    other = "en" if lang == "de" else "de"
    other_href = r + g[other]
    llm_href = r + GUIDES["llm"][lang]
    shots = ""
    if g["shots"]:
        imgs = "".join(f'<img src="{r}assets/img/{x}.webp" alt="" loading="lazy" width="270" height="480">' for x in SHOTS)
        shots = f'<div class="shots" role="group" aria-label="Screenshots">{imgs}</div><p class="sub" style="font-size:.9rem">{t["gallery"]}</p>'
    note = f'<p class="callout"><a href="{llm_href}">{t["llm_note"]}</a></p>' if g["note"] else ""
    if key == "vf":
        cta = f'<div class="cta"><h2>{t["vf_cta_h"]}</h2><p>{t["vf_cta_p"]}</p><a class="btn" href="{VF_BLUEPRINT}">{t["vf_cta_b"]}</a> <a class="btn alt" href="{VF_CODE}">{t["vf_code_b"]}</a></div>'
    else:
        cta = (f'<div class="cta"><h2>{t["cta_h"]}</h2><p>{t["cta_p"]}</p><a class="btn" href="{BLUEPRINT}">{t["cta_b"]}</a></div>' if g["cta"] else "")
    body = f"""<div class="wrap narrow"><article>
<p><a href="{r}{'de/' if lang=='de' else ''}#projects">← {t['home_b']}</a> · <a href="{other_href}" hreflang="{other}">{t['other_page']}</a></p>
<h1>{html.escape(title)}</h1>
<p class="sub">{html.escape(sub)}</p>
{note}{shots}
{body_html}
{cta}
</article></div>"""
    plain = re.sub(r"<[^>]+>", "", title)
    return layout(lang, depth, f"{plain} – Reality Today", t[g["desc"]], body, g[other], "")

def local_links(content):
    """Point folder links at their index.html, so the pages also work opened from disk (file://),
    where a browser shows a directory listing instead of the index. Web servers serve both the same."""
    def fix(m):
        path = m.group(2)
        return m.group(1) + (path + "index.html" if path.endswith("/") else path) + (m.group(3) or "") + '"'
    return re.sub(r'(<a\b[^>]*?\bhref=")((?!https?:|mailto:|#|/)[^"#]*/)(#[^"]*)?"', fix, content)

def write(path, content):
    if path != "404.html":  # the 404 page is served from any URL, it keeps its own root-relative links
        content = local_links(content)
    p = ROOT / path; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8"); print("wrote", path)

write("index.html", home("en"))
write("de/index.html", home("de"))
for _k, _g in GUIDES.items():
    for _l in ("en", "de"):
        write(_g[_l] + "index.html", guide(_k, _l))
write("404.html", layout("en", 0, "Not found – Reality Today", "Page not found",
  '<div class="wrap narrow hero"><h1>404</h1><p class="lead">This page does not exist. <a href="/">Back to the start</a> · <a href="/de/">Zur Startseite</a></p></div>', "de/", ""))

p = ROOT / "404.html"
p.write_text(p.read_text(encoding="utf-8").replace('"./assets/', '"/assets/').replace('href="./"', 'href="/"'), encoding="utf-8")
