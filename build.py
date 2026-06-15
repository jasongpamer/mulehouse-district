#!/usr/bin/env python3
import json, html, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load(name):
    with open(f"content/{name}.json") as f:
        return json.load(f)

def h(text):
    return html.escape(text).replace("·", "&middot;").replace("—", "&mdash;").replace("–", "&ndash;")

site = load("site")
hero = load("hero")
place = load("place")
engines = load("engines")
hotel = load("hotel")
gallery = load("gallery")
operators = load("operators")
cta = load("cta")

# Build engine cards
engine_cards = ""
for i, eng in enumerate(engines["engines"]):
    extra_style = ' style="display:flex;align-items:center;justify-content:center;"' if eng["number"] == "+" else ""
    wrap_open = "<div>" if eng["number"] == "+" else ""
    wrap_close = "</div>" if eng["number"] == "+" else ""
    engine_cards += f"""        <div class="engine-card"{extra_style}>
          {wrap_open}<div class="engine-number">{h(eng["number"])}</div>
          <p class="engine-name">{h(eng["name"])}</p>
          <p class="engine-desc">{h(eng["description"])}</p>{wrap_close}
        </div>\n"""

# Build hotel stats
hotel_stats = ""
for stat in hotel["stats"]:
    gold_style = ' style="color:var(--gold)"' if stat.get("gold") else ""
    hotel_stats += f"""            <div class="hotel-stat-row">
              <span class="hotel-stat-label">{h(stat["label"])}</span>
              <span class="hotel-stat-value"{gold_style}>{h(stat["value"])}</span>
            </div>\n"""

# Build gallery items
gallery_items = ""
for item in gallery["items"]:
    gallery_items += f"""        <div class="gallery-item">
          <img src=".{item['image']}" alt="{h(item['alt'])}">
          <div class="gallery-caption">
            <p class="gallery-caption-title">{h(item['title'])}</p>
            <p class="gallery-caption-sub">{h(item['caption'])}</p>
          </div>
        </div>\n"""

# Build operator cards
operator_cards = ""
for op in operators["operators"]:
    operator_cards += f"""        <div class="operator-card">
          <p class="operator-name">{h(op["name"])}</p>
          <p class="operator-role">{h(op["role"])}</p>
          <p class="operator-desc">{h(op["description"])}</p>
        </div>\n"""

# Build place stats
place_stats = ""
for stat in place["stats"]:
    gold_class = " gold" if stat.get("gold") else ""
    place_stats += f"""            <div class="stat">
              <div class="stat-number{gold_class}">{h(stat["value"])}</div>
              <p class="caption">{h(stat["label"])}</p>
            </div>\n"""

# Build CTA steps
cta_steps = ""
for i, step_text in enumerate(cta["steps"], 1):
    cta_steps += f"""        <div class="cta-step">
          <div class="cta-step-num">{i}</div>
          <p class="cta-step-text">{h(step_text)}</p>
        </div>\n"""

