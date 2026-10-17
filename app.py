"""
Gellar's Snack Bar website, built with Streamlit.
Run locally:  streamlit run app.py
All menu, price, hours and contact data lives in menu_data.py.
"""

import base64
import re
import urllib.parse
from datetime import datetime, timedelta
from html import escape
from zoneinfo import ZoneInfo

import streamlit as st
import streamlit.components.v1 as components

from menu_data import BUSINESS, FLAVORS_SPOTTED, HOURS, MENU

st.set_page_config(
    page_title="Gellar's Snack Bar | Ice cream & burgers in Manomet, MA",
    page_icon="🍦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

TZ = ZoneInfo("America/New_York")
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ---------------------------------------------------------------- helpers
def raw(markup: str) -> None:
    """Render HTML through st.markdown without Markdown mangling it."""
    lines = [ln.strip() for ln in markup.splitlines()]
    st.markdown("\n".join(ln for ln in lines if ln), unsafe_allow_html=True)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def money(value: float) -> str:
    return f"${value:,.2f}"


def fmt_time(hhmm: str) -> str:
    hour, minute = (int(x) for x in hhmm.split(":"))
    suffix = "am" if hour < 12 else "pm"
    hour12 = hour % 12 or 12
    return f"{hour12} {suffix}" if minute == 0 else f"{hour12}:{minute:02d} {suffix}"


def open_status() -> tuple[bool, str]:
    now = datetime.now(TZ)
    today = DAYS[now.weekday()]
    hours = HOURS.get(today)
    current = now.strftime("%H:%M")
    if hours:
        start, end = hours
        if start <= current < end:
            return True, f"Open now until {fmt_time(end)}"
        if current < start:
            return False, f"Opens today at {fmt_time(start)}"
    for offset in range(1, 8):
        day = DAYS[(now + timedelta(days=offset)).weekday()]
        if HOURS.get(day):
            label = "tomorrow" if offset == 1 else day
            return False, f"Closed now. Opens {label} at {fmt_time(HOURS[day][0])}"
    return False, "Closed for the season"


def cone_svg_uri() -> str:
    svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 340">
  <defs>
    <pattern id="waffle" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="16" height="16" fill="#E2A65B"/>
      <path d="M0 0H16M0 0V16" stroke="#B97934" stroke-width="3"/>
    </pattern>
  </defs>
  <path d="M52 168 L168 168 L110 330 Z" fill="url(#waffle)"/>
  <path d="M52 168 L168 168 L160 184 L60 184 Z" fill="#C98A43"/>
  <ellipse cx="110" cy="164" rx="66" ry="22" fill="#F7A3B8"/>
  <ellipse cx="110" cy="138" rx="58" ry="24" fill="#F9B3C5"/>
  <ellipse cx="110" cy="112" rx="47" ry="22" fill="#F7A3B8"/>
  <ellipse cx="110" cy="88" rx="35" ry="19" fill="#F9B3C5"/>
  <path d="M84 80 C88 52 104 40 118 30 C116 46 132 54 134 74 Z" fill="#F7A3B8"/>
  <path d="M70 132 C88 124 112 124 138 130" stroke="#FFE1E8" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M80 106 C96 99 114 99 132 104" stroke="#FFE1E8" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M92 82 C102 77 112 77 122 80" stroke="#FFE1E8" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>
"""
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


# Flat index of every menu item, keyed by a stable id.
ITEMS: dict[str, dict] = {}
for _tab in MENU:
    for _section in _tab["sections"]:
        for _item in _section["items"]:
            ITEMS[slug(f"{_tab['tab']}_{_item['name']}")] = _item


# ---------------------------------------------------------------- order state
if "cart" not in st.session_state:
    st.session_state.cart = {}


def add_item(item_id: str) -> None:
    cart = st.session_state.cart
    cart[item_id] = cart.get(item_id, 0) + 1
    st.session_state.just_added = ITEMS[item_id]["name"]


def change_qty(item_id: str, delta: int) -> None:
    cart = st.session_state.cart
    cart[item_id] = cart.get(item_id, 0) + delta
    if cart[item_id] <= 0:
        cart.pop(item_id, None)


def clear_order() -> None:
    st.session_state.cart = {}
    st.session_state.order_notes = ""


if name := st.session_state.pop("just_added", None):
    st.toast(f"Added {name} to your order", icon="🍦")


# ---------------------------------------------------------------- styles
raw("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Shrikhand&family=Figtree:wght@400;500;600;700;800&display=swap');
:root {
  --navy: #1D2547;
  --navy-2: #2A3463;
  --berry: #F0587D;
  --berry-dark: #B83357;
  --pink: #FFC9D6;
  --cone: #E2A65B;
  --mint: #BFE8D6;
  --mint-wash: #F1FAF6;
  --ink: #1D2547;
  --muted: #5B6280;
  --line: #E6E1EC;
}
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
.stApp { background: #FFFFFF; color: var(--ink); overflow-x: hidden; }
.stApp .stMarkdown, .stApp p, .stApp li, .stApp label, .stApp button, .stApp input, .stApp textarea, .stApp a, .stApp td, .stApp th { font-family: 'Figtree', system-ui, sans-serif; }
[data-testid="stMainBlockContainer"], .block-container { padding-top: 0 !important; padding-bottom: 0 !important; max-width: 1180px; }
.hero-tag, .status, .hero-address, .btn, .section-sub, .tab-intro, .board-note, .chip, .item-name, .item-desc, .item-price, .order-empty, .order-line-name, .order-line-sub, .subtotal, .order-fine, .story p, .facts li, .hours, .fine, .contact, .foot p, .order-fab { font-family: 'Figtree', system-ui, sans-serif; }
a:focus-visible, button:focus-visible { outline: 3px solid var(--berry) !important; outline-offset: 3px; }

/* Awning */
.awning { position: relative; height: 54px; margin: 0 calc(50% - 50vw); background: repeating-linear-gradient(90deg, var(--berry) 0 48px, #FFFFFF 48px 96px); filter: drop-shadow(0 3px 0 rgba(29,37,71,.12)); }
.awning::after { content: ""; position: absolute; left: 0; right: 0; bottom: -24px; height: 24px; background: radial-gradient(circle at 24px 0, var(--berry) 23.5px, transparent 24px) 0 0 / 96px 24px repeat-x, radial-gradient(circle at 72px 0, #FFFFFF 23.5px, transparent 24px) 0 0 / 96px 24px repeat-x; }

/* Hero */
.hero { margin-top: 2.75rem; background: radial-gradient(120% 90% at 85% 10%, var(--navy-2) 0%, var(--navy) 60%); border-radius: 36px; padding: clamp(2rem, 5vw, 4.25rem); display: grid; grid-template-columns: 1.35fr 1fr; gap: 2rem; align-items: center; overflow: hidden; }
.sign { font-family: 'Shrikhand', 'Cooper Black', 'Cooper Std', Georgia, serif; font-size: clamp(4.2rem, 11vw, 9rem); line-height: .95; color: #FFE6EC; transform: rotate(-5deg); transform-origin: left center; margin: .25rem 0 0; text-shadow: 0 0 4px #FFFFFF, 0 0 14px var(--berry), 0 0 36px var(--berry), 0 0 80px rgba(240,88,125,.55); animation: neon-on 1.6s ease-out 1 both; }
@keyframes neon-on { 0% { opacity: .1; } 10% { opacity: 1; } 14% { opacity: .25; } 22% { opacity: 1; } 27% { opacity: .55; } 34%, 100% { opacity: 1; } }
.hero-tag { color: #E8EAF6; font-size: clamp(1.1rem, 2vw, 1.35rem); line-height: 1.5; max-width: 28ch; margin: 1.75rem 0 1.25rem; }
.status { display: inline-flex; align-items: center; gap: .55rem; color: #FFFFFF; font-weight: 600; font-size: .98rem; background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.2); border-radius: 999px; padding: .45rem 1rem; }
.status .dot { width: .6rem; height: .6rem; border-radius: 50%; background: #6BE3A8; box-shadow: 0 0 10px #6BE3A8; }
.status.closed .dot { background: #FF9AB1; box-shadow: none; }
.hero-address { color: #AEB4D3; font-size: .95rem; margin-top: .75rem; }
.cta-row { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 1.75rem; }
.btn { display: inline-block; padding: .9rem 1.35rem; border-radius: 14px; font-weight: 700; font-size: 1.05rem; text-decoration: none !important; text-align: center; transition: transform .08s ease, box-shadow .08s ease; }
.btn-primary { background: var(--berry); color: #FFFFFF !important; box-shadow: 0 6px 0 var(--berry-dark); }
.btn-primary:hover { transform: translateY(3px); box-shadow: 0 3px 0 var(--berry-dark); }
.btn-ghost { color: #FFFFFF !important; border: 2px solid rgba(255,255,255,.4); }
.btn-ghost:hover { border-color: #FFFFFF; }
.btn-outline { color: var(--navy) !important; border: 2px solid var(--navy); background: #FFFFFF; }
.btn-outline:hover { background: var(--navy); color: #FFFFFF !important; }
.btn-block { display: block; width: 100%; box-sizing: border-box; margin-top: .65rem; }
.hero-art { position: relative; display: flex; justify-content: center; }
.cone { width: min(250px, 75%); filter: drop-shadow(0 24px 30px rgba(0,0,0,.35)); }
.badge { position: absolute; top: 2%; right: 6%; width: 118px; height: 118px; border-radius: 50%; background: var(--mint); color: var(--navy); display: flex; flex-direction: column; align-items: center; justify-content: center; transform: rotate(12deg); box-shadow: 0 0 0 6px var(--navy), 0 0 0 9px var(--mint); }
.badge b { font-family: 'Shrikhand', 'Cooper Black', 'Cooper Std', Georgia, serif; font-weight: 400; font-size: 2.1rem; line-height: 1; }
.badge span { font-weight: 700; font-size: .92rem; }
@media (prefers-reduced-motion: reduce) { .sign { animation: none; } .btn { transition: none; } }
@media (max-width: 760px) {
  .hero { grid-template-columns: 1fr; border-radius: 28px; }
  .hero-art { order: -1; justify-content: flex-start; }
  .cone { width: 130px; }
  .badge { width: 92px; height: 92px; left: 150px; right: auto; }
  .badge b { font-size: 1.6rem; }
  .cta-row .btn { flex: 1 1 100%; }
}

/* Sections */
.section-title { font-family: 'Shrikhand', 'Cooper Black', 'Cooper Std', Georgia, serif; font-weight: 400; font-size: clamp(2.1rem, 4.5vw, 3rem); color: var(--navy); margin: 4rem 0 .35rem; line-height: 1.1; }
.section-sub { color: var(--muted); font-size: 1.08rem; line-height: 1.55; max-width: 60ch; margin: 0 0 1.5rem; }

/* Menu tabs (selectors cover older BaseWeb tabs and newer react-aria tabs) */
.stTabs [role="tablist"] { gap: .5rem; flex-wrap: wrap; border: none !important; box-shadow: none !important; }
.stTabs [role="tablist"]::after, .stTabs [role="tablist"]::before { display: none !important; }
.stTabs [role="tab"] { background: #F5F1F7; border-radius: 999px; padding: .55rem 1.15rem !important; height: auto; border: none !important; }
.stTabs [role="tab"] p { font-weight: 700; font-size: 1rem; color: var(--navy); }
.stTabs [role="tab"][aria-selected="true"] { background: var(--navy); }
.stTabs [role="tab"][aria-selected="true"] p { color: #FFFFFF; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"], .stTabs .react-aria-SelectionIndicator { display: none !important; }
.tab-intro { color: var(--muted); font-size: 1.02rem; line-height: 1.55; max-width: 62ch; margin: .75rem 0 0; }
.board-title { font-family: 'Shrikhand', 'Cooper Black', 'Cooper Std', Georgia, serif; font-weight: 400; font-size: 1.55rem; color: var(--berry); margin: 2rem 0 .1rem; }
.board-note { color: var(--muted); font-size: .95rem; margin: 0 0 .25rem; }
.chips { display: flex; flex-wrap: wrap; gap: .5rem; margin: .75rem 0 .25rem; }
.chip { background: var(--pink); color: var(--navy); border-radius: 999px; padding: .35rem .85rem; font-weight: 600; font-size: .93rem; }

/* Menu rows */
.st-key-menu [data-testid="stHorizontalBlock"] { border-bottom: 1px dashed var(--line); padding: .6rem 0; gap: .75rem; }
.st-key-menu .stMarkdown p { margin: 0; }
.item-name { font-weight: 700; font-size: 1.06rem; color: var(--ink); }
.item-name .oos { font-weight: 600; font-size: .78rem; color: var(--berry-dark); background: #FFE6EC; border-radius: 6px; padding: .1rem .4rem; margin-left: .4rem; vertical-align: middle; }
.item-row.is-oos .item-name { color: #9AA0B8; }
.item-desc { color: var(--muted); font-size: .92rem; line-height: 1.45; max-width: 62ch; margin-top: .15rem; }
.item-price { font-weight: 700; font-size: 1.06rem; text-align: right; font-variant-numeric: tabular-nums; color: var(--ink); }
.item-price.ask { font-weight: 500; font-size: .82rem; color: var(--muted); line-height: 1.25; }
[class*="st-key-add_"] button { width: 100%; background: #FFFFFF; border: 2px solid var(--navy); color: var(--navy); border-radius: 12px; font-weight: 700; }
[class*="st-key-add_"] button p { font-weight: 700; }
[class*="st-key-add_"] button:hover { background: var(--navy); color: #FFFFFF; border-color: var(--navy); }
[class*="st-key-add_"] button:hover p { color: #FFFFFF; }
@media (max-width: 640px) {
  .st-key-menu [data-testid="stHorizontalBlock"], .st-key-order [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; }
  .st-key-menu [data-testid="stColumn"], .st-key-order [data-testid="stColumn"] { min-width: 0 !important; width: auto !important; }
  .st-key-menu [data-testid="stColumn"]:nth-child(1) { flex: 1 1 0 !important; }
  .st-key-menu [data-testid="stColumn"]:nth-child(2) { flex: 0 0 4.3rem !important; }
  .st-key-menu [data-testid="stColumn"]:nth-child(3) { flex: 0 0 4.4rem !important; }
}

/* Order panel */
.st-key-order { background: var(--mint-wash); border: 2px solid var(--mint); border-radius: 24px; padding: 1.4rem 1.3rem 1.2rem; position: sticky; top: 1rem; }
.order-title { font-family: 'Shrikhand', 'Cooper Black', 'Cooper Std', Georgia, serif; font-weight: 400; font-size: 1.8rem; color: var(--navy); margin: 0; }
.order-empty { color: var(--muted); line-height: 1.5; margin: .25rem 0 0; }
.order-line-name { font-weight: 700; line-height: 1.3; }
.order-line-sub { color: var(--muted); font-size: .88rem; }
.st-key-order .stMarkdown p { margin: 0; }
[class*="st-key-dec_"] button, [class*="st-key-inc_"] button { min-height: 2.1rem; padding: 0 .6rem; border-radius: 10px; border: 2px solid var(--mint); background: #FFFFFF; font-weight: 800; }
.subtotal { display: flex; justify-content: space-between; font-weight: 800; font-size: 1.2rem; border-top: 2px dashed var(--mint); padding-top: .8rem; margin-top: .4rem; color: var(--navy); }
.order-fine { color: var(--muted); font-size: .85rem; line-height: 1.45; margin: .35rem 0 .75rem !important; }
.st-key-clear_order button { background: transparent; border: none; color: var(--muted); text-decoration: underline; padding: 0; min-height: 0; }

/* Floating order bar, phones only */
.order-fab { display: none; }
@media (max-width: 640px) {
  .order-fab { display: flex; justify-content: space-between; align-items: center; position: fixed; left: 12px; right: 12px; bottom: calc(12px + env(safe-area-inset-bottom, 0px)); z-index: 1000; background: var(--navy); color: #FFFFFF !important; text-decoration: none !important; font-weight: 700; padding: .95rem 1.2rem; border-radius: 16px; box-shadow: 0 10px 24px rgba(29,37,71,.35); }
  .order-fab span:last-child { color: var(--pink); }
}

/* Story */
.story { display: grid; grid-template-columns: 1.15fr 1fr; gap: clamp(1.5rem, 4vw, 3.5rem); align-items: start; }
.story p { font-size: 1.1rem; line-height: 1.7; max-width: 58ch; color: var(--ink); margin: 0 0 1rem; }
.facts { list-style: none; padding: 0; margin: 0; border-left: 6px solid var(--cone); }
.facts li { padding: .8rem 0 .8rem 1.2rem; font-size: 1.04rem; line-height: 1.5; border-bottom: 1px dashed var(--line); }
.facts li:last-child { border-bottom: none; }
.facts strong { color: var(--berry-dark); }
@media (max-width: 760px) { .story { grid-template-columns: 1fr; } }

/* Visit */
.hours { width: 100%; border-collapse: collapse; font-size: 1.02rem; border: none !important; }
.hours tr { border: none !important; background: transparent !important; }
.hours td { padding: .5rem .25rem !important; border: none !important; border-bottom: 1px dashed var(--line) !important; }
.hours td:last-child { text-align: right; font-variant-numeric: tabular-nums; }
.hours tr.today td { font-weight: 800; color: var(--berry-dark); }
.contact { margin-top: 1.5rem; line-height: 1.8; font-size: 1.04rem; }
.contact a { color: var(--navy); font-weight: 700; }
.fine { color: var(--muted); font-size: .88rem; margin-top: .75rem; }
.st-key-map iframe { border-radius: 24px; border: 2px solid var(--line) !important; }

/* Footer */
.foot { margin: 4.5rem calc(50% - 50vw) 0; background: var(--navy); color: #C9CDE4; padding: 2.5rem max(1.5rem, calc(50vw - 560px)); display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; align-items: center; }
.foot-sign { font-family: 'Shrikhand', 'Cooper Black', 'Cooper Std', Georgia, serif; font-size: 2rem; color: #FFE6EC; text-shadow: 0 0 14px var(--berry); }
.foot p { margin: 0; font-size: .92rem; line-height: 1.6; }
.foot a { color: #FFFFFF; }
</style>
""")


