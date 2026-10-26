# Working in this repo

- After making changes, always commit and push to `main`. Hostinger auto-deploys from `main`.
  (Standing instruction from the owner.)
- The site is static HTML/CSS with a small, vendored progressive-enhancement motion layer
  (GSAP + Lenis in `assets/vendor`, driven by `assets/motion.js`). No build step. Every section
  must stay readable and usable when JavaScript or motion is off.