# Build CTA contacts
cta_contacts = ""
for contact in cta["contacts"]:
    cta_contacts += f"""        <div class="cta-contact-item">
          <p class="cta-contact-name">{h(contact["name"])}</p>
          <p class="cta-contact-role">{h(contact["role"])}</p>
        </div>\n"""

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{h(site["title"])}</title>
  <meta name="description" content="{h(site["description"])}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Display&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Archivo:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
  <style>
    *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

    :root {{
      --ink: #0A0703;
      --gold: #C9A34E;
      --cream: #F0E6D3;
      --cream-muted: rgba(240, 230, 211, 0.55);
      --oxblood: #8B3A2A;
      --gold-07: rgba(201, 163, 78, 0.7);
      --gold-04: rgba(201, 163, 78, 0.4);
      --gold-03: rgba(201, 163, 78, 0.3);
      --gold-025: rgba(201, 163, 78, 0.25);
    }}

    html {{ font-size: 16px; scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }}

    body {{
      background: var(--ink);
      color: var(--cream);
      font-family: 'Libre Caslon Text', Georgia, serif;
      line-height: 1.65;
      overflow-x: hidden;
    }}

    img {{ display: block; max-width: 100%; }}

    .eyebrow {{
      font-family: 'Archivo', sans-serif;
      font-weight: 500;
      font-size: 0.75rem;
      letter-spacing: 0.4em;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 1rem;
    }}

    .headline {{
      font-family: 'Libre Caslon Display', Georgia, serif;
      font-weight: 400;
      line-height: 1.1;
    }}

    .headline .turn {{ font-style: italic; color: var(--gold); }}

    .body-text {{
      color: var(--cream-muted);
      max-width: 860px;
      font-size: 1.05rem;
    }}

    .caption {{
      font-family: 'Archivo', sans-serif;
      font-weight: 500;
      font-size: 0.7rem;
      letter-spacing: 0.3em;
      text-transform: uppercase;
      color: var(--cream-muted);
    }}

    section {{ padding: 6rem 2rem; }}
    .container {{ max-width: 1200px; margin: 0 auto; }}

    nav {{
      position: fixed; top: 0; left: 0; right: 0; z-index: 100;
      padding: 1.25rem 2rem;
      display: flex; justify-content: space-between; align-items: center;
      transition: background 0.4s ease;
    }}
    nav.scrolled {{
      background: rgba(10,7,3,0.95);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--gold-04);
    }}
    .nav-logo {{
      font-family: 'Archivo', sans-serif; font-weight: 600;
      font-size: 0.65rem; letter-spacing: 0.35em;
      text-transform: uppercase; color: var(--cream); text-decoration: none;
    }}
    .nav-links {{ display: flex; gap: 2rem; list-style: none; }}
    .nav-links a {{
      font-family: 'Archivo', sans-serif; font-weight: 500;
      font-size: 0.65rem; letter-spacing: 0.2em;
      text-transform: uppercase; color: var(--cream-muted);
      text-decoration: none; transition: color 0.3s;
    }}
    .nav-links a:hover {{ color: var(--gold); }}

    .hero {{
      position: relative; min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
      text-align: center; padding: 4rem 2rem; overflow: hidden;
    }}
    .hero::before {{
      content: ''; position: absolute; inset: 0;
      background: linear-gradient(to bottom, rgba(10,7,3,0.3) 0%, rgba(10,7,3,0.6) 100%);
      z-index: 1;
    }}
    .hero-bg {{
      position: absolute; inset: 0; background: var(--ink); z-index: 0;
    }}
    .hero-bg img {{
      width: 100%; height: 100%; object-fit: cover;
    }}
    .hero-frame {{
      position: absolute; inset: 40px;
      border: 1px solid var(--gold-07); z-index: 2; pointer-events: none;
    }}
    .hero-frame-inner {{
      position: absolute; inset: 12px;
      border: 1px solid var(--gold-03);
    }}
    .hero-content {{ position: relative; z-index: 3; }}
    .hero-logo {{
      width: 80px; height: 80px; margin: 0 auto 2rem;
      border-radius: 50%; border: 1px solid var(--gold-04);
      display: flex; align-items: center; justify-content: center;
      font-family: 'Libre Caslon Display', serif;
      font-size: 1.8rem; color: var(--gold);
    }}
    .hero .eyebrow {{ font-size: 0.8rem; letter-spacing: 0.5em; margin-bottom: 2rem; }}
    .hero .headline {{ font-size: clamp(3rem, 8vw, 6.5rem); margin-bottom: 1.5rem; }}
    .hero-tagline {{
      font-family: 'Libre Caslon Text', serif; font-style: italic;
      font-size: 1.15rem; color: var(--cream-muted);
    }}
    .hero-rule {{ width: 60px; margin: 1.5rem auto; border-top: 1px solid var(--gold); }}

    .place {{ position: relative; }}
    .place-grid {{
      display: grid; grid-template-columns: 1fr 1fr;
      gap: 4rem; align-items: center;
    }}
    .place-image {{
      position: relative; aspect-ratio: 4/5; overflow: hidden;
    }}
    .place-image img {{ width: 100%; height: 100%; object-fit: cover; }}
    .place-image::after {{
      content: ''; position: absolute; inset: 14px;
      border: 1px solid var(--gold-04); pointer-events: none;
    }}
    .place .headline {{ font-size: clamp(2.2rem, 4vw, 3.2rem); margin-bottom: 1.5rem; }}
    .stats-row {{ display: flex; gap: 0; margin-top: 2.5rem; }}
    .stat {{ flex: 1; padding: 1.25rem 0; border-top: 1px solid var(--gold-04); }}
    .stat + .stat {{ padding-left: 1.5rem; border-left: 1px solid var(--gold-025); }}
    .stat-number {{
      font-family: 'Libre Caslon Display', serif;
      font-size: clamp(1.8rem, 3vw, 2.4rem);
      color: var(--cream); line-height: 1.1; margin-bottom: 0.4rem;
    }}
    .stat-number.gold {{ color: var(--gold); }}

    .engines {{ border-top: 1px solid var(--gold-04); }}
    .engines .headline {{ font-size: clamp(2.4rem, 5vw, 3.8rem); margin-bottom: 1rem; }}
    .engines .body-text {{ margin-bottom: 3rem; }}
    .engine-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 0; border-top: 1px solid var(--gold-04);
    }}
    .engine-card {{
      padding: 2rem 1.5rem;
      border-bottom: 1px solid var(--gold-04);
      border-right: 1px solid var(--gold-04);
    }}
    .engine-number {{
      font-family: 'Libre Caslon Display', serif;
      font-size: 1.6rem; color: var(--gold); margin-bottom: 0.75rem;
    }}
    .engine-name {{
      font-family: 'Archivo', sans-serif; font-weight: 600;
      font-size: 0.72rem; letter-spacing: 0.25em;
      text-transform: uppercase; color: var(--cream); margin-bottom: 0.75rem;
    }}
    .engine-desc {{
      font-size: 0.95rem; color: var(--cream-muted);
      font-style: italic; line-height: 1.5;
    }}

    .hotel {{ position: relative; border-top: 1px solid var(--gold-04); }}
    .hotel-grid {{
      display: grid; grid-template-columns: 1fr 1fr;
      gap: 4rem; align-items: center;
    }}
    .hotel .headline {{ font-size: clamp(2.2rem, 4vw, 3.2rem); margin-bottom: 1.5rem; }}
    .hotel-stats {{ margin-top: 2rem; }}
    .hotel-stat-row {{
      display: flex; justify-content: space-between; align-items: baseline;
      padding: 0.9rem 0; border-top: 1px solid var(--gold-04);
    }}
    .hotel-stat-label {{
      font-family: 'Archivo', sans-serif; font-weight: 500;
      font-size: 0.68rem; letter-spacing: 0.25em;
      text-transform: uppercase; color: var(--cream-muted);
    }}
    .hotel-stat-value {{
      font-family: 'Libre Caslon Text', serif;
      font-size: 1rem; color: var(--cream);
    }}
    .hotel-image {{ position: relative; aspect-ratio: 4/3; overflow: hidden; }}
    .hotel-image img {{ width: 100%; height: 100%; object-fit: cover; }}
    .hotel-image::after {{
      content: ''; position: absolute; inset: 14px;
      border: 1px solid var(--gold-04); pointer-events: none;
    }}

    .gallery {{ border-top: 1px solid var(--gold-04); }}
    .gallery-header {{
      display: flex; justify-content: space-between; align-items: baseline;
      margin-bottom: 3rem;
    }}
    .gallery-title {{
      font-family: 'Libre Caslon Text', serif; font-style: italic;
      font-size: 1.3rem; color: var(--cream);
    }}
    .gallery-grid {{
      display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;
    }}
    .gallery-item {{ position: relative; aspect-ratio: 4/3; overflow: hidden; }}
    .gallery-item img {{
      width: 100%; height: 100%; object-fit: cover;
      transition: transform 0.6s ease;
    }}
    .gallery-item:hover img {{ transform: scale(1.03); }}
    .gallery-item::after {{
      content: ''; position: absolute; inset: 10px;
      border: 1px solid var(--gold-04); pointer-events: none;
      transition: border-color 0.4s ease;
    }}
    .gallery-item:hover::after {{ border-color: var(--gold-07); }}
    .gallery-caption {{
      position: absolute; bottom: 0; left: 0; right: 0;
      padding: 2rem 1.5rem 1.25rem;
      background: linear-gradient(to top, rgba(10,7,3,0.9) 0%, transparent 100%);
      z-index: 1;
    }}
    .gallery-caption-title {{
      font-family: 'Archivo', sans-serif; font-weight: 600;
      font-size: 0.65rem; letter-spacing: 0.25em;
      text-transform: uppercase; color: var(--cream); margin-bottom: 0.3rem;
    }}
    .gallery-caption-sub {{
      font-family: 'Libre Caslon Text', serif; font-style: italic;
      font-size: 0.85rem; color: var(--cream-muted);
    }}

    .operators {{ border-top: 1px solid var(--gold-04); }}
    .operators .headline {{ font-size: clamp(2.2rem, 4vw, 3.2rem); margin-bottom: 1rem; }}
    .operators .body-text {{ margin-bottom: 3rem; }}
    .operator-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 0; border-top: 1px solid var(--gold-04);
    }}
    .operator-card {{
      padding: 2rem 1.5rem;
      border-bottom: 1px solid var(--gold-04);
      border-right: 1px solid var(--gold-04);
    }}
    .operator-name {{
      font-family: 'Libre Caslon Text', serif;
      font-size: 1.25rem; color: var(--cream); margin-bottom: 0.4rem;
    }}
    .operator-role {{
      font-family: 'Archivo', sans-serif; font-weight: 600;
      font-size: 0.65rem; letter-spacing: 0.25em;
      text-transform: uppercase; color: var(--gold); margin-bottom: 0.75rem;
    }}
    .operator-desc {{
      font-size: 0.92rem; color: var(--cream-muted); line-height: 1.55;
    }}

    .cta {{
      position: relative; text-align: center;
      padding: 8rem 2rem; border-top: 1px solid var(--gold-04); overflow: hidden;
    }}
    .cta::before {{
      content: ''; position: absolute; inset: 0;
      background: rgba(10,7,3,0.92);
      z-index: 1;
    }}
    .cta-bg {{ position: absolute; inset: 0; z-index: 0; }}
    .cta-bg img {{ width: 100%; height: 100%; object-fit: cover; object-position: center top; opacity: 0.15; }}
    .cta-frame {{
      position: absolute; inset: 40px;
      border: 1px solid var(--gold-07); z-index: 2; pointer-events: none;
    }}
    .cta-frame-inner {{
      position: absolute; inset: 12px; border: 1px solid var(--gold-03);
    }}
    .cta-content {{ position: relative; z-index: 3; }}
    .cta .headline {{ font-size: clamp(2.8rem, 6vw, 5rem); margin-bottom: 2.5rem; }}
    .cta-steps {{
      display: flex; justify-content: center; gap: 0;
      max-width: 800px; margin: 0 auto 3rem;
      border-top: 1px solid var(--gold-04);
      border-bottom: 1px solid var(--gold-04);
    }}
    .cta-step {{ flex: 1; padding: 1.5rem 1.25rem; text-align: left; }}
    .cta-step + .cta-step {{ border-left: 1px solid var(--gold-025); }}
    .cta-step-num {{
      font-family: 'Libre Caslon Display', serif;
      font-size: 1.4rem; color: var(--gold); margin-bottom: 0.5rem;
    }}
    .cta-step-text {{ font-size: 0.9rem; color: var(--cream-muted); line-height: 1.45; }}
    .cta-contact {{ display: flex; justify-content: center; gap: 3rem; margin-top: 2rem; }}
    .cta-contact-name {{
      font-family: 'Archivo', sans-serif; font-weight: 600;
      font-size: 0.65rem; letter-spacing: 0.25em;
      text-transform: uppercase; color: var(--cream); margin-bottom: 0.2rem;
    }}
    .cta-contact-role {{ font-size: 0.85rem; color: var(--cream-muted); }}
    .cta-disclaimer {{
      font-style: italic; font-size: 0.8rem;
      color: var(--cream-muted); opacity: 0.6;
      margin-top: 3rem; max-width: 600px; margin-left: auto; margin-right: auto;
    }}

    footer {{ padding: 2rem; text-align: center; border-top: 1px solid var(--gold-04); }}
    footer p {{
      font-family: 'Archivo', sans-serif; font-weight: 500;
      font-size: 0.6rem; letter-spacing: 0.35em;
      text-transform: uppercase; color: var(--cream-muted); opacity: 0.5;
    }}

    .fade-in {{
      opacity: 0; transform: translateY(30px);
      transition: opacity 0.8s ease, transform 0.8s ease;
    }}
    .fade-in.visible {{ opacity: 1; transform: translateY(0); }}

    @media (max-width: 768px) {{
      section {{ padding: 3.5rem 1.25rem; }}

      .hero {{ min-height: 100vh; min-height: 100dvh; padding: 3rem 1.25rem; }}
      .hero .headline {{ font-size: clamp(2.6rem, 12vw, 4rem); }}
      .hero .eyebrow {{ font-size: 0.7rem; letter-spacing: 0.4em; margin-bottom: 1.5rem; }}
      .hero-tagline {{ font-size: 1rem; }}
      .hero-logo {{ width: 60px; height: 60px; font-size: 1.4rem; margin-bottom: 1.5rem; }}
      .hero-frame {{ inset: 16px; }}
      .hero-frame-inner {{ inset: 8px; }}

      .place-grid, .hotel-grid {{ grid-template-columns: 1fr; gap: 2rem; }}
      .place-image {{ order: -1; aspect-ratio: 16/9; }}
      .place .headline, .hotel .headline, .operators .headline {{ font-size: clamp(1.8rem, 7vw, 2.4rem); }}
      .body-text {{ font-size: 0.95rem; }}

      .stats-row {{ flex-wrap: wrap; gap: 0; }}
      .stat {{ flex: 1 1 45%; }}
      .stat:nth-child(odd) {{ border-left: none; }}
      .stat-number {{ font-size: 1.6rem; }}

      .engines .headline {{ font-size: clamp(2rem, 7vw, 2.8rem); }}
      .engine-grid, .operator-grid {{ grid-template-columns: 1fr; }}
      .engine-card, .operator-card {{ border-right: none; padding: 1.5rem 1rem; }}

      .hotel-image {{ aspect-ratio: 16/9; }}

      .gallery-header {{ flex-direction: column; gap: 0.5rem; align-items: flex-start; }}
      .gallery-grid {{ grid-template-columns: 1fr; gap: 1.25rem; }}
      .gallery-item {{ aspect-ratio: 3/2; }}
      .gallery-caption {{ padding: 1.5rem 1.25rem 1rem; }}
      .gallery-caption-title {{ font-size: 0.6rem; }}
      .gallery-caption-sub {{ font-size: 0.8rem; }}

      .cta {{ padding: 5rem 1.25rem; }}
      .cta .headline {{ font-size: clamp(2rem, 8vw, 3rem); margin-bottom: 2rem; }}
      .cta-frame {{ inset: 16px; }}
      .cta-frame-inner {{ inset: 8px; }}
      .cta-steps {{ flex-direction: column; }}
      .cta-step + .cta-step {{ border-left: none; border-top: 1px solid var(--gold-025); }}
      .cta-contact {{ flex-direction: column; gap: 1.5rem; }}
      .cta-disclaimer {{ font-size: 0.75rem; }}

      .operator-name {{ font-size: 1.1rem; }}

      nav {{ padding: 1rem 1.25rem; }}
      .nav-links {{ display: none; }}

      .place-image::after, .hotel-image::after, .gallery-item::after {{
        inset: 8px;
      }}
    }}

    @media (max-width: 480px) {{
      section {{ padding: 3rem 1rem; }}
      .hero .headline {{ font-size: 2.4rem; }}
      .hero-frame {{ inset: 12px; }}
      .hero-frame-inner {{ inset: 6px; }}
      .stat {{ flex: 1 1 100%; }}
      .stat + .stat {{ border-left: none; }}
      .cta-frame {{ inset: 12px; }}
      .cta-frame-inner {{ inset: 6px; }}
      .cta .headline {{ font-size: 1.8rem; }}
    }}
  </style>