# ---------------------------------------------------------------- hero
is_open, status_text = open_status()
toast_url = escape(BUSINESS["toast_url"])
raw(f"""
<div class="awning" aria-hidden="true"></div>
<section class="hero">
  <div>
    <div class="sign" role="heading" aria-level="1">{escape(BUSINESS["sign_name"])}</div>
    <p class="hero-tag">{escape(BUSINESS["tagline"])}</p>
    <div class="status {'open' if is_open else 'closed'}"><span class="dot"></span>{escape(status_text)}</div>
    <div class="hero-address">{escape(BUSINESS["address_line1"])}, {escape(BUSINESS["address_line2"])}</div>
    <div class="cta-row">
      <a class="btn btn-primary" href="{toast_url}" target="_blank" rel="noopener">Order online</a>
      <a class="btn btn-ghost" href="tel:{BUSINESS["phone_tel"]}">Call {escape(BUSINESS["phone_display"])}</a>
    </div>
  </div>
  <div class="hero-art">
    <img class="cone" src="{cone_svg_uri()}" alt="A strawberry soft-serve cone, like the one on Gellar's roof">
    <div class="badge" role="img" aria-label="100th summer"><b>100th</b><span>summer</span></div>
  </div>
</section>
""")


# ---------------------------------------------------------------- menu + order
raw('<div class="section-title" role="heading" aria-level="2" id="menu">The menu</div>')
raw('<p class="section-sub">Add what you want, then place the order online or call it in. Prices come from the shop and can change, so the window has the final word.</p>')

