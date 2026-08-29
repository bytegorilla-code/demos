#!/usr/bin/env python3
"""
ReforgeIT — static site generator.

Run:  python3 build.py
It rewrites every .html file in this folder from the templates below, so the
header, footer and <head> stay identical across pages. Edit here, not in the
generated HTML, or your change will be overwritten next time you run it.
"""
import os, re, datetime

# ---------------------------------------------------------------- settings
SITE   = "https://www.reforgeit.co.uk"   # REPLACE with the real domain
BRAND  = "ReforgeIT"
LEGAL  = "Essentialtechgb Ltd"           # REPLACE if the registered name changed
EBAY   = "https://www.ebay.co.uk/str/everydayneed"
EMAIL  = "sales@essentialtechgb.co.uk"
EMAIL2 = "essentialtechgb@gmail.com"
ADDR1  = "Unit 3 Metro Triangle"
ADDR2  = "Mount Street, Birmingham"
POST   = "B7 5QT"
HOURS  = "Mon–Fri 9:00–18:00"
YEAR   = "2025/26"

CAT = {
    "laptops":  EBAY + "/Laptops/_i.html?store_cat=44082038012",
    "desktops": EBAY + "/Desktop-PC/_i.html?store_cat=44082043012",
    "accs":     EBAY + "/Accessories/_i.html?store_cat=44082042012",
}

NAV = [("Home","index.html"), ("Products","products.html"), ("About","about.html"),
       ("Process","process.html"), ("Reviews","reviews.html"), ("Blog","blog.html"),
       ("Contact","contact.html")]

SPRITE = open("images/logo/logo-sprite.svg", encoding="utf-8").read().strip()
HDR = open("_header.html", encoding="utf-8").read()
FTR = open("_footer.html", encoding="utf-8").read()
FTR_TAIL = """
<button class="top" id="toTop" aria-label="Back to top">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>

<script src="js/main.js" defer></script>
</body>
</html>
"""

# ---------------------------------------------------------------- favicon
FAVICON = ("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20"
           "viewBox%3D%220%200%2064%2064%22%3E%3Cdefs%3E%3ClinearGradient%20id%3D%22g%22%20"
           "x1%3D%220%22%20y1%3D%220%22%20x2%3D%221%22%20y2%3D%221%22%3E%3Cstop%20offset%3D%220%22%20"
           "stop-color%3D%22%232FAF66%22/%3E%3Cstop%20offset%3D%221%22%20stop-color%3D%22%23404093%22/%3E"
           "%3C/linearGradient%3E%3C/defs%3E%3Crect%20width%3D%2264%22%20height%3D%2264%22%20rx%3D%2214%22%20"
           "fill%3D%22url%28%23g%29%22/%3E%3Cg%20transform%3D%22translate%282.310%201.700%29%20scale%280.1732%29%22%20"
           "fill%3D%22%23fff%22%3E%3Cpath%20d%3D%22M249.84%2C111.62c.35-13.15-3.97-24.17-12.85-32.93-19.43-19.18-56.26-23.9-76.96-24.99%2C"
           "21.44%2C10.63%2C33.19%2C23.14%2C34.97%2C37.27%2C2.9%2C22.97-21.67%2C40.9-22.71%2C41.65l-106.85%2C83.2-.8%2C77.19c22.25-17.45%2C"
           "42.79-33.14%2C61.06-47.1%2C80.93-61.81%2C125.51-95.85%2C124.13-134.29Z%22/%3E%3Cpath%20d%3D%22M198.13%2C205.37l-48.28%2C"
           "37.02%2C24.83%2C28.04c14.57%2C16.45%2C35.49%2C25.88%2C57.47%2C25.88h46.72l-80.74-90.93Z%22/%3E%3Cpath%20d%3D%22M185.86%2C"
           "92.12c-1.37-10.84-11.44-20.99-29.92-30.16-8.54-4.24-17.95-6.44-27.49-6.44h-64.16v58.84h113.6c4.77-5.98%2C9.04-13.81%2C"
           "7.98-22.23Z%22/%3E%3C/g%3E%3C/svg%3E")

# ---------------------------------------------------------------- structured data
ORG_LD = """{
  "@context":"https://schema.org",
  "@type":"Organization",
  "@id":"%(site)s/#organization",
  "name":"%(brand)s",
  "legalName":"%(legal)s",
  "url":"%(site)s/",
  "logo":"%(site)s/images/logo/logo-full-colour.svg",
  "email":"%(email)s",
  "slogan":"Rebuilt for what's next",
  "address":{"@type":"PostalAddress","streetAddress":"%(a1)s, %(a2s)s",
    "addressLocality":"Birmingham","postalCode":"%(post)s","addressCountry":"GB"},
  "sameAs":["%(ebay)s"]
}""" % dict(site=SITE, brand=BRAND, legal=LEGAL, email=EMAIL, a1=ADDR1,
            a2s="Mount Street", post=POST, ebay=EBAY)

SITE_LD = """{
  "@context":"https://schema.org",
  "@type":"WebSite",
  "@id":"%s/#website",
  "url":"%s/",
  "name":"%s",
  "publisher":{"@id":"%s/#organization"}
}""" % (SITE, SITE, BRAND, SITE)


def crumb_ld(trail):
    items = []
    for i, (label, url) in enumerate(trail, start=1):
        items.append('{"@type":"ListItem","position":%d,"name":"%s","item":"%s/%s"}'
                     % (i, label, SITE, url))
    return ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}'
            % ",".join(items))


# ---------------------------------------------------------------- head
PRELOADER = """
<div class="pre" id="pre">
  <div class="pre__in">
    <span class="pre__mk"><svg viewBox="0 0 343.15 350" aria-hidden="true"><use href="#ri-mark"/></svg></span>
    <svg class="pre__logo" role="img" aria-label="ReforgeIT"><use href="#ri-logo"/></svg>
    <span class="pre__bar"><i></i></span>
  </div>
</div>
"""


def head(title, desc, slug, extra_ld="", pre=False):
    ld = '\n<script type="application/ld+json">%s</script>' % ORG_LD
    ld += '\n<script type="application/ld+json">%s</script>' % SITE_LD
    if extra_ld:
        ld += '\n<script type="application/ld+json">%s</script>' % extra_ld
    PRE = PRELOADER if pre else ""
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{slug}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#2FAF66">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{slug}">
<meta property="og:image" content="{SITE}/images/social/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/images/social/og-image.jpg">

