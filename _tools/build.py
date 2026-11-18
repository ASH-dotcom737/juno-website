#!/usr/bin/env python3
"""Generate one HTML file per page address from index.html.

Each page is the same app (index.html) with its own <title>, description, canonical
link, social preview tags and structured data, so Google and link previews see the
right page. Run from the site root:  python3 _tools/build.py
"""
import html, json, os, re, subprocess

SITE = "https://junojewelleryco.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

# Pull the catalogue/notes data straight from the page script so there is one source of truth.
block = src[src.index("var products = ["):src.index("var sourceMetals")]
data = json.loads(subprocess.check_output(["node", "-e", block + "process.stdout.write(JSON.stringify({products, notes}))"]))
mock = re.search(r"var MOCK_CATALOGUE = (true|false)", src).group(1) == "true"
legal = {
    "privacy": ("Privacy policy", "How Juno Jewellery Co. collects, uses and looks after the details you share through junojewelleryco.com."),
    "terms": ("Website terms", "Terms for using junojewelleryco.com, including the sample catalogue, indicative metal prices and how quotes become orders."),
}
ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "Juno Jewellery Co.", "url": SITE + "/",
       "logo": SITE + "/images/juno-icon.png", "email": "junojewelleryco@gmail.com", "areaServed": "AU"}

def head(title, desc, path, image, ld, noindex=False, og_type="website"):
    e = lambda x: html.escape(x, quote=True)
    out = [f"<title>{e(title)}</title>",
           f'<meta name="description" content="{e(desc)}">',
           f'<link rel="canonical" href="{SITE}{path}">']
    if noindex:
        out.append('<meta name="robots" content="noindex">')
    out += [f'<meta property="og:type" content="{og_type}">',
            '<meta property="og:site_name" content="Juno Jewellery Co.">',
            f'<meta property="og:title" content="{e(title)}">',
            f'<meta property="og:description" content="{e(desc)}">',
            f'<meta property="og:url" content="{SITE}{path}">',
            f'<meta property="og:image" content="{SITE}{image}">',
            '<meta name="twitter:card" content="summary_large_image">',
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>"]
    return "<!--HEAD:START-->\n" + "\n".join(out) + "\n<!--HEAD:END-->"

def write(path, block_html):
    page = re.sub(r"<!--HEAD:START-->.*?<!--HEAD:END-->", lambda m: block_html, src, flags=re.S)
    target = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    open(target, "w", encoding="utf-8").write(page)
    return path

pages = []
home_ld = {"@context": "https://schema.org", "@graph": [ORG, {"@type": "WebSite", "url": SITE + "/", "name": "Juno Jewellery Co.", "publisher": {"@id": SITE + "/#org"}}]}
pages.append((write("/", head("Juno Jewellery Co. | Wholesale Gold & Silver",
    "Gold and silver jewellery sourcing for Australian jewellers and independent retailers. Explore the sample catalogue or send Juno a sourcing brief.",
    "/", "/images/juno-graphite-hoops-1152.webp", home_ld)), True))

for p in data["products"]:
    path = f"/catalogue/{p['slug']}/"
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "sku": p["sku"],
          "description": p["description"], "image": SITE + p["full"], "material": p["material"],
          "category": p["category"], "brand": {"@type": "Brand", "name": "Juno Jewellery Co."}}
    pages.append((write(path, head(f"{p['name']} | Juno Jewellery Co.", p["description"], path, p["image"], ld,
                                   noindex=mock, og_type="product")), not mock))

for n in data["notes"]:
    path = f"/notes/{n['slug']}/"
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": n["title"], "description": n["introduction"],
          "image": SITE + n["image"], "author": ORG, "publisher": ORG, "mainEntityOfPage": SITE + path}
    pages.append((write(path, head(f"{n['title']} | Juno Notes", n["introduction"], path, n["thumb"], ld, og_type="article")), True))

src_ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Source a piece", "url": SITE + "/source/", "publisher": ORG}
pages.append((write("/source/", head("Source a piece | Juno Jewellery Co.",
    "Send Juno a sourcing brief: describe the piece, metal and quantity, add a reference photo, and Ashkan will reply by email.",
    "/source/", "/images/paperclip-chain.webp", src_ld)), True))

for slug, (title, desc) in legal.items():
    path = f"/{slug}/"
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": SITE + path, "publisher": ORG}
    pages.append((write(path, head(f"{title} | Juno Jewellery Co.", desc, path, "/images/juno-graphite-hoops-1152.webp", ld)), True))

urls = "".join(f"<url><loc>{SITE}{p}</loc></url>" for p, indexed in pages if indexed)
open(os.path.join(ROOT, "sitemap.xml"), "w").write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
print("\n".join(f"{p}{'' if i else '  (noindex)'}" for p, i in pages))
