"""
build_caetanos_site.py
Generates a single-file website for Caetano's Barber Shop (Dartmouth, MA).

Edit the CONTENT section below (prices, hours, story, reviews), then run:
    python build_caetanos_site.py
It writes caetanos_barber_shop.html next to this script.
"""
from html import escape
from pathlib import Path

# ----------------------------------------------------------------------------
# CONTENT — everything the owner would want to change lives here
# ----------------------------------------------------------------------------
SHOP = {
    "name": "Caetano’s Barber Shop",
    "street": "601 State Rd",
    "town": "Dartmouth, MA 02747",
    "phone_display": "(774) 627-0241",
    "phone_link": "+17746270241",
    "maps": "https://maps.google.com/?q=601+State+Rd+Dartmouth+MA+02747",
}

# Sample prices — replace with the shop's real menu
SERVICES = [
    ("Classic haircut", "Scissor or clipper cut, finished with a neck shave", 30),
    ("Skin fade", "Taper down to the skin, blended by hand", 35),
    ("Haircut and beard", "Full cut plus beard shape and line-up", 45),
    ("Beard trim", "Shape, line-up and hot towel", 18),
    ("Hot towel shave", "Straight razor, two passes, warm lather", 35),
    ("Line-up", "Edges, temples and neckline between cuts", 15),
    ("Kids’ cut", "12 and under", 22),
    ("Seniors", "65 and up, any weekday", 22),
]

# Sample hours — replace with real hours
HOURS = [
    ("Monday", "Closed"),
    ("Tuesday", "9 am – 6 pm"),
    ("Wednesday", "9 am – 6 pm"),
    ("Thursday", "9 am – 7 pm"),
    ("Friday", "9 am – 7 pm"),
    ("Saturday", "8 am – 3 pm"),
    ("Sunday", "Closed"),
]

# Sample story — replace with Caetano's own words
STORY = [
    "Caetano picked up his first pair of clippers cutting his cousins’ hair "
    "on the back porch. By the time he was out of barber school, half the "
    "neighborhood was showing up on that porch.",
    "He spent years behind someone else’s chair before deciding he wanted "
    "something smaller, not bigger: one chair, his own hours, and the time "
    "to actually talk to the person sitting in it.",
    "So he opened at 601 State Rd. No sign out on the highway, no ads. Just "
    "one customer telling the next. Most people who sit down here were sent "
    "by someone who already does.",
]

# How people found the shop — the word-of-mouth section (sample quotes)
REFERRALS = [
    ("My father-in-law sent me. Now I send my son.", "Mike R., Dartmouth"),
    ("Best fade on the SouthCoast and he remembers how you like it.", "Jay T., New Bedford"),
    ("Saw a coworker’s cut, asked where. Been going three years.", "Luis A., Fairhaven"),
]

FAQ = [
    ("Do I need an appointment?",
     "It’s a one-chair shop, so calling ahead is the surest way to get in. "
     "Walk-ins are welcome when the chair is open."),
    ("How do I pay?", "Cash and card are both fine."),
    ("Where do I park?", "There’s parking right in front of the shop on State Rd."),
]

GALLERY = ["Skin fade", "Classic side part", "Beard shape-up",
           "Kids’ cut", "Textured crop", "Hot towel shave"]


# ----------------------------------------------------------------------------
# RENDERING
# ----------------------------------------------------------------------------
def e(text):
    return escape(text, quote=True)


def render_services():
    rows = []
    for name, desc, price in SERVICES:
        rows.append(f"""
        <li class="svc">
          <div class="svc-line"><span class="svc-name">{e(name)}</span>
            <span class="leader" aria-hidden="true"></span>
            <span class="svc-price">${price}</span></div>
          <p class="svc-desc">{e(desc)}</p>
        </li>""")
    return "".join(rows)


def render_hours():
    return "".join(
        f'<tr><th scope="row">{e(d)}</th><td>{e(h)}</td></tr>' for d, h in HOURS
    )