<link rel="icon" type="image/svg+xml" href="{FAVICON}">
<link rel="icon" type="image/png" sizes="32x32" href="images/logo/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="images/logo/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
{ld}
</head>
<body>

<a class="skip" href="#main">Skip to content</a>

{SPRITE}
{PRE}
"""


# ---------------------------------------------------------------- header
def header():
    return '\n<div class="prog" id="prog"></div>\n' + HDR


# ---------------------------------------------------------------- page banner
def banner(h1, sub, trail):
    crumbs = "\n          ".join(
        (f'<li><a href="{u}">{n}</a></li>' if u else f'<li aria-current="page">{n}</li>')
        for n, u in trail)
    return f"""
<section class="phero">
  <svg class="mark-wm" viewBox="0 0 343.15 350" aria-hidden="true"><use href="#ri-mark"/></svg>
  <div class="wrap phero__in">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol>
          {crumbs}
      </ol>
    </nav>
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
</section>
"""


# ---------------------------------------------------------------- CTA + footer
CTA = f"""
<section class="cta">
  <svg class="mark-wm" viewBox="0 0 343.15 350" aria-hidden="true"><use href="#ri-mark"/></svg>
  <div class="wrap cta__in">
    <div class="riseL">
      <h2>Ready to find your next machine?</h2>
      <p>Live stock, full specifications and current prices are on our eBay store.</p>
    </div>
    <a class="btn btn--green riseR" href="{EBAY}" target="_blank" rel="noopener">
          <span>Visit The eBay Store</span> <span class="arw" aria-hidden="true">&#8599;</span>
    </a>
  </div>
</section>
"""


def footer():
    return FTR + FTR_TAIL


def write(slug, html):
    open(slug, "w", encoding="utf-8").write(html)
    print("  wrote", slug)


# ======================================================================
#  SHARED BLOCKS
# ======================================================================
RANGES = [
    ("Laptops", CAT["laptops"], "laptop",
     "Business-class ultrabooks and dependable everyday laptops from trusted brands.",
     ["Core i5 and i7 options", "SSD storage", "Tested and warranty-backed"], "laptops.jpg"),
    ("Desktop PCs", CAT["desktops"], "tower",
     "Reliable towers for home offices, study setups and busy workplaces.",
     ["Small-form and full tower", "Ready to plug in", "Upgrade paths available"], "desktop-pcs.jpg"),
    ("All-in-One PCs", EBAY, "aio",
     "Space-saving all-in-ones that keep desks tidy without compromising power.",
     ["One-piece design", "Ideal for reception desks", "Less cable clutter"], "all-in-one.jpg"),
    ("SSD &amp; Storage", CAT["accs"], "ssd",
     "Solid-state drives and hard drives to make old machines feel brand new.",
     ["SATA and NVMe drives", "Desktop and laptop sizes", "Instant speed boost"], "ssd-storage.jpg"),
    ("RAM &amp; Memory", CAT["accs"], "ram",
     "Memory upgrades that add speed and multitasking headroom for less.",
     ["DDR3, DDR4 and DDR5", "Laptop SODIMM and desktop", "Cheapest useful upgrade"], "ram-memory.jpg"),
    ("Accessories &amp; Cables", CAT["accs"], "acc",
     "Chargers, docks, cables and the essential add-ons for your setup.",
     ["Power adapters", "Docking stations", "Cables and adapters"], "accessories-cables.jpg"),
]

ICONS = {
 "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20l-1.5-3h-17z"/>',
 "tower":  '<rect x="6" y="3" width="12" height="18" rx="1.5"/><path d="M9 7h6M9 11h6"/><circle cx="15" cy="16.5" r="1.2"/>',
 "aio":    '<rect x="2.5" y="4" width="19" height="12" rx="2"/><path d="M9 20h6M12 16v4"/>',
 "ssd":    '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 10h4M7 14h8"/>',
 "ram":    '<rect x="2.5" y="8" width="19" height="8" rx="1.5"/><path d="M6 16v3M10 16v3M14 16v3M18 16v3"/>',
 "acc":    '<path d="M6 8V5.5a2.5 2.5 0 015 0V8M13 8V5.5a2.5 2.5 0 015 0V8"/><rect x="4" y="8" width="16" height="7" rx="2"/><path d="M12 15v4"/>',
}

def range_card(name, url, icon, blurb, bullets, pic):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return f"""      <a class="cat rise" href="{url}" target="_blank" rel="noopener">
        <div class="cat__img">
          <!-- REPLACE: swap the picsum src for the client's own photo -->
          <img class="photo" src="images/products/{pic}" alt="{name}" loading="lazy" width="800" height="500" onerror="this.remove()">
          <svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{name}">
            <defs><linearGradient id="g{icon}" x1="0" y1="0" x2="1" y2="1">
              <stop stop-color="#23934F"/><stop offset="1" stop-color="#0C3020"/></linearGradient></defs>
            <rect width="800" height="500" fill="url(#g{icon})"/>
            <circle cx="640" cy="90" r="150" fill="#4CC47E" opacity=".16"/>
            <g stroke="#B0E5C6" stroke-width="2.5" opacity=".3" fill="none">
              <path d="M40 120h80l26 26h120M40 380h60l30-30h120"/></g>
            <g transform="translate(280,110) scale(10)" fill="none" stroke="#E9EFEC" stroke-width="1.6"
               stroke-linejoin="round" stroke-linecap="round">{ICONS[icon]}</g>
          </svg>
        </div>
        <div class="cat__body">
          <div class="cat__ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round">{ICONS[icon]}</svg></div>
          <h3>{name}</h3>
          <p>{blurb}</p>
          <ul>{lis}</ul>
          <span class="cat__go">View on eBay <span class="arw" aria-hidden="true">&#8599;</span></span>
        </div>
      </a>
