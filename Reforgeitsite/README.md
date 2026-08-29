# ReforgeIT — website

Plain HTML, CSS and JavaScript. No build step, no server code, no database.
Open `index.html` in a browser and the whole site works.

## Folder structure

```
index.html        Home
products.html     The six ranges + condition grading
about.html        Who we are, the numbers, why choose us
process.html      How we refurbish, what we check, grading, FAQ
reviews.html      Customer feedback
blog.html         Guides (placeholder cards for now)
contact.html      Contact form, details and map
privacy.html      \
terms.html         >  legal pages — drafts, get them checked
cookies.html      /

css/style.css     Every style on the site. Colours live at the very top.
js/main.js        Menu, slider, scroll animations, counters.
images/           Logo sprite + a README listing every photo still needed.
robots.txt        Tells search engines they may index the site.
sitemap.xml       Lists every page for search engines.
build.py          Optional. See below. Safe to delete.
```

## Making changes

**Colours** — open `css/style.css`. The first block is `:root`, which holds every
colour as a variable. Change `--g-500` and the green updates everywhere.

**Text** — edit the HTML file for that page directly.

**Photos** — see `images/README.txt`. Each slot currently shows a drawn SVG
placeholder so nothing looks broken; search a page for `REPLACE:` to find them.

**Menu, header, footer** — these repeat on all ten pages. Change them by hand in
each file, or use `build.py` (below) to do it once.

## build.py (optional)

Every page was generated from this script, so the header, footer and `<head>`
are identical everywhere. If you edit the menu or footer in `build.py` and run:

```
python3 build.py
```

…all ten pages are rewritten. **This overwrites the HTML files**, so if you have
hand-edited them, either stop using the script or move your edits into it first.

You can delete `build.py` and just edit the HTML by hand. Nothing depends on it.

## Before going live

1. Find and replace `https://www.reforgeit.co.uk` with the real domain, in every
   HTML file plus `robots.txt` and `sitemap.xml`.
2. Search all files for `REPLACE:` and `CONFIRM` and work through the list.
3. Get a free key at web3forms.com and paste it into the contact form, or the
   form will not send.
4. Add the Companies House registration number to the footer — a UK limited
   company is legally required to show it.
5. Add the real photos.
6. Submit `sitemap.xml` in Google Search Console.

## Hosting

Any static host works: Netlify, Cloudflare Pages, GitHub Pages, or normal shared
hosting. Upload the whole folder. No PHP, no database.