menu_col, order_col = st.columns([1.75, 1], gap="large")

with menu_col:
    with st.container(key="menu"):
        tabs = st.tabs([t["tab"] for t in MENU])
        for tab, tab_data in zip(tabs, MENU):
            with tab:
                raw(f'<p class="tab-intro">{escape(tab_data["intro"])}</p>')
                if tab_data["tab"] == "Ice cream":
                    chips = "".join(f'<span class="chip">{escape(f)}</span>' for f in FLAVORS_SPOTTED)
                    raw(f'<div class="board-title">Flavors spotted lately</div><div class="chips">{chips}</div>')
                for section in tab_data["sections"]:
                    note = f'<p class="board-note">{escape(section["note"])}</p>' if section["note"] else ""
                    raw(f'<div class="board-title">{escape(section["title"])}</div>{note}')
                    for it in section["items"]:
                        item_id = slug(f"{tab_data['tab']}_{it['name']}")
                        c_name, c_price, c_add = st.columns([6, 1.5, 1.5], vertical_alignment="center")
                        oos = it["out_of_stock"]
                        with c_name:
                            badge = '<span class="oos">Sold out</span>' if oos else ""
                            desc = f'<div class="item-desc">{escape(it["desc"])}</div>' if it["desc"] else ""
                            raw(f'<div class="item-row{" is-oos" if oos else ""}"><div class="item-name">{escape(it["name"])}{badge}</div>{desc}</div>')
                        with c_price:
                            if it["price"] is None:
                                raw('<div class="item-price ask">Ask at the window</div>')
                            else:
                                raw(f'<div class="item-price">{money(it["price"])}</div>')
                        with c_add:
                            if it["price"] is not None and not oos:
                                st.button("Add", key=f"add_{item_id}", on_click=add_item, args=(item_id,))