"""

TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<circle cx="12" cy="12" r="10"/><path d="M8 12.5l2.5 2.5L16 9.5"/></svg>')

def ticks(items):
    return "\n".join(f"      <li>{TICK} {i}</li>" for i in items)

REVIEWS = [
  ("James C.", "Verified buyer",
   "From the speed of the replies to how quickly it arrived, it couldn't have been better. "
   "The laptop performed better than I expected from a refurbished machine — everything in "
   "full working order and well packaged."),
  ("Sara R.", "Verified buyer",
   "Brilliant value and honest grading. The desktop was exactly as described, set up in "
   "minutes and has been rock solid for months. I've since recommended them to two colleagues."),
  ("Michael P.", "Verified buyer",
   "Ordered an SSD upgrade and it turned up next day, perfectly packed. Great communication "
   "and a fair price. This is now my go-to seller for anything tech related."),
]

def review_cards(cls_first="riseL"):
    out = []
    for i,(name, role, text) in enumerate(REVIEWS):
        cls = ["riseL","rise","riseR"][i % 3]
        out.append(f"""      <div class="rev {cls}">
        <div class="rev__st" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p>{text}</p>
        <b>{name} &middot; {role}</b>
      </div>""")
    return "\n".join(out)

POSTS = [
  ("choosing-a-refurbished-laptop.html", "How to choose the right refurbished laptop",
   "Buying Guide", "4 min", "choosing-a-laptop",
   "Processor, memory, storage and screen — the four things that actually matter, and how to "
   "match them to what you do all day.",
   [("Start with what you actually do",
     ["The specification you need depends far more on your workload than on the year the machine "
      "was made. A three-year-old business laptop will handle email, documents, spreadsheets and "
      "a browser full of tabs without complaint.",
      "Video editing, CAD or modern gaming are the exceptions. Everything else is comfortably "
      "within reach of refurbished kit at a fraction of the price."]),
    ("Processor",
     ["An Intel Core i5 is the sweet spot for most people. An i7 is worth it if you regularly run "
      "heavy spreadsheets, virtual machines or lots of applications at once.",
      "Check the generation as well as the number — a newer i5 usually beats an older i7."]),
    ("Memory",
     ["8GB is a workable minimum. 16GB is the comfortable answer and is what we would recommend "
      "if you keep a lot of browser tabs open.",
      "Memory is also the cheapest upgrade to add later, so it is not worth overpaying for at "
      "the point of purchase."]),
    ("Storage",
     ["Insist on an SSD. A solid-state drive is the single biggest difference between a machine "
      "that feels fast and one that feels tired, regardless of the processor.",
      "256GB suits most people. Go to 512GB if you store photos or large files locally."]),
    ("Screen and condition",
     ["Our condition grades describe cosmetic appearance only. A Grade C machine performs exactly "
      "the same as a Grade A one — it just has more visible marks, and costs less.",
      "If the laptop will sit on your own desk rather than in front of clients, Grade B or C is "
      "usually the best value in the range."])]),

  ("ssd-vs-hdd.html", "SSD vs HDD: which upgrade is worth it?",
   "Upgrades", "3 min", "ssd-vs-hdd",
   "A solid-state drive is usually the single biggest speed jump you can give an older machine. "
   "Here is why, and when a hard drive still makes sense.",
   [("The difference in practice",
     ["A hard drive stores data on a spinning platter and reads it with a moving arm. An SSD has "
      "no moving parts at all, so it finds data almost instantly.",
      "In everyday use that means a machine that boots in seconds rather than minutes, and "
      "applications that open the moment you click them."]),
    ("Why it beats other upgrades",
     ["On an older laptop, swapping a hard drive for an SSD usually makes more difference than "
      "adding memory or changing the processor would.",
      "It is also the cheapest of the three, and the easiest to fit."]),
    ("When a hard drive still makes sense",
     ["Bulk storage. If you need several terabytes for photos, video or backups, a hard drive "
      "gives you far more space per pound.",
      "The common approach is both: an SSD for the operating system and applications, and a hard "
      "drive alongside it for files."]),
    ("What to look for",
     ["Check whether your machine takes a 2.5in SATA drive or an M.2 NVMe drive. NVMe is faster, "
      "but only fits machines designed for it.",
      "If you are unsure which your laptop takes, send us the model number and we will tell you."])]),

  ("grading-explained.html", "What our A / B / C grading really means",
   "Explained", "2 min", "grading-explained",
   "Grading describes cosmetic condition only. Whatever the grade, the machine is tested to the "
   "same standard and carries the same warranty.",
   [("Grading is about looks, not performance",
     ["This is the point people most often misunderstand. A grade tells you how a machine looks — "
      "how much wear is on the casing and screen. It says nothing about how it runs.",
      "Every machine we sell passes the same diagnostics before it is listed, whatever letter "
      "ends up on it."]),
    ("Grade A — Excellent",
     ["Little to no visible wear. The kind of machine you would be happy to hand straight to a "
      "client or put in front of a customer."]),
    ("Grade B — Good",
     ["Small scratches or scuffs on the casing from normal use. The screen is clear and unmarked. "
      "This is the most popular grade, and usually the best balance of price and appearance."]),
    ("Grade C — Fair",
     ["Noticeable scratches, scuffs or dents. Priced accordingly, and the best value in the range "
      "if the machine is going to sit on your own desk."]),
    ("What every grade includes",
     ["Full diagnostics, storage securely wiped, a clean operating system, and a 12-month "
      "warranty. None of that changes with the grade."])]),

  ("why-refurbished-is-greener.html", "Why refurbished tech is the greener choice",
   "Sustainability", "3 min", "greener-choice",
   "Manufacturing a new laptop carries a far bigger footprint than the electricity it will ever "
   "use. Reuse beats recycling, every time.",
   [("Most of the impact happens before you switch it on",
     ["For a typical laptop, the majority of its lifetime carbon footprint comes from "
      "manufacturing — mining the materials, making the components and shipping it across the "
      "world — not from the power it draws afterwards.",
      "That means the greenest machine is almost always one that already exists."]),
    ("Reuse beats recycling",
     ["Recycling recovers some materials, but it is energy-intensive and a lot is lost in the "
      "process. Extending the working life of a machine avoids that step entirely.",
      "A laptop that gets a second five years of use has effectively halved its footprint per "
      "year of service."]),
    ("It is not a trade-off",
     ["Choosing refurbished does not mean accepting less. Business-class machines are built to a "
      "higher standard than budget consumer kit, and they arrive barely used.",
      "You get better hardware, a lower price and a smaller footprint at the same time."])]),
]

def post_cards(limit=None):
    items = POSTS[:limit] if limit else POSTS
    out = []
    for slug, title, tag, mins, pic, blurb, _sections in items:
        out.append(f"""      <article class="post rise">
        <a class="post__img" href="{slug}" aria-hidden="true" tabindex="-1">
          <span class="post__tag">{tag}</span>
          <!-- REPLACE: swap the picsum src for a real photo -->
          <img src="images/blog/{pic}-card.jpg" alt="" loading="lazy" width="800" height="500">
        </a>
        <div class="post__body">
          <p class="post__meta">Aug 2026 &middot; {mins} read</p>
          <h3><a href="{slug}">{title}</a></h3>
          <p>{blurb}</p>
          <a class="post__go" href="{slug}">Read more <span class="arw" aria-hidden="true">&#8599;</span></a>
        </div>
      </article>""")
    return "\n".join(out)


GRADES = """
    <div class="gcards">
      <div class="gcard riseL">
        <span class="gcard__l"><b>A</b><span>Excellent</span></span>
        <h3>Looks close to new</h3>
        <p>Little to no visible wear. The kind of machine you would be happy to hand straight to a client.</p>
      </div>
      <div class="gcard rise">
        <span class="gcard__l"><b>B</b><span>Good</span></span>
        <h3>Light cosmetic wear</h3>
        <p>Small scratches or scuffs on the casing from normal use. Screen clear and unmarked.</p>
      </div>
      <div class="gcard riseR">
        <span class="gcard__l"><b>C</b><span>Fair</span></span>
        <h3>Visible marks</h3>
        <p>Noticeable scratches, scuffs or dents. Priced accordingly — the best value in the range.</p>
      </div>
    </div>

    <div class="gnote zoom">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l8 4v6c0 5-3.4 8.6-8 10-4.6-1.4-8-5-8-10V6z"/><path d="M9 12l2 2 4-4.5"/></svg>
      <div>
        <b>Applies to every grade</b>
        <p>Grading describes cosmetic condition only. Whatever the grade, the machine has passed the
           same diagnostics, had its storage securely wiped, and carries the same 12-month warranty.</p>
      </div>
    </div>