def render_story():
    return "".join(f"<p>{e(p)}</p>" for p in STORY)


def render_referrals():
    return "".join(
        f'<figure class="ref"><blockquote>“{e(q)}”</blockquote>'
        f"<figcaption>{e(who)}</figcaption></figure>"
        for q, who in REFERRALS
    )


def render_faq():
    return "".join(
        f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>"
        for q, a in FAQ
    )


def render_gallery():
    return "".join(
        f'<div class="ph" role="img" aria-label="Photo placeholder: {e(g)}">'
        f"<span>{e(g)}</span></div>"
        for g in GALLERY
    )


CSS = """
:root{
  --ink:#16241D; --paper:#EEF1EC; --surface:#FFFFFF; --green:#1E3B2F;
  --brass:#A9822F; --red:#B3261E; --muted:#56635C; --line:#C9D0CA;
  --pole-blue:#1F3A6B;
  color-scheme:light;
  box-sizing:border-box;
  padding-top:env(safe-area-inset-top,0px);
  padding-bottom:env(safe-area-inset-bottom,0px);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ink:#E6ECE7; --paper:#101A15; --surface:#18251E; --green:#2C5242;
    --brass:#D2AA55; --red:#E0574E; --muted:#9FAEA5; --line:#2D3D34;
    color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --ink:#E6ECE7; --paper:#101A15; --surface:#18251E; --green:#2C5242;
  --brass:#D2AA55; --red:#E0574E; --muted:#9FAEA5; --line:#2D3D34;
  color-scheme:dark;
}
*,*::before,*::after{box-sizing:inherit}
html{scroll-behavior:smooth;scroll-padding-top:calc(env(safe-area-inset-top,0px) + 64px)}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"Libre Franklin",system-ui,-apple-system,"Segoe UI",sans-serif;
  font-size:1.0625rem;line-height:1.6}
a{color:inherit}
:focus-visible{outline:3px solid var(--brass);outline-offset:3px}
.wrap{max-width:1080px;margin:0 auto;padding:0 1.25rem}
h1,h2,h3{font-family:"Alfa Slab One",Rockwell,"Roboto Slab",Georgia,serif;
  font-weight:400;line-height:1.08;margin:0}
h2{font-size:clamp(1.9rem,4vw,2.6rem);margin-bottom:1.5rem}

/* sample notice */
.notice{background:var(--brass);color:#1a1405;font-size:.875rem;text-align:center;padding:.45rem 1rem}

/* header */
header.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;
  background:var(--paper);border-bottom:1px solid var(--line)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);
  z-index:21;background:var(--paper)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;height:60px;gap:1rem}
.brand{font-family:"Alfa Slab One",Rockwell,Georgia,serif;font-size:1.2rem;text-decoration:none}
nav.links{display:flex;gap:1.4rem;font-size:.95rem}
nav.links a{text-decoration:none;color:var(--muted)}
nav.links a:hover{color:var(--ink)}
.btn{display:inline-block;background:var(--red);color:#fff;text-decoration:none;
  font-weight:700;padding:.7rem 1.2rem;border-radius:999px;white-space:nowrap}
.btn:hover{filter:brightness(1.08)}
.btn.ghost{background:transparent;color:var(--ink);border:2px solid var(--ink)}
@media (max-width:760px){nav.links{display:none}}

/* hero */
.hero{padding:4.5rem 0 4rem}
.hero .wrap{display:grid;grid-template-columns:72px 1fr;gap:2.5rem;align-items:stretch}
.pole{border-radius:36px;min-height:340px;border:5px solid var(--brass);
  background:repeating-linear-gradient(-45deg,
     var(--red) 0 18px,#fff 18px 36px,var(--pole-blue) 36px 54px,#fff 54px 72px);
  background-size:100% 204px;animation:spin 3.2s linear infinite}
@keyframes spin{to{background-position:0 204px}}
@media (prefers-reduced-motion:reduce){.pole{animation:none}}
.hero h1{font-size:clamp(2.8rem,8.5vw,6.2rem);letter-spacing:-.01em}
.hero p.lede{font-size:1.2rem;max-width:34ch;margin:1.4rem 0 2rem;color:var(--muted)}
.hero .actions{display:flex;flex-wrap:wrap;gap:.8rem}
.hero address{font-style:normal;margin-top:2rem;color:var(--muted);font-size:.95rem}
@media (max-width:600px){
  .hero .wrap{grid-template-columns:28px 1fr;gap:1.2rem}
  .pole{border-width:3px;min-height:260px}
}

section{padding:4.5rem 0;border-top:1px solid var(--line)}

/* services menu */
.menu{display:grid;grid-template-columns:1fr 1fr;gap:0 3.5rem;list-style:none;margin:0;padding:0}
@media (max-width:760px){.menu{grid-template-columns:1fr}}
.svc{padding:1rem 0;border-bottom:1px dashed var(--line)}
.svc-line{display:flex;align-items:baseline;gap:.6rem}
.svc-name{font-weight:700;font-size:1.1rem}
.leader{flex:1;border-bottom:2px dotted var(--muted);transform:translateY(-4px);opacity:.5}
.svc-price{font-family:"Alfa Slab One",Rockwell,Georgia,serif;font-size:1.35rem;color:var(--red)}
.svc-desc{margin:.2rem 0 0;color:var(--muted);font-size:.95rem}
.menu-note{margin-top:1.5rem;color:var(--muted);font-size:.95rem}

/* story */
.story .wrap{display:grid;grid-template-columns:1fr 1.4fr;gap:3rem}
@media (max-width:760px){.story .wrap{grid-template-columns:1fr;gap:1rem}}
.story-text p{max-width:62ch;margin:0 0 1.1rem}
.story-text p:first-child{font-size:1.25rem;line-height:1.5}

/* referrals */
.refs{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem}
@media (max-width:760px){.refs{grid-template-columns:1fr}}
.ref{margin:0;padding-left:1.1rem;border-left:4px solid var(--brass)}
.ref blockquote{margin:0 0 .6rem;font-size:1.2rem;line-height:1.45}
.ref figcaption{color:var(--muted);font-size:.9rem}
.refs-intro{max-width:56ch;color:var(--muted);margin:-.6rem 0 2rem}

/* gallery */
.gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem}
@media (max-width:600px){.gallery{grid-template-columns:repeat(2,1fr)}}
.ph{aspect-ratio:1/1;border-radius:6px;background:var(--green);display:flex;align-items:flex-end;
  padding:.8rem;color:#E6ECE7;font-size:.9rem;
  background-image:radial-gradient(circle at 30% 30%,rgba(255,255,255,.10),transparent 60%)}

/* visit */
.visit .wrap{display:grid;grid-template-columns:1fr 1fr;gap:3rem}
@media (max-width:760px){.visit .wrap{grid-template-columns:1fr}}
table.hours{border-collapse:collapse;width:100%;max-width:380px}
.hours th,.hours td{text-align:left;padding:.5rem 0;border-bottom:1px solid var(--line);font-weight:400}
.hours td{text-align:right}
.hours tr.today th,.hours tr.today td{font-weight:700;color:var(--red)}
.visit address{font-style:normal;font-size:1.2rem;margin-bottom:1.2rem}
details{border-bottom:1px solid var(--line);padding:.9rem 0}
summary{cursor:pointer;font-weight:700}
details p{margin:.5rem 0 0;color:var(--muted)}

footer{background:var(--green);color:#E6ECE7;padding:2.5rem 0 calc(2.5rem + 64px)}
footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:1rem;font-size:.95rem}
footer a{color:#E6ECE7}

/* mobile call bar */
.callbar{display:none}
@media (max-width:760px){
  .callbar{display:block;position:fixed;left:0;right:0;bottom:0;z-index:30;
    background:var(--red);text-align:center;
    padding:.95rem 1rem calc(.95rem + env(safe-area-inset-bottom,0px))}
  .callbar a{color:#fff;font-weight:700;text-decoration:none;font-size:1.05rem}
}
"""