with order_col:
    with st.container(key="order"):
        raw('<div class="order-title" role="heading" aria-level="2" id="your-order">Your order</div>')
        cart = st.session_state.cart
        if not cart:
            raw('<p class="order-empty">Nothing here yet. Tap Add next to anything on the menu and it shows up here with a running total.</p>')
        else:
            subtotal = 0.0
            lines = []
            for item_id, qty in list(cart.items()):
                it = ITEMS[item_id]
                line_total = it["price"] * qty
                subtotal += line_total
                lines.append(f"{qty} x {it['name']}  {money(line_total)}")
                c_line, c_minus, c_plus = st.columns([4, 1, 1], vertical_alignment="center")
                with c_line:
                    raw(f'<div class="order-line-name">{qty} × {escape(it["name"])}</div><div class="order-line-sub">{money(line_total)}</div>')
                with c_minus:
                    st.button("−", key=f"dec_{item_id}", on_click=change_qty, args=(item_id, -1), help="Remove one")
                with c_plus:
                    st.button("+", key=f"inc_{item_id}", on_click=change_qty, args=(item_id, 1), help="Add one")
            raw(f'<div class="subtotal"><span>Subtotal</span><span>{money(subtotal)}</span></div>')
            count = sum(cart.values())
            raw(f'<a class="order-fab" href="#your-order" target="_self"><span>View your order ({count})</span><span>{money(subtotal)}</span></a>')
            raw('<p class="order-fine">Before tax. Online checkout happens on Gellar\'s own Toast page, so your payment goes straight to the shop.</p>')
            notes = st.text_area(
                "Notes for the kitchen",
                key="order_notes",
                placeholder="Cheeseburger dragged through the garden, extra pickles…",
                height=80,
            )
            raw(f"""
            <a class="btn btn-primary btn-block" href="{toast_url}" target="_blank" rel="noopener">Place order online</a>
            <a class="btn btn-outline btn-block" href="tel:{BUSINESS["phone_tel"]}">Call it in</a>
            """)
            with st.expander("Read your order over the phone"):
                summary = "Gellar's order\n" + "\n".join(lines) + f"\nSubtotal before tax: {money(subtotal)}"
                if notes.strip():
                    summary += f"\nNotes: {notes.strip()}"
                st.code(summary, language=None)
            st.button("Clear order", key="clear_order", on_click=clear_order)