"""


# ======================================================================
#  PAGES
# ======================================================================
def page_home():
    body = '\n<main id="main">\n' + open("_home-body.html", encoding="utf-8").read() + '\n</main>\n'
    return head("Refurbished Laptops, PCs &amp; Accessories in Birmingham | " + BRAND,
                "Quality refurbished laptops, desktop PCs and accessories at competitive prices. "
                "Quality guaranteed, backed for a year, dispatched from Birmingham.",
                "index.html", pre=True) + header() + body + footer()


def page_products():
    ld = ('{"@context":"https://schema.org","@type":"ItemList","name":"Refurbished IT ranges",'
          '"itemListElement":[' + ",".join(
            '{"@type":"ListItem","position":%d,"name":"%s","url":"%s"}'
            % (i+1, r[0].replace("&amp;","&"), r[1]) for i, r in enumerate(RANGES)) + ']}')
    body = f"""
{banner("Refurbished IT Equipment",
        "High-quality laptops, desktops, all-in-ones, storage, memory and accessories — "
        "all tested, graded and sold through our eBay store.",
        [("Home","index.html"),("Products",None)])}
<main id="main">

<section class="band">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Our range</span>
      <h2>Six ranges, one standard.</h2>
      <p>Stock changes constantly. Live availability, full specifications and current prices are
         always on our eBay store — these pages tell you what to expect before you get there.</p>
    </div>
    <div class="range">
{"".join(range_card(*r) for r in RANGES[:3])}    </div>
    <div class="range" style="margin-top:24px">
{"".join(range_card(*r) for r in RANGES[3:])}    </div>
  </div>
</section>

<section class="band grades" id="grading" style="background:var(--white)">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Condition grading</span>
      <h2>You know what you are getting before you buy.</h2>
      <p>Every listing states its grade. The grade describes the casing and screen only — never the performance.</p>
    </div>
{GRADES}
  </div>
</section>

<section class="band why">
  <div class="wrap split">
    <div class="riseL">
      <div class="head" style="margin-bottom:0">
        <span class="eyebrow">What is included</span>
        <h2>Every order, whatever the range.</h2>
        <p>The same standard applies from a £40 memory upgrade to a top-end workstation.</p>
      </div>
      <ul class="ticks">
{ticks(["12-month warranty", "Multi-point diagnostics", "Storage securely wiped",
        "Clean operating system", "Honest cosmetic grading", "Securely packed for transit"])}
      </ul>
    </div>
    <div class="panel panel--dark riseR">
      <h3 style="font-size:26px;margin-bottom:14px">Need a specific build?</h3>
      <p style="margin-bottom:24px">Tell us the processor, memory and storage you are after — or just
         describe what you need the machine to do. If we do not have it listed, we will look out for it.</p>
      <a class="btn btn--green" href="contact.html">
          <span>Talk To Us</span> <span class="arw" aria-hidden="true">&#8599;</span></a>
    </div>
  </div>
</section>

{CTA}
</main>
"""
    return head("Refurbished Laptops, Desktop PCs, SSDs &amp; RAM | " + BRAND,
                "Browse our refurbished IT ranges: business laptops, desktop PCs, all-in-ones, SSD "
                "storage, memory upgrades and accessories. Tested, graded and warranty-backed.",
                "products.html", ld) + header() + body + footer()


def page_about():
    ld = crumb_ld([("Home","index.html"),("About","about.html")])
    body = f"""
{banner("About " + BRAND,
        "One of the most reputable refurbished tech sellers in the UK, working out of "
        "Metro Triangle in Birmingham.",
        [("Home","index.html"),("About",None)])}
<main id="main">

<section class="band">
  <div class="wrap split">
    <div class="riseL">
      <div class="head" style="margin-bottom:0">
        <span class="eyebrow">Who we are</span>
        <h2>Refurbished tech, done properly.</h2>
        <p>We specialise in high-quality refurbished IT equipment, offering a wide range of products
           at competitive prices — so you can meet all your technology needs with complete confidence.</p>
        <p style="margin-top:16px">Everything we sell is restored to full working order in-house,
           tested against a full component list and graded honestly before it is listed. No surprises
           when the box arrives.</p>
      </div>
      <ul class="ticks">
{ticks(["Expert testing", "Honest grading", "Quick dispatch", "Buyer-first approach"])}
      </ul>
    </div>
    <div class="panel riseR">
      <h3 style="font-size:24px;margin-bottom:24px">By the numbers</h3>
      <!-- CONFIRM these percentages with the client. -->
      <div class="bars">
        <div>
          <div class="bar__top"><span>Positive feedback</span><b>100%</b></div>
          <div class="bar__track"><span class="bar__fill" data-pct="100"></span></div>
        </div>
        <div>
          <div class="bar__top"><span>Repeat &amp; returning buyers</span><b>90%</b></div>
          <div class="bar__track"><span class="bar__fill" data-pct="90"></span></div>
        </div>
        <div>
          <div class="bar__top"><span>Orders dispatched on time</span><b>96%</b></div>
          <div class="bar__track"><span class="bar__fill" data-pct="96"></span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="stats">
  <svg class="mark-wm" viewBox="0 0 343.15 350" aria-hidden="true"><use href="#ri-mark"/></svg>
  <div class="wrap stats__in">
    <div class="stat rise"><b class="num" data-to="5400" data-suffix="+">0</b><span>Orders delivered</span></div>
    <div class="stat rise"><b class="num" data-to="100" data-suffix="%">0</b><span>Positive feedback</span></div>
    <div class="stat rise"><b class="num" data-to="12" data-suffix=" mo">0</b><span>Warranty as standard</span></div>
  </div>
