# Source for qcdesignsme.github.io/think-of-us

Working files used to build this application page. The live site is the `index.html`, `img/` and `prototype/` at the repo root; nothing in `source/` is needed to view it.

To make a version for another role: copy this repo's contents into a new repo, then edit `source/page/build.py` (content) and `source/page/template.html` (layout) and rebuild.

## Page: `source/page/`

| File | What it is |
| --- | --- |
| `template.html` | The whole page: CSS tokens, hero, sections, matcher and animation scripts. Placeholders: `{{STAGE}}`, `{{LOGOS}}`, `{{NEEDS}}`, `{{VA_DECK}}`, `{{VA_DECK_ATTR}}`. |
| `build.py` | Holds the six requirement-matcher panels (`needs` list: names, pills, posting quotes, evidence rows, buttons, images, embeds) and fills the template. |
| `stage.html` | Markup for the hero animation stage: four logos with names, the ground line, and the character (side view and front-facing waving view). |

Build (Python 3, no dependencies), from the repo root:

```
python3 source/page/build.py
```

This writes `index.html` at the repo root (images load from `img/`) and `source/page/qian-chen-think-of-us.html`, a single self-contained file with images inlined (git-ignored, for emailing or uploading).

Content that is not in `build.py` (hero card, work cards, role map, quotes, letter, footer) is plain text in `template.html`.

## Hero animation: `source/animation/`

- `logos.json`: the four round logos (Mentor Collective, USDA, VA, Think of Us in #21a69b) as base64 PNG data URIs. `{{LOGOS}}` in the page comes from here.
- `logos/`: the same four logos as 256px transparent PNGs.
- `loader-loop.src.html` and `loader-wave.src.html`: the standalone looping animations (the wave version stops, turns, waves, runs off). They contain `{{mc}}`-style placeholders filled from `logos.json`.
- `crop.py`, `cap.py`, `capw.py`, `mkgif.py`, `mkgifw.py`: one-off scripts used to cut the logo circles and export transparent GIF/PNG versions (Playwright + Pillow). They have absolute paths from the original workspace; adjust before reuse.

The version on the page plays once, ends on the wave, and has round Play/Replay and Pause buttons (32px, labelled for screen readers); see the "hero animation" script at the end of `template.html`. To swap the last logo for another company, replace `us` in `logos.json` and its label in `stage.html`.

## Reading the Figma file: `source/figma-tools/`

Node scripts that read a `.fig` file without Figma (unzip it first; it contains `canvas.fig` and `images/`). Install with `npm install` (kiwi-schema, pako, fzstd).

- `parse.js <dir>`: decodes `<dir>/canvas.fig` to `<dir>.json`.
- `tree.js <dir> <depth>`: prints the node tree with ids.
- `render.js <dir> <nodeId>...`: rough HTML render plus a text dump of a frame.
- `map.js`: lists which node uses which image.

The page's design source is the Figma file "Qian Chen for Think of Us".
