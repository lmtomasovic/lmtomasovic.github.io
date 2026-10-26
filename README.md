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
| `CNAME` | Points GitHub Pages at luketomasovic.com. Do not delete. |
| `CLAUDE.md` | Notes that Claude Code reads before editing the site |

## How to update the site

The easiest way: open this folder in Claude Code and describe the change, for example "add my new Substack post to the Writing page" or "update the Now section." Claude Code reads `CLAUDE.md` first, so it knows the style rules.

If you'd rather edit by hand, every page is a normal HTML file. Open it in any text editor, change the words, save, and publish (see below).

### Common edits

- **Change my photo.** Save a new square photo as `assets/photo.jpg`, replacing the old one. No code change needed. About 400×400 pixels is plenty.
- **Update "Now".** In `index.html`, edit the three lines under `Now` and change "Updated October 2026."
- **Add a Substack post.** In `writing.html`, there's a commented-out example list. Copy one `<li>…</li>` block per post, newest first, and delete the "Nothing here yet" box.
- **Add a venture or project.** In `other.html`, copy an existing `<li>…</li>` line and change the words.
- **Change the accent color.** In `assets/style.css`, change `--accent` (light mode) and the two `--accent` lines under the dark mode sections.
- **Change a link.** The icon links appear on every page (home and footer). Ask Claude Code to "change my LinkedIn link everywhere," or search all files for the old address.

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