</section>

<section class="band why">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Why choose us</span>
      <h2>Trusted refurbished tech, thousands of happy buyers.</h2>
      <p>Our reputation is built on doing the simple things well: rigorous testing, honest grading,
         fair prices and fast, reliable delivery — order after order.</p>
    </div>
    <div class="whys">
      <div class="wcard rise">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3.5v5c0 4.6-3 7.9-7 9.2-4-1.3-7-4.6-7-9.2v-5z"/><path d="M9 12l2 2 4.5-5"/></svg>
        <h3>Trusted UK seller</h3>
        <p>A strong feedback record across thousands of completed orders on eBay.</p>
      </div>
      <div class="wcard rise">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="18" height="14" rx="2"/><path d="M8 6V4h8v2M9 13l2 2 4-4"/></svg>
        <h3>Warranty backed</h3>
        <p>Every machine is covered by a genuine 12-month warranty as standard.</p>
      </div>
      <div class="wcard rise">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21c5-2.4 8-6 8-11 0-3-2-5.5-4.5-5.5-1.6 0-2.8.9-3.5 2-.7-1.1-1.9-2-3.5-2C6 4.5 4 7 4 10c0 5 3 8.6 8 11z"/></svg>
        <h3>Greener by default</h3>
        <p>Every machine given a second life is one fewer manufactured, and one fewer in a skip.</p>
      </div>
      <div class="wcard rise">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.3 7-11a7 7 0 10-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>
        <h3>A real UK business</h3>
        <p>{LEGAL}, a registered company based at Metro Triangle in Birmingham.</p>
      </div>
    </div>
  </div>
</section>

{CTA}
</main>
"""
    return head("About Us — Refurbished IT Specialists in Birmingham | " + BRAND,
                "We restore quality laptops, desktops and accessories to full working order. "
                "Tested, honestly graded and warranty-backed, from our base in Birmingham.",
                "about.html", ld) + header() + body + footer()


FAQS = [
 ("What does refurbished actually mean here?",
  "Every machine is stripped down, cleaned, repaired where needed and put through a full "
  "diagnostic before it is listed. It is not simply wiped and resold."),
 ("Is my data safe on a machine you have refurbished?",
  "Yes. Storage is securely wiped before a clean operating system is installed, so nothing "
  "from the previous owner remains."),
 ("What does the A / B / C grade refer to?",
  "Cosmetic condition only — the casing and screen. Performance is not graded, because every "
  "machine has to pass the same tests regardless of how it looks."),
 ("How long is the warranty?",
  "Twelve months on every machine, whatever the grade."),
 ("Where do you ship from?",
  "Our base at Metro Triangle in Birmingham. Orders are packed securely and tracked."),
]

def faq_ld():
    items = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (q.replace('"','\\"'), a.replace('"','\\"')) for q, a in FAQS)
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % items


def page_process():
    body = f"""
{banner("How We Refurbish",
        "A simple, disciplined cycle stands behind every device we sell — source, refurbish, grade, ship.",
        [("Home","index.html"),("Process",None)])}
<main id="main">

<section class="band">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Our process</span>
      <h2>How we work.</h2>
      <p>Three stages, in order, on every unit that comes through the door.</p>
    </div>
    <div class="steps" style="grid-template-columns:repeat(3,1fr)">
      <div class="stp rise"><b>01</b><h3>Source &amp; inspect</h3>
        <p>Quality stock is selected and checked against a full component list before anything else happens.</p></div>
      <div class="stp rise"><b>02</b><h3>Refurbish &amp; test</h3>
        <p>Cleaned, repaired and put through full performance and battery diagnostics until it behaves like new.</p></div>
      <div class="stp rise"><b>03</b><h3>Grade &amp; ship</h3>
        <p>Honestly graded, warranty-backed and dispatched fast, packed securely for transit.</p></div>
    </div>
  </div>
</section>

<section class="band why">
  <div class="wrap split">
    <div class="riseL">
      <div class="head" style="margin-bottom:0">
        <span class="eyebrow">Fully refurbished</span>
        <h2>Every device, checked and restored properly.</h2>
        <p>Refurbished doesn't mean second-best. Each machine is stripped down, cleaned, repaired and
           tested until it performs like new — then honestly graded so you know exactly what you are getting.</p>
      </div>
      <ul class="ticks">
{ticks(["Multi-point diagnostics", "Storage securely wiped",
        "Worn parts replaced", "Honest A / B / C grading",
        "Clean operating system", "Securely packed for transit"])}
      </ul>
      <p style="margin-top:28px"><a class="btn btn--out" href="contact.html">
          <span>Talk To Us</span> <span class="arw" aria-hidden="true">&#8599;</span></a></p>
    </div>
    <div class="panel panel--dark riseR">
      <h3 style="font-size:26px;margin-bottom:16px">What we check</h3>
      <ul class="ticks" style="grid-template-columns:1fr;color:#fff">
{ticks(["Battery health and charge cycles", "Screen for dead pixels and marks",
        "Every keyboard key and the trackpad", "All ports, wireless and Bluetooth",
        "Storage health and read/write speed", "Fans, vents and running temperatures"])}
      </ul>
    </div>
  </div>
</section>

<section class="band grades" style="background:var(--white)">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Condition grading</span>
      <h2>What our A / B / C grades mean.</h2>
      <p>Grading is about appearance, not performance. Here is exactly what each letter tells you.</p>
    </div>
{GRADES}
  </div>
</section>

