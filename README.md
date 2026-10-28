# luketomasovic.com

My personal website. Plain HTML and CSS, no build step, hosted free on GitHub Pages.

## What's in here

| File | What it is |
| --- | --- |
| `index.html` | Home: photo, short bio, link icons, "Now" section |
| `about.html` | The longer story |
| `research.html` | Research areas |
| `writing.html` | List of Substack posts |
| `other.html` | Ventures, bookshelf (links to Goodreads), side projects |
| `404.html` | Shown when someone visits a page that doesn't exist |
| `assets/style.css` | All colors, fonts and layout |
| `assets/icons.svg` | The LinkedIn, X, Scholar, GitHub, Substack and email icons |
| `assets/favicon.svg` | The "LT" browser-tab icon |
| `assets/photo.jpg` | My headshot |
| `assets/og-card.png` | The preview image shown when the site is shared on LinkedIn, X or Slack |
| `scripts/make-og-card.py` | Rebuilds that preview image. Only needed if the name, tagline or photo changes |
| `assets/il2-receptor-*`, `assets/endotag-fusion-*`, `assets/bispecific-igg-*` | The spinning structures on the Research page, each rendered once per theme |
| `scripts/make-structure-spin.py` | Rebuilds those animations, and makes new ones for other projects |
| `scripts/structures/` | Local structure files the script renders from, with their terms of use |
| `CNAME` | Points GitHub Pages at luketomasovic.com. Do not delete. |
| `CLAUDE.md` | Notes that Claude Code reads before editing the site |

## How to update the site

The easiest way: open this folder in Claude Code and describe the change, for example "add my new Substack post to the Writing page" or "update the Now section." Claude Code reads `CLAUDE.md` first, so it knows the style rules.

If you'd rather edit by hand, every page is a normal HTML file. Open it in any text editor, change the words, save, and publish (see below).

### Common edits

- **Change my photo.** Save a new square photo as `assets/photo.jpg`, replacing the old one. About 400×400 pixels is plenty. The photo also appears on the share card, so rebuild that afterwards (see below).
- **Update "Now".** In `index.html`, edit the lines under `Now` and change "Updated October 2026."
- **Add a Substack post.** In `writing.html`, there's a commented-out example list. Copy one `<li>…</li>` block per post, newest first, and delete the "Nothing here yet" box.
- **Add a venture or project.** In `other.html`, copy an existing `<li>…</li>` line and change the words.
- **Change the accent color.** In `assets/style.css`, change `--accent` (light mode) and the two `--accent` lines under the dark mode sections.
- **Change a link.** The icon links appear on every page (home and footer). Ask Claude Code to "change my LinkedIn link everywhere," or search all files for the old address.

### Rebuild the share card

`assets/og-card.png` is the image LinkedIn, X and Slack show when someone posts
a link to the site. It does not update itself. If you change your photo, your
name or the tagline, rebuild it:

```bash
pip install Pillow
python3 scripts/make-og-card.py
```

The first run downloads the two fonts; later runs are offline. If you changed
the name or tagline, edit the three lines near the top of that script to match
before running it.

Already-shared links keep the old image until the site that cached it refetches.
LinkedIn's [Post Inspector](https://www.linkedin.com/post-inspector/) forces a refresh.

### Add a structure animation to a Research section

Each animated structure is a short video of the molecule turning, rendered
twice: once on the light page background and once on the dark one, so it looks
like part of the page in either theme.

To add one for another project, open `scripts/make-structure-spin.py` and copy a
block in `STRUCTURES`. A structure comes either from the PDB (`"pdb": "2ERJ"`,
downloaded and cached) or from a local file in `scripts/structures/`. Parts are
any PyMOL selection, so you can split a complex by chain or a single chain by
residue range. Then:

```bash
brew install pymol ffmpeg
python3 scripts/make-structure-spin.py
```

It prints the pixel dimensions to put in the `<video>` tags. Copy the `<figure
class="structure">` block in `research.html` and point it at the new filenames.
Rendering takes a few minutes per structure.

Colours are baked into the video, so the swatches in the figure caption are set
separately in `assets/style.css` (the `.key-*` rules). If you change a chain
colour, change it in both places.

**If the structure is a prediction rather than an experimental structure**, say
so in the caption. The EndoTag figure is an AlphaFold Server model, and those
Terms of Use require conspicuous notice wherever the output or anything derived
from it is published, so its caption links to
[alphafoldserver.com/output-terms](https://alphafoldserver.com/output-terms) and
the terms file sits next to the structure in `scripts/structures/`. Keep both if
you keep the figure. AlphaFold Server output is also non-commercial use only.

## Publishing

The site is live at **https://luketomasovic.com**. It is already set up, so
there is nothing to configure. This section is just a record of how it works.

### How it is wired up

- Repository: `lmtomasovic/lmtomasovic.github.io` (public)
- GitHub Pages serves the `main` branch from the root, with Enforce HTTPS on
- The `CNAME` file in this folder is what points Pages at the custom domain. Do not delete it.
- DNS is at Cloudflare: four `A` records on `@` pointing at GitHub
  (`185.199.108.153`, `.109`, `.110`, `.111`), and a `CNAME` on `www` to
  `lmtomasovic.github.io`. Every record is **DNS only** (gray cloud), not
  proxied, because Cloudflare's proxy blocks GitHub's HTTPS certificate renewal.
- Email: Cloudflare Email Routing forwards `contact@luketomasovic.com` to Gmail.

### Publishing a change

From this folder:

```bash
git add -A && git commit -m "what changed" && git push
```

GitHub Pages republishes within a minute or two.

### Turn on visitor counts (GoatCounter)

Not set up yet. To do it:

1. Sign up at goatcounter.com and pick a code, for example `luketomasovic`.
2. In every `.html` file, find the GoatCounter comment near the top, replace `YOURCODE` with your code, and remove the `<!--` and `-->` lines around the script. (Or ask Claude Code to do it.)

Cloudflare Web Analytics is a free alternative that works without the proxy.

## Preview locally

Double-clicking `index.html` opens it in your browser. The icons may not show this way because browsers block the icon file when opened from disk; they work once the site is published. To see everything locally, run `python3 -m http.server` in this folder and open `http://localhost:8000`.
