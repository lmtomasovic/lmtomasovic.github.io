# Notes for Claude Code

This is Luke Tomasovic's personal website. Read this before making changes.

## Setup

- Plain HTML and CSS only. No frameworks, no build step, no npm. Luke isn't comfortable with code, so keep every change simple enough to edit by hand.
- Hosted on GitHub Pages from the repository root. Custom domain: luketomasovic.com.
- Every page repeats the same `<head>`, header and footer. When one changes, change all of them (`index.html`, `about.html`, `research.html`, `writing.html`, `other.html`, `404.html`).
- All styling lives in `assets/style.css`. Use the existing CSS variables; don't add inline colors.
- Icons come from the sprite in `assets/icons.svg` via `<use href="assets/icons.svg#name">`.

## Look and feel

- Minimalist, casual, inviting. It should not feel academic, stuffy, or like a resume.
- One centered column (max 640px), nav across the top.
- Figtree for body text, JetBrains Mono for small accents (nav, labels, dates).
- Accent color `#4292c6` in light mode, `#6baed6` in dark mode. Light and dark follow the visitor's system setting.
- Link icons are icon-only (with `aria-label` and `title`). They appear under the bio on Home and small in every footer. Outside links open in a new tab; email does not.

## Content rules

- Write casually and plainly, like Luke talking. Short sentences, no buzzwords, no em-dashes.
- Keep it accessible to general readers as well as scientists.
- Do not include: GPA, total publication count, personal hobbies, a CV link, or anything about job searching.
- Do not describe unpublished work, including the "stapler" antibody and logic-gated IL-2 projects, until Luke says it's published.
- Research page is all about immunoengineering and protein design. Three short sections: (1) Conditionally active IL-2/antibody fusion proteins, (2) Computationally designed protein-based therapeutics, (3) Engineering bispecific antibodies. Each has a brief high-level description and a "Papers:" line (and for section 1, a "Presentations:" line). No transplant section, no keywords lines.
- The PEGS 2026 poster is hosted locally at `assets/pegs-2026-poster.pdf` and linked from the Presentations line in `research.html`. Luke decided not to list BMES 2025.
- Writing page lists Substack posts in this format: date, category, title (linked), one-line subtitle. Newest first.
- No talks or awards section on the Research page. Luke decided against it.
- Other page has three sections: Ventures, Bookshelf (a link to Luke's Goodreads, https://www.goodreads.com/review/list/69780414) and Side projects. Luke decided against a teaching section.

## Links

- LinkedIn: https://www.linkedin.com/in/luketomasovic
- X: https://x.com/luketomasovic11
- Google Scholar: https://scholar.google.com/citations?user=PSj0g8gAAAAJ&hl=en
- ORCID: https://orcid.org/0000-0002-1459-3252
- GitHub: https://github.com/lmtomasovic
- Substack: https://luketomasovic.substack.com/
- Email: lmtomasovic@gmail.com

## Still to do

- Turn on GoatCounter once Luke has an account (see README).
- Connect the domain once purchased (see README).
