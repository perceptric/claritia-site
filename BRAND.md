# Claritia brand: the website

**Version 3.0, 3 November 2026.** Replaces the black-and-white bracket look of version 2. The full guide, with every
token, component and rule, is the Claritia design system: https://claude.ai/artifact/2ZKbX3ATfS3Fr7LnEVTUkA. This
file is the short version for the site. The tokens live at the top of `assets/site.css`.

## The look

Calm. A warm off-white page between two thin rails, white surfaces lifted by soft ring shadows, Inter for every word
and Claritia green as the one accent. Show the product itself, drawn in HTML, more than pictures of it.

## Mark

The Slot: a green tile (`#0C8C5E`) holding six time slots, with one booked in solid white. A form that ends in a
meeting, said in one shape. The name is Inter 600 at -0.03em.

| File (`assets/brand/`) | Use |
|---|---|
| `claritia-mark.svg` | The mark, 20 px and up |
| `claritia-mark-small.svg` | 16 to 19 px and the browser tab: four bigger slots |
| `claritia-mark-ink.svg` | One-color printing and stamps |
| `claritia-mark-white.svg` | On green or on photos |
| `claritia-lockup.svg`, `claritia-lockup-on-dark.svg` | Mark and name as outlines, where text can't be live |
| `claritia-app-icon.png`, `claritia-avatar.png` | App stores and social profiles (square, they round it) |
| `favicon.ico`, `apple-touch-icon.png`, `og-image.png` | Browser, phone home screen, link previews |

- In the lockup the gap is a third of the mark's height. Keep a quarter of its height clear on every side.
- When there's no room for the name (a folded sidebar, a tab, an avatar), show the mark alone.
- Never recolor the tile, move the booked slot, outline, rotate or shadow the mark, or set the name in another font.

## Color

| Token | Value | Use |
|---|---|---|
| `--bg` | #fafaf5 | The page |
| `--surface` | #ffffff | Cards, the header, inputs |
| `--rail`, `--line` | #ebebe4, #ebebeb | The rails and bands; rows inside cards |
| `--ink`, `--text` | #0f0f0f, #171717 | Headings; body text in the UI |
| `--body`, `--meta` | #6c6c6d, #737373 | Paragraphs; labels and counts |
| `--btn` | #333333 | The dark primary button |
| `--green` | #0c8c5e | The mark, tiles, the running light, chart lines, focus |
| `--green-strong` | #0a7a52 | Green fills that carry white text (#0c8c5e is 4.3:1 on white) |
| `--green-100`, `--green-200` | #e3f4ec, #c9eadb | Selected chips, the picked switch |
| `--dark` | #242421 | Dark bands and the footer |

Green stays near 5% of a view. Status tags pair a soft fill with a deep text: green, orange, blue, purple, gray.

## Type

Inter only. Display 64/64 at weight 500 with -0.042em tracking (40px on phones). Section titles 44/44 at 500 with
-0.035em. Card titles 18px at 500. Lead text 18/24 in `--body`. Headings are one tone. Mono is only for code.

## Shape and depth

- Raised things carry a 1px ring plus soft layers (`--sh-rest`, `--sh-hover`) and no border.
- Buttons, chips and the header are pills. Status tags 6px, kind tags 4px, inputs 8px, cards 10 to 12px, the prompt
  frame 16px, product windows 20px, the tile field 24px.
- The primary button is dark (`--btn`) with its own ring shadow. Green buttons are for the last step of a flow.

## Layout

The frame is `min(1360px, 100% - 80px)` between 1px rails. Sections pad 132px on top and 40px at the sides. Between
sections sits a 79px band with full-width hairlines. Section heads are a small chip, a title and one line.

## Pictures and motion

- **Tile field:** green tiles blink at the hero's edges; a full field of soft greens sits behind the product.
- **Running light:** a green comet circles the prompt's edge every 5 seconds.
- **Rise in:** things arrive with opacity, a 2px blur and 6px of travel over 200 to 560ms on `cubic-bezier(.22,1,.36,1)`.
  Hover and color changes take 150ms. Everything stops under reduced motion.

## Words

Short, plain and calm, at a 9th-grade level. Sentence case. Buttons say what happens. No hype, no emoji, and no
made-up customers, quotes or numbers.