</head>
<body>

  <nav>
    <a href="#" class="nav-logo">{h(site["nav_logo"])}</a>
    <ul class="nav-links">
      <li><a href="#place">The Place</a></li>
      <li><a href="#engines">The District</a></li>
      <li><a href="#hotel">The Hotel</a></li>
      <li><a href="#operators">Operators</a></li>
      <li><a href="#contact">Contact</a></li>
    </ul>
  </nav>

  <section class="hero" id="hero">
    <div class="hero-bg">
      <img src=".{hero["background_image"]}" alt="{h(hero["background_alt"])}">
    </div>
    <div class="hero-frame"><div class="hero-frame-inner"></div></div>
    <div class="hero-content">
      <div class="hero-logo">M</div>
      <p class="eyebrow">{h(hero["eyebrow"])}</p>
      <h1 class="headline">{h(hero["headline_1"])}<br>{h(hero["headline_2"])}</h1>
      <div class="hero-rule"></div>
      <p class="hero-tagline">{h(hero["tagline"])}</p>
    </div>
  </section>

  <section class="place" id="place">
    <div class="container">
      <div class="place-grid fade-in">
        <div class="place-image">
          <img src=".{place["image"]}" alt="{h(place["image_alt"])}">
        </div>
        <div>
          <p class="eyebrow">{h(place["eyebrow"])}</p>
          <h2 class="headline">{h(place["headline"])}<br><span class="turn">{h(place["headline_turn"])}</span></h2>
          <p class="body-text">{h(place["body"])}</p>
          <div class="stats-row">
{place_stats}          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="engines" id="engines">
    <div class="container">
      <div class="fade-in">
        <p class="eyebrow">{h(engines["eyebrow"])}</p>
        <h2 class="headline">{h(engines["headline"])}<br><span class="turn">{h(engines["headline_turn"])}</span></h2>
        <p class="body-text">{h(engines["body"])}</p>
      </div>
      <div class="engine-grid fade-in">
{engine_cards}      </div>
    </div>
  </section>

  <section class="hotel" id="hotel">
    <div class="container">
      <div class="hotel-grid fade-in">
        <div>
          <p class="eyebrow">{h(hotel["eyebrow"])}</p>
          <h2 class="headline">{h(hotel["headline"])}<br><span class="turn">{h(hotel["headline_turn"])}</span></h2>
          <p class="body-text">{h(hotel["body"])}</p>
          <div class="hotel-stats">
{hotel_stats}          </div>
        </div>
        <div class="hotel-image">
          <img src=".{hotel["image"]}" alt="{h(hotel["image_alt"])}">
        </div>
      </div>
    </div>
  </section>

  <section class="gallery" id="gallery">
    <div class="container">
      <div class="gallery-header fade-in">
        <p class="eyebrow" style="margin-bottom:0;">{h(gallery["eyebrow"])}</p>
        <p class="gallery-title">{h(gallery["subtitle"])}</p>
      </div>
      <div class="gallery-grid fade-in">
{gallery_items}      </div>
    </div>
  </section>

  <section class="operators" id="operators">
    <div class="container">
      <div class="fade-in">
        <p class="eyebrow">{h(operators["eyebrow"])}</p>
        <h2 class="headline">{h(operators["headline"])}<br><span class="turn">{h(operators["headline_turn"])}</span></h2>
        <p class="body-text">{h(operators["body"])}</p>
      </div>
      <div class="operator-grid fade-in">
{operator_cards}      </div>
    </div>
  </section>

  <section class="cta" id="contact">
    <div class="cta-bg">
      <img src=".{cta["background_image"]}" alt="{h(cta["background_alt"])}">
    </div>
    <div class="cta-frame"><div class="cta-frame-inner"></div></div>
    <div class="cta-content fade-in">
      <div class="hero-logo" style="margin-bottom:1.5rem;">M</div>
      <p class="eyebrow">{h(cta["eyebrow"])}</p>
      <h2 class="headline">{h(cta["headline"])}<br><span class="turn">{h(cta["headline_turn"])}</span></h2>
      <div class="cta-steps">
{cta_steps}      </div>
      <div class="cta-contact">
{cta_contacts}      </div>
      <p class="cta-disclaimer">{cta["disclaimer"].replace(". ", ".<br>")}</p>
    </div>
  </section>

  <footer>
    <p>{h(site["footer"])}</p>
  </footer>

  <script>
    const nav = document.querySelector('nav');
    window.addEventListener('scroll', () => {{
      nav.classList.toggle('scrolled', window.scrollY > 80);
    }});

    const observer = new IntersectionObserver((entries) => {{
      entries.forEach(entry => {{
        if (entry.isIntersecting) entry.target.classList.add('visible');
      }});
    }}, {{ threshold: 0.1, rootMargin: '0px 0px -50px 0px' }});

    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

    document.querySelectorAll('a[href^="#"]').forEach(link => {{
      link.addEventListener('click', e => {{
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        if (target) target.scrollIntoView({{ behavior: 'smooth' }});
      }});
    }});

    if (window.netlifyIdentity) {{
      window.netlifyIdentity.on("init", user => {{
        if (!user) {{
          window.netlifyIdentity.on("login", () => {{
            document.location.href = "/admin/";
          }});
        }}
      }});
    }}
  </script>

</body>
</html>"""

with open("index.html", "w") as f:
    f.write(page)

print("Built index.html")