<section class="band why">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Questions</span>
      <h2>Frequently asked.</h2>
      <p>If your question is not here, send us a message and we will answer it properly.</p>
    </div>
    <div class="faq rise">
{"".join('      <details><summary>%s</summary><p>%s</p></details>%s' % (q, a, chr(10)) for q, a in FAQS)}
    </div>
  </div>
</section>

{CTA}
</main>
"""
    return head("Our Refurbishment Process &amp; Grading Explained | " + BRAND,
                "How we refurbish: source and inspect, refurbish and test, grade and ship. Plus what "
                "our A, B and C condition grades actually mean.",
                "process.html", faq_ld()) + header() + body + footer()


def page_reviews():
    ld = crumb_ld([("Home","index.html"),("Reviews","reviews.html")])
    body = f"""
{banner("Customer Reviews",
        "A snapshot of the feedback behind our rating — the full record is public on our eBay store.",
        [("Home","index.html"),("Reviews",None)])}
<main id="main">

<section class="band reviews" style="padding-block:clamp(56px,7vw,96px)">
  <svg class="mark-wm" viewBox="0 0 343.15 350" aria-hidden="true"><use href="#ri-mark"/></svg>
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Client stories</span>
      <h2>Trusted by thousands of satisfied buyers.</h2>
      <p>These are real comments from buyers. Every listing we sell is backed by the same warranty
         and the same grading standard.</p>
    </div>
    <div class="revs">
{review_cards()}
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div class="riseL">
      <div class="head" style="margin-bottom:0">
        <span class="eyebrow">Our record</span>
        <h2>Reputation, measured.</h2>
        <p>We would rather show the numbers than talk about them. All feedback is public and
           verifiable on our eBay store.</p>
      </div>
      <p style="margin-top:28px"><a class="btn btn--out" href="{EBAY}" target="_blank" rel="noopener">
          <span>See Our eBay Feedback</span> <span class="arw" aria-hidden="true">&#8599;</span></a></p>
    </div>
    <div class="panel riseR">
      <!-- CONFIRM these percentages with the client. -->
      <div class="bars">
        <div>
          <div class="bar__top"><span>Positive feedback</span><b>100%</b></div>
          <div class="bar__track"><span class="bar__fill" data-pct="100"></span></div>
        </div>
        <div>
          <div class="bar__top"><span>Repeat &amp; returning buyers</span><b>90%</b></div>
          <div class="bar__track"><span class="bar__fill" data-pct="90"></span></div>
        </div>
        <div>
          <div class="bar__top"><span>Orders dispatched on time</span><b>96%</b></div>
          <div class="bar__track"><span class="bar__fill" data-pct="96"></span></div>
        </div>
      </div>
    </div>
  </div>
</section>

{CTA}
</main>
"""
    return head("Customer Reviews &amp; eBay Feedback | " + BRAND,
                "Read what buyers say about our refurbished laptops, desktops and upgrades — "
                "honest grading, fast dispatch and a 12-month warranty on every order.",
                "reviews.html", ld) + header() + body + footer()


def page_blog():
    ld = crumb_ld([("Home","index.html"),("Blog","blog.html")])
    body = f"""
{banner("Guides &amp; Tech Tips",
        "Straight answers to the questions buyers ask us most — what to look for, what to upgrade, "
        "and what refurbished really means.",
        [("Home","index.html"),("Blog",None)])}
<main id="main">

<section class="band">
  <div class="wrap">
    <!-- REPLACE: these four cards are placeholders. Write the posts, then link each card
         to its own page (e.g. blog/choosing-a-refurbished-laptop.html). If the client is
         not going to publish regularly, remove this page and the Blog nav link instead —
         an empty blog does more harm than no blog. -->
    <div class="posts">
{post_cards()}
    </div>
  </div>
</section>

{CTA}
</main>
"""
    return head("Refurbished Tech Guides &amp; Buying Advice | " + BRAND,
                "Buying guides, upgrade advice and plain-English explanations of refurbished "
                "grading — from the team that refurbishes the machines.",
                "blog.html", ld) + header() + body + footer()


# ======================================================================
#  RUNNER
# ======================================================================
PAGES = {
    "index.html":    page_home,
    "products.html": page_products,
    "about.html":    page_about,
    "process.html":  page_process,
    "reviews.html":  page_reviews,
    "blog.html":     page_blog,
}



def page_contact():
    ld = ('{"@context":"https://schema.org","@type":"LocalBusiness",'
          '"@id":"%s/#localbusiness","name":"%s","image":"%s/images/social/og-image.jpg",'
          '"url":"%s/contact.html","email":"%s","priceRange":"££",'
          '"address":{"@type":"PostalAddress","streetAddress":"%s, Mount Street",'
          '"addressLocality":"Birmingham","postalCode":"%s","addressCountry":"GB"},'
          '"openingHoursSpecification":[{"@type":"OpeningHoursSpecification",'
          '"dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],'
          '"opens":"09:00","closes":"18:00"}]}'
          % (SITE, BRAND, SITE, SITE, EMAIL, ADDR1, POST))

    body = f"""
{banner("Contact Us",
        "Bulk orders, a particular specification, or a question about a listing — "
        "send us a note and we will come back to you.",
        [("Home","index.html"),("Contact",None)])}
<main id="main">