JS = """
(function(){
  var days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var today=days[new Date().getDay()];
  document.querySelectorAll('.hours tr').forEach(function(r){
    if(r.querySelector('th').textContent===today){r.classList.add('today');}
  });
  document.getElementById('yr').textContent=new Date().getFullYear();
})();
"""


def build():
    s = SHOP
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(s['name'])} · Dartmouth, MA</title>
<meta name="description" content="One-chair barber shop at 601 State Rd, Dartmouth, MA. Haircuts, fades, beard trims and hot towel shaves. Call {e(s['phone_display'])}.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Libre+Franklin:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="notice">Sample site: prices, hours, story and reviews are placeholders to swap for the real ones.</div>

<header class="top"><div class="wrap">
  <a class="brand" href="#top">Caetano’s</a>
  <nav class="links" aria-label="Sections">
    <a href="#prices">Prices</a><a href="#story">Our story</a>
    <a href="#work">The work</a><a href="#visit">Visit</a>
  </nav>
  <a class="btn" href="tel:{s['phone_link']}">Call to book</a>
</div></header>

<main id="top">
  <div class="hero"><div class="wrap">
    <div class="pole" aria-hidden="true"></div>
    <div>
      <h1>One chair.<br>One barber.<br>No strangers.</h1>
      <p class="lede">A neighborhood barber shop on State Rd in Dartmouth, built one customer at a time.</p>
      <div class="actions">
        <a class="btn" href="tel:{s['phone_link']}">Call {e(s['phone_display'])}</a>
        <a class="btn ghost" href="#prices">See prices</a>
      </div>
      <address>{e(s['street'])}, {e(s['town'])}</address>
    </div>
  </div></div>

  <section id="prices"><div class="wrap">
    <h2>What we do</h2>
    <ul class="menu">{render_services()}</ul>
    <p class="menu-note">Every cut includes a hot towel and a neck shave. Prices are cash or card.</p>
  </div></section>

  <section id="story" class="story"><div class="wrap">
    <h2>How it started</h2>
    <div class="story-text">{render_story()}</div>
  </div></section>

  <section id="word"><div class="wrap">
    <h2>Who sent you?</h2>
    <p class="refs-intro">Nobody finds this shop by accident. Here’s how a few regulars ended up in the chair.</p>
    <div class="refs">{render_referrals()}</div>
  </div></section>

  <section id="work"><div class="wrap">
    <h2>The work</h2>
    <div class="gallery">{render_gallery()}</div>
  </div></section>

  <section id="visit" class="visit"><div class="wrap">
    <div>
      <h2>Come by</h2>
      <address>{e(s['street'])}<br>{e(s['town'])}</address>
      <p><a class="btn" href="tel:{s['phone_link']}">Call {e(s['phone_display'])}</a>
         &nbsp;<a href="{e(s['maps'])}" target="_blank" rel="noopener">Get directions</a></p>
      <table class="hours" aria-label="Opening hours"><tbody>{render_hours()}</tbody></table>
    </div>
    <div>
      <h2>Good to know</h2>
      {render_faq()}
    </div>
  </div></section>
</main>

<footer><div class="wrap">
  <span>© <span id="yr"></span> {e(s['name'])}</span>
  <span>{e(s['street'])}, {e(s['town'])} · <a href="tel:{s['phone_link']}">{e(s['phone_display'])}</a></span>
</div></footer>

<div class="callbar"><a href="tel:{s['phone_link']}">Call to book · {e(s['phone_display'])}</a></div>
<script>{JS}</script>
</body>
</html>"""
    out = Path(__file__).with_name("caetanos_barber_shop.html")
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} ({len(html):,} bytes)")


if __name__ == "__main__":
    build()
