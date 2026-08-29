IMAGES
======

Images are grouped by the part of the site they appear in:

  images/home/       the home page
  images/products/   the six range cards on products.html
  images/blog/       blog cards and article headers
  images/social/     the share preview
  images/logo/       every logo variant

TO REPLACE ONE
--------------
Drop your own photo in with THE SAME FILENAME and THE SAME PIXEL SIZE. Nothing
in the HTML needs editing. Each placeholder has its section, purpose and size
printed on it, so you can tell at a glance which is which.

WANT THE ORIGINAL STOCK PHOTOS BACK?
------------------------------------
The site used photos from picsum.photos before these files existed. To fetch
them, save the block below as get-photos.sh (Mac/Linux) and run it from inside
the images folder. On Windows, paste each URL into a browser and save it with
the matching filename.

  # --- HOME ---
  curl -L -o home/hero-background.jpg        "https://picsum.photos/id/180/1800/1100"
  curl -L -o home/hero-slide-1.jpg           "https://picsum.photos/id/0/900/900"
  curl -L -o home/hero-slide-2.jpg           "https://picsum.photos/id/2/900/900"
  curl -L -o home/hero-slide-3.jpg           "https://picsum.photos/id/119/900/900"
  curl -L -o home/category-laptops.jpg       "https://picsum.photos/id/0/800/500"
  curl -L -o home/category-desktop-pc.jpg    "https://picsum.photos/id/48/800/500"
  curl -L -o home/category-accessories.jpg   "https://picsum.photos/id/60/800/500"

  # --- PRODUCTS ---
  curl -L -o products/laptops.jpg            "https://picsum.photos/id/0/800/500"
  curl -L -o products/desktop-pcs.jpg        "https://picsum.photos/id/48/800/500"
  curl -L -o products/all-in-one.jpg         "https://picsum.photos/id/60/800/500"
  curl -L -o products/ssd-storage.jpg        "https://picsum.photos/id/119/800/500"
  curl -L -o products/ram-memory.jpg         "https://picsum.photos/id/2/800/500"
  curl -L -o products/accessories-cables.jpg "https://picsum.photos/id/180/800/500"

  # --- BLOG (cards 800x500) ---
  curl -L -o blog/choosing-a-laptop-card.jpg    "https://picsum.photos/id/3/800/500"
  curl -L -o blog/ssd-vs-hdd-card.jpg           "https://picsum.photos/id/20/800/500"
  curl -L -o blog/grading-explained-card.jpg    "https://picsum.photos/id/42/800/500"
  curl -L -o blog/greener-choice-card.jpg       "https://picsum.photos/id/96/800/500"

  # --- BLOG (article headers 1200x675) ---
  curl -L -o blog/choosing-a-laptop-hero.jpg    "https://picsum.photos/id/3/1200/675"
  curl -L -o blog/ssd-vs-hdd-hero.jpg           "https://picsum.photos/id/20/1200/675"
  curl -L -o blog/grading-explained-hero.jpg    "https://picsum.photos/id/42/1200/675"
  curl -L -o blog/greener-choice-hero.jpg       "https://picsum.photos/id/96/1200/675"

  # --- SOCIAL ---
  # og-image.jpg has NO download link. It is not a stock photo — it is a designed
  # card: brand gradient background, white logo, and one line of text. Make it in
  # Canva or Figma at exactly 1200x630 and save it as images/social/og-image.jpg.

Those are random stock photos, not refurbished IT. The client's own workshop and
stock photos will always do a better job here.

FULL LIST
---------
images/home/
  hero-background.jpg        1800x1100   behind the green hero
  hero-slide-1.jpg            900x900    hero circle, slide 1
  hero-slide-2.jpg            900x900    hero circle, slide 2
  hero-slide-3.jpg            900x900    hero circle, slide 3
  category-laptops.jpg        800x500    Laptops card
  category-desktop-pc.jpg     800x500    Desktop PC card
  category-accessories.jpg    800x500    Accessories card

images/products/
  laptops.jpg                 800x500
  desktop-pcs.jpg             800x500
  all-in-one.jpg              800x500
  ssd-storage.jpg             800x500
  ram-memory.jpg              800x500
  accessories-cables.jpg      800x500

images/blog/
  choosing-a-laptop-card.jpg     800x500    card in the blog list
  choosing-a-laptop-hero.jpg    1200x675    top of the article
  ssd-vs-hdd-card.jpg            800x500
  ssd-vs-hdd-hero.jpg           1200x675
  grading-explained-card.jpg     800x500
  grading-explained-hero.jpg    1200x675
  greener-choice-card.jpg        800x500
  greener-choice-hero.jpg       1200x675

images/social/
  og-image.jpg               1200x630    preview on WhatsApp, Facebook, LinkedIn

images/logo/
  logo-sprite.svg        THE MASTER FILE. Every page inlines this, which is how
                         the logo reaches the header, footer, preloader and the
                         large background watermarks. To change the logo across
                         the whole site: replace this file, then run
                             python3 build.py
  logo-full-white.svg    full lockup with tagline, white  — footer, preloader
  logo-full-dark.svg     same, dark — light backgrounds and print
  logo-full-colour.svg   original colour artwork from the designer
  logo-lockup-white.svg  lockup without tagline, white — sticky header
  logo-lockup-dark.svg   same, dark
  logo-mark-white.svg    icon only, white — the large watermarks
  logo-mark-green.svg    icon only, brand green
  logo-mark-colour.svg   original colour icon from the designer
  favicon.svg            browser tab icon

  favicon-32.png         32x32     older browsers
  apple-touch-icon.png   180x180   iPhone "Add to Home Screen"
  icon-192.png           192x192   Android home screen
  icon-512.png           512x512   Android splash / app install
  logo-mark-512.png      512x512   plain green mark on transparent

  These four were generated from the mark, so they already match the brand. If
  the logo changes, they need regenerating too.

TIPS
----
- Keep each photo under about 300KB. Large photos are the main cause of a slow
  site, and Google measures loading speed.
- WebP is smaller than JPG at the same quality. If you change format, update the
  file extension in the HTML too.
- Update the alt="" text when you swap in a real photo.

FONTS
-----
Outfit (headings) and Inter (body) load from Google Fonts. The link is in one
place: the head() function in build.py. To self-host them instead — faster, and
avoids a third-party request that counts under UK GDPR — download both in woff2
from google-webfonts-helper, put them in a fonts/ folder, remove the Google
<link> tags, and add @font-face rules at the top of css/style.css.