# ---------------------------------------------------------------- story
raw('<div class="section-title" role="heading" aria-level="2">100 summers on the corner</div>')
raw("""
<div class="story">
  <div>
    <p>Gellar's opened in 1926, when Calvin Coolidge was president, at the corner of Route 3A and White Horse Road. It made it through the Depression and every summer since, and it's still in the family. Peter Gellar is the fourth generation behind the window.</p>
    <p>You'll know it by the five-foot strawberry cone on the roof. The sign says Gellars, no apostrophe. Somewhere along the way it fell off, and nobody put it back.</p>
    <p>Grab a picnic table out back after the beach, or stop in year-round. There are a few seats inside for the cold months.</p>
  </div>
  <ul class="facts">
    <li><strong>Ice cream</strong> from Richardson's in Middleton, with 24 soft-serve flavors and about 36 hard ones</li>
    <li><strong>Burgers</strong> hand-packed by Perry's Market, right here in Plymouth</li>
    <li><strong>Pickles and lemonade</strong> made in house</li>
    <li><strong>A kids' table</strong> built into a replica 1957 Chevy convertible</li>
  </ul>
</div>
""")


# ---------------------------------------------------------------- visit
raw('<div class="section-title" role="heading" aria-level="2">Come by</div>')
raw(f'<p class="section-sub">{escape(BUSINESS["cross_street"])}, a short walk up from White Horse Beach.</p>')

