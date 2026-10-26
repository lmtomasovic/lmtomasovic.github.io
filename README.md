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

### First time: put it on GitHub Pages

1. On GitHub, create a new public repository named `lmtomasovic.github.io`.
2. Upload every file in this folder to it (the "Add file → Upload files" button works; keep the `assets` folder).
3. In the repository, go to **Settings → Pages**. Under "Build and deployment," choose **Deploy from a branch**, pick `main` and `/ (root)`, and save.
4. After a minute or two the site is live at `https://lmtomasovic.github.io`.

### After that

Every time you upload changed files (or Claude Code pushes a commit), GitHub Pages republishes within a minute or two.

### Connect luketomasovic.com

1. Buy `luketomasovic.com` from any registrar (Cloudflare, Porkbun, Namecheap and Squarespace Domains all work).
2. In the repository's **Settings → Pages → Custom domain**, enter `luketomasovic.com` and save. GitHub adds a `CNAME` file for you.
3. At your registrar, add these DNS records:
   - Four `A` records for `@` pointing to `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`
   - One `CNAME` record for `www` pointing to `lmtomasovic.github.io`
4. Back in Settings → Pages, once the domain check passes, tick **Enforce HTTPS**. DNS can take up to a day to settle.

### Turn on visitor counts (GoatCounter)

1. Sign up at goatcounter.com and pick a code, for example `luketomasovic`.
2. In every `.html` file, find the GoatCounter comment near the top, replace `YOURCODE` with your code, and remove the `<!--` and `-->` lines around the script. (Or ask Claude Code to do it.)

## Preview locally

Double-clicking `index.html` opens it in your browser. The icons may not show this way because browsers block the icon file when opened from disk; they work once the site is published. To see everything locally, run `python3 -m http.server` in this folder and open `http://localhost:8000`.
