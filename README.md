# Juno Jewellery Co. — junojewelleryco.com

Static site served by GitHub Pages from this repository (branch `main`, root).

## How it's built
- `index.html` holds the whole site: markup, styles, script, catalogue and Juno Notes data.
- Every page has its own address: `/catalogue/<style>/`, `/notes/<note>/`, `/source/`, `/privacy/`, `/terms/`. Each folder holds a copy of `index.html` with that page's title, description, canonical link, social preview and structured data.
- After editing `index.html`, run `python3 _tools/build.py` from the site root. It regenerates every page folder and `sitemap.xml` (needs Python 3 and Node).
- `MOCK_CATALOGUE = true` in `index.html` keeps the sample product pages out of Google. Set it to `false` once real stock is listed, then rebuild.

## Live services
- Metal prices: Gold API, from the visitor's browser, every minute (falls back to the reference close in the script).
- Charts: TradingView mini-chart widget.
- Enquiries, quote requests and sourcing briefs: emailed to junojewelleryco@gmail.com via FormSubmit, with an automatic reply to the buyer. A Gmail filter keeps them out of Spam.
- Quote list: stored in the visitor's browser (`juno.quote-list.v1`).

## Domains
- junojewelleryco.com: GitHub Pages (A records 185.199.108–111.153, `www` CNAME to ash-dotcom737.github.io), DNS at VentraIP.
- junojewelleryco.com.au and junojewelleryco.online: 301 forwarding at VentraIP to https://junojewelleryco.com.
- Older addresses (`/#arc-hoops`, `/source?sample=`, `/?piece=`) are redirected to the matching page.