info_col, map_col = st.columns([1, 1.35], gap="large")
with info_col:
    today = DAYS[datetime.now(TZ).weekday()]
    rows = ""
    for day in DAYS:
        hrs = HOURS.get(day)
        text = f"{fmt_time(hrs[0])} to {fmt_time(hrs[1])}" if hrs else "Closed"
        rows += f'<tr class="{"today" if day == today else ""}"><td>{day}</td><td>{text}</td></tr>'
    raw(f"""
    <table class="hours" aria-label="Opening hours">{rows}</table>
    <p class="fine">Hours shift with the season. Check Facebook or call before a special trip.</p>
    <div class="contact">
      {escape(BUSINESS["address_line1"])}<br>{escape(BUSINESS["address_line2"])}<br>
      <a href="tel:{BUSINESS["phone_tel"]}">{escape(BUSINESS["phone_display"])}</a><br>
      <a href="mailto:{BUSINESS["email"]}">{escape(BUSINESS["email"])}</a><br>
      <a href="{escape(BUSINESS["facebook"])}" target="_blank" rel="noopener">Follow on Facebook for specials</a>
    </div>
    """)
with map_col:
    with st.container(key="map"):
        q = urllib.parse.quote(BUSINESS["map_query"])
        map_url = f"https://maps.google.com/maps?q={q}&z=15&output=embed"
        if hasattr(st, "iframe"):  # Streamlit 1.5x+
            st.iframe(map_url, height=420)
        else:
            components.iframe(map_url, height=420)


# ---------------------------------------------------------------- footer
year = datetime.now(TZ).year
raw(f"""
<div class="foot" role="contentinfo">
  <div class="foot-sign">{escape(BUSINESS["sign_name"])}</div>
  <p>{escape(BUSINESS["name"])}, {escape(BUSINESS["address_line1"])}, Manomet<br>
  Serving the corner since {BUSINESS["founded"]}. © {year}</p>
  <p><a href="{toast_url}" target="_blank" rel="noopener">Order online</a><br>
  <a href="tel:{BUSINESS["phone_tel"]}">{escape(BUSINESS["phone_display"])}</a></p>
</div>
""")