<section class="band">
  <div class="wrap cgrid">
    <div class="riseL">
      <div class="head" style="margin-bottom:32px">
        <span class="eyebrow">Get in touch</span>
        <h2>We reply within one working day.</h2>
        <p>Tell us the model, specification or quantity you are after — or just describe what you
           need the machine to do, and we will point you the right way.</p>
      </div>
      <ul class="infos">
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>
          <div><b>Sales</b><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
        </li>
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>
          <div><b>General enquiries</b><span><a href="mailto:{EMAIL2}">{EMAIL2}</a></span></div>
        </li>
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 21s7-6.3 7-11a7 7 0 10-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>
          <div><b>Address</b><span>{ADDR1}, {ADDR2} {POST}</span></div>
        </li>
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5.5l3.5 2"/></svg>
          <div><b>Opening hours</b><span>{HOURS}</span></div>
        </li>
        <li style="border-bottom:0">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M4 7h16v13H4z"/><path d="M4 11h16M9 7V4h6v3"/></svg>
          <div><b>Buy online</b><span><a href="{EBAY}" target="_blank" rel="noopener">Our eBay store &#8599;</a></span></div>
        </li>
      </ul>
    </div>

    <form class="form riseR" action="https://formsubmit.co/ajax/sales@essentialtechgb.co.uk" method="POST">
      <input type="hidden" name="_subject" value="New enquiry from the {BRAND} website">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_captcha" value="false">
      <input type="text" name="_honey" style="display:none" tabindex="-1" aria-hidden="true" autocomplete="off">

      <div class="field"><label for="f1">Your name</label>
        <input id="f1" name="name" type="text" required autocomplete="name"></div>
      <div class="field"><label for="f2">Email address</label>
        <input id="f2" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="f3">Phone (optional)</label>
        <input id="f3" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="f4">What are you looking for?</label>
        <textarea id="f4" name="message" required placeholder="Model, specification, quantity — whatever you know."></textarea></div>
      <button class="btn btn--out" type="submit"><span>Send Enquiry</span> <span class="arw" aria-hidden="true">&#8599;</span></button>
      <p class="fmsg" role="status" aria-live="polite" hidden></p>
      <p class="fnote">We reply within one working day. Your details are only used to answer your enquiry.</p>
    </form>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="head rise" style="max-width:none">
      <span class="eyebrow">Find us</span>
      <h2>{ADDR1}, Birmingham.</h2>
    </div>
    <iframe class="map rise" title="Map showing {ADDR1}, Mount Street, Birmingham {POST}"
      src="https://www.google.com/maps?q={ADDR1.replace(' ','+')}+Mount+Street+Birmingham+{POST}&amp;output=embed"
      loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
</section>

{CTA}
</main>
"""
    return head("Contact Us — Refurbished IT in Birmingham | " + BRAND,
                "Get in touch about refurbished laptops, desktops or upgrades. Based at Metro "
                "Triangle, Birmingham. We reply within one working day.",
                "contact.html", ld) + header() + body + footer()


PAGES["contact.html"] = page_contact




# ----------------------------------------------------------------- legal pages
LEGAL_NOTE = """
    <div class="gnote zoom" style="margin-bottom:36px">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9L2.4 17.5A2 2 0 004.1 20.5h15.8a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z"/></svg>
      <div>
        <b>Draft — have this checked</b>
        <p>This is a starting template, not legal advice. Have a UK solicitor or an online
           policy generator review it against how the business actually handles data before
           the site goes live.</p>
      </div>
    </div>
"""

def legal_page(slug, h1, intro, sections):
    blocks = ""
    for heading, paras in sections:
        blocks += "      <h2 style=\"font-size:26px;margin:38px 0 14px\">%s</h2>\n" % heading
        for para in paras:
            blocks += "      <p style=\"color:var(--body-c);margin-bottom:14px\">%s</p>\n" % para
    body = """
%s
<main id="main">
<section class="band">
  <div class="wrap" style="max-width:860px">
%s
%s
  </div>
</section>
</main>
""" % (banner(h1, intro, [("Home","index.html"),(h1,None)]), LEGAL_NOTE, blocks)
    return head(h1 + " | " + BRAND, intro,
                slug, crumb_ld([("Home","index.html"),(h1,slug)])) + header() + body + footer()


def page_privacy():
    return legal_page("privacy.html", "Privacy Policy",
      "How %s collects, uses and protects your personal information." % BRAND, [
      ("Who we are", [
        "%s is a trading name of %s, registered in England and Wales (company number [ADD COMPANY NUMBER]), "
        "with its registered office at %s, %s %s." % (BRAND, LEGAL, ADDR1, ADDR2, POST),
        "For any question about this policy or your data, email <a href=\"mailto:%s\">%s</a>." % (EMAIL, EMAIL)]),
      ("What we collect", [
        "When you use the contact form we collect your name, email address, and any phone number "
        "or message you choose to give us. That is all we ask for.",
        "Our hosting provider records standard technical information such as IP address and browser "
        "type as part of serving the site. We do not use this to identify you."]),
      ("Why we use it", [
        "Solely to answer your enquiry and, where relevant, to fulfil an order. We do not sell your "
        "information, and we do not add you to a marketing list without asking first.",
        "The lawful basis is legitimate interest — responding to someone who has contacted us — or "
        "the performance of a contract where you have placed an order."]),
      ("How long we keep it", [
        "Enquiry emails are kept for up to 24 months so we can refer back to previous conversations. "
        "Order records are kept for six years, as UK tax law requires."]),
      ("Sharing", [
        "Purchases are completed through eBay, which operates its own privacy policy covering that "
        "part of the transaction. Contact form messages are delivered by our form provider and go "
        "straight to our inbox.",
        "We do not share your details with anyone else except where the law requires it."]),
      ("Your rights", [
        "Under UK GDPR you can ask for a copy of the data we hold about you, ask us to correct it, "
        "or ask us to delete it. Email us and we will respond within one month.",
        "If you are unhappy with how we have handled your data you can complain to the Information "
        "Commissioner's Office at ico.org.uk."]),
      ("Changes", [
        "If this policy changes we will update this page and change the date below.",
        "Last updated: [ADD DATE]."]),
      ])


def page_terms():
    return legal_page("terms.html", "Terms of Use",
      "The terms on which you may use the %s website." % BRAND, [
      ("These terms", [
        "By using this website you accept these terms. If you do not accept them, please do not use the site.",
        "The site is operated by %s, registered in England and Wales (company number [ADD COMPANY NUMBER])." % LEGAL]),
      ("What this site is", [
        "This website describes what we sell and how we work. Purchases are not completed here — every "
        "sale is made through our eBay store, and eBay's own terms, buyer protection and returns process "
        "apply to that transaction.",
        "Prices, specifications and availability shown on eBay are the authoritative ones."]),
      ("Accuracy", [
        "We take care to keep the information here accurate, but it is provided for general guidance. "
        "Specifications and condition grades for a particular item are set out in full on its eBay listing.",
        "Condition grading describes cosmetic appearance. It does not describe performance, which is "
        "tested to the same standard for every item regardless of grade."]),
      ("Warranty", [
        "Our warranty covers hardware faults arising in normal use for twelve months from delivery. It "
        "does not cover accidental damage, liquid damage, or faults caused by modification.",
        "This does not affect your statutory rights as a consumer under UK law. [CONFIRM the exact "
        "warranty terms with the client and replace this paragraph.]"]),
      ("Intellectual property", [
        "The design, text, logo and graphics on this site belong to us and may not be reproduced without "
        "permission. Brand names of manufacturers remain the property of their respective owners."]),
      ("Liability", [
        "We do not exclude liability for death, personal injury or fraud. Otherwise our liability in "
        "connection with this website is limited to the value of any order placed with us."]),
      ("Governing law", [
        "These terms are governed by the law of England and Wales, and the courts of England and Wales "
        "have exclusive jurisdiction."]),
      ])


def page_cookies():
    return legal_page("cookies.html", "Cookie Policy",
      "What this website stores on your device, and what it does not." % () or
      "What this website stores on your device, and what it does not.", [
      ("The short version", [
        "This website does not set any tracking or advertising cookies. There is no analytics script "
        "and no advertising pixel, so there is nothing to consent to.",
        "[CONFIRM: this stays true only while no analytics is added. If Google Analytics, Meta Pixel "
        "or similar goes on the site, this page must change and a consent banner becomes a legal "
        "requirement in the UK.]"]),
      ("Third-party content", [
        "The contact page embeds a Google Map. Google may set cookies when that map loads. If you would "
        "rather avoid that, the map can be replaced with a static image and a link.",
        "Fonts are loaded from Google Fonts. These can be moved onto our own server to remove that "
        "request entirely — see images/FONTS-README.txt in the site files."]),
      ("Buying on eBay", [
        "When you follow a link to our eBay store you leave this website. eBay sets its own cookies and "
        "operates its own privacy and cookie policies."]),
      ("Controlling cookies", [
        "Every major browser lets you block or delete cookies through its settings. Doing so will not "
        "stop this site working."]),
      ("Changes", [
        "Last updated: [ADD DATE]."]),
      ])


PAGES["privacy.html"] = page_privacy
PAGES["terms.html"]   = page_terms
PAGES["cookies.html"] = page_cookies



# ----------------------------------------------------------------- blog posts
def make_post(slug, title, tag, mins, pic, blurb, sections):
    def fn():
        ld = ('{"@context":"https://schema.org","@type":"BlogPosting",'
              '"headline":"%s","description":"%s","datePublished":"2026-08-01",'
              '"author":{"@id":"%s/#organization"},"publisher":{"@id":"%s/#organization"},'
              '"mainEntityOfPage":"%s/%s"}' % (title, blurb.replace('"',"'"), SITE, SITE, SITE, slug))
        blocks = ""
        for heading, paras in sections:
            blocks += "      <h2>%s</h2>\n" % heading
            for para in paras:
                blocks += "      <p>%s</p>\n" % para
        body = """
