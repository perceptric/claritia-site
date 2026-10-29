# Working in this repo

- After making changes, always commit and push to `main`. Hostinger auto-deploys from `main`.
  (Standing instruction from the owner.)
- The site is static HTML, CSS and a little plain JavaScript. No build step, no library. Every section
  must stay readable and usable when JavaScript or motion is off.
- The look follows `BRAND.md`, in the same family as tryomniscient.com.
- The hero picture and the product tour are generated: edit `tools/hero.py` or `tools/tour.py`, then run
  `python3 tools/hero.py && python3 tools/tour.py`. The product drawings come from `tools/feats.py`.
