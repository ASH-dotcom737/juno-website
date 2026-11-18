# Juno Jewellery Co. — junojewelleryco.com

Static site served by GitHub Pages. Everything lives in `index.html` (markup, styles, script) plus `images/`.

- Live prices: Gold API (browser request, refreshes every minute; falls back to the reference close in the script).
- Charts: TradingView mini-chart widget.
- Enquiries, quote requests and sourcing briefs: emailed to junojewelleryco@gmail.com via FormSubmit (first submission sends a one-time activation email).
- Quote list: stored in the visitor's browser (`juno.quote-list.v1`, same format as v18).
- Old v18 addresses (`/catalogue/*`, `/notes/*`, `/source?sample=`, `/?piece=`) redirect to the matching section.