%s
<main id="main">
<section class="band">
  <div class="wrap">
    <article class="article rise">
      <div class="article__img">
        <!-- REPLACE: swap the picsum src for a real photo -->
        <img src="images/blog/%s-hero.jpg" alt="%s" width="1200" height="675" loading="eager" fetchpriority="high">
      </div>
      <p class="article__lead">%s</p>
%s
      <p style="margin-top:36px"><a class="btn btn--out" href="blog.html">
        <span>All Guides</span> <span class="arw" aria-hidden="true">&#8599;</span></a></p>
    </article>
  </div>
</section>
%s
</main>
""" % (banner(title, "%s &middot; %s read" % (tag, mins),
              [("Home","index.html"),("Blog","blog.html"),(tag,None)]),
       pic, title, blurb, blocks, CTA)
        return head(title + " | " + BRAND, blurb, slug, ld) + header() + body + footer()
    return fn


for _p in POSTS:
    PAGES[_p[0]] = make_post(*_p)


# ----------------------------------------------------------------- 404
def page_404():
    body = """
<main id="main">
<section class="band nf">
  <div class="wrap">
    <b>404</b>
    <div class="head" style="margin-inline:auto;text-align:center">
      <h1 style="font-size:clamp(28px,4vw,44px);margin-bottom:16px">This page has moved on.</h1>
      <p>The link may be out of date, or the page may have been renamed. Everything
         we sell is on our eBay store, and the main pages are below.</p>
    </div>
    <p style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;justify-content:center">
      <a class="btn btn--green" href="index.html"><span>Back To Home</span></a>
      <a class="btn btn--out" href="products.html"><span>Our Products</span></a>
      <a class="btn btn--out" href="contact.html"><span>Contact Us</span></a>
    </p>
  </div>
</section>
</main>
"""
    return head("Page not found | " + BRAND,
                "That page could not be found. Browse our refurbished laptops, desktop PCs "
                "and accessories, or get in touch.",
                "404.html").replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">',
        '<meta name="robots" content="noindex, follow">') + header() + body + footer()


PAGES["404.html"] = page_404


# ----------------------------------------------------------------- sitemap + manifest
def write_extras():
    import datetime
    today = datetime.date.today().isoformat()
    weight = {"index.html":("1.0","weekly"), "products.html":("0.9","weekly"),
              "contact.html":("0.8","monthly"), "about.html":("0.7","monthly"),
              "process.html":("0.7","monthly"), "blog.html":("0.6","weekly"),
              "reviews.html":("0.6","monthly")}
    rows = []
    for slug in PAGES:
        if slug == "404.html":
            continue
        pri, freq = weight.get(slug, ("0.5","monthly") if slug.endswith(".html") and
                                     slug not in ("privacy.html","terms.html","cookies.html")
                                     else ("0.2","yearly"))
        loc = SITE + "/" + ("" if slug == "index.html" else slug)
        rows.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
                    "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
                    % (loc, today, freq, pri))
    open("sitemap.xml","w",encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows) + "\n</urlset>\n")
    print("  wrote sitemap.xml (%d urls)" % len(rows))

    open("robots.txt","w",encoding="utf-8").write(
        "# %s\n# REPLACE the domain below if it changes.\n\n"
        "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % (BRAND, SITE))
    print("  wrote robots.txt")

    open("site.webmanifest","w",encoding="utf-8").write("""{
  "name": "%s — Refurbished IT Equipment",
  "short_name": "%s",
  "description": "Quality refurbished laptops, desktops and accessories from Birmingham.",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#141636",
  "theme_color": "#2FAF66",
  "icons": [
    { "src": "images/logo/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "images/logo/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "images/logo/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
""" % (BRAND, BRAND))
    print("  wrote site.webmanifest")

if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or list(PAGES)
    print("Building %s" % BRAND)
    for slug in only:
        if slug in PAGES:
            write(slug, PAGES[slug]())
        else:
            print("  ?? unknown page:", slug)
    write_extras()
    print("Done.")
