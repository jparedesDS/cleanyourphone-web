# CleanYourPhone — website

Static landing page for [CleanYourPhone](https://github.com/jparedesDS/cleanyourphone), the
open-source, reversible Android debloat skill for coding agents.

Live site: **<https://jparedesds.github.io/cleanyourphone-web/>**  
Spanish: **<https://jparedesds.github.io/cleanyourphone-web/es.html>**

No framework, no build step, no external fonts, no analytics, no third-party requests.

## What is here

- A skill-first bilingual English/Spanish landing page: the hero is a prompt card with **Open the
  skill** as the primary action and the app as the secondary path.
- **Choose your path**: the skill on the left as the main product, the local app on the right as an
  early MVP, and the CLI only as a small GitHub link.
- Inline SVG icons for GitHub, skill, app, download, CLI, docs, security, discussions, license and
  language.
- A three-step flow: connect locally, review, apply or restore.
- A profile grid with the existing 156 profiles and official full-color PNG logos for Google,
  Samsung, Xiaomi, Redmi, POCO and OnePlus.
- Four compact safety cards, six FAQ items, a final CTA and a footer with icons.
- A strict Content Security Policy, `security.txt`, canonical URLs, hreflang alternates,
  Open Graph metadata, JSON-LD and a sitemap.

## Preview locally

```bash
python -m http.server 8080
```

Open <http://localhost:8080/>.

## Files

| Path | What it is |
|---|---|
| `index.html` | English landing page. |
| `es.html` | Spanish landing page. |
| `styles.css` | Shared styles. |
| `app.js` | Copy buttons and toast feedback. |
| `assets/logo.svg`, `assets/favicon.svg` | Primary mark and favicon used by the site. |
| `assets/brands/` | Official full-color PNG logos and their source/trademark README (`assets/brands/README.md`). |
| `assets/banner.png` | Repository banner (1600×440). |
| `assets/og.png` | Social preview image (1280×640). |
| `assets/brand/` | `banner-web`, `banner-skill`, `social-web`, `social-skill` variants. |
| `robots.txt`, `sitemap.xml` | Crawler metadata. |
| `.well-known/security.txt` | Security contact and policy. |
| `404.html` | Not-found page. |
| `tests/test_site.py` | Link, ID, language, CSP, metadata and asset checks. |

## Release sync

`softwareVersion` in `index.html` and `es.html` must match `VERSION` in `tools/phone.py` in the skill
repository. When the JSON-LD block changes, recompute the CSP `sha256` hash in both pages and run the
test suite again.

## Brand assets

The final logo, banner and social preview are checked in under `assets/`. The identity, palette,
logo usage and clear-space rules live in
[docs/BRAND.md](https://github.com/jparedesDS/cleanyourphone/blob/main/docs/BRAND.md).

The website uses the two-color CleanYourMail-style system: lavender `#A78BFA` for actions and
emphasis, white `#F3F1EC` for text, and graphite `#121316` for the surface. The CleanYourMail
wordmark keeps its own orange `#FFB38A`.

Profile brand logos live in `assets/brands/`; their source URLs and trademark notice are in
`assets/brands/README.md`. The app repository is currently empty, so the site labels it as an early
MVP instead of claiming a downloadable binary.

The earlier phone-mockup banner generator has been retired; do not reintroduce it over the final
lockup assets.

## Deploy

This repository is a static site at the root. In GitHub:

1. **Settings → Pages**.
2. **Build and deployment → Source**: **Deploy from a branch**.
3. Branch: **`main`**, folder: **`/ (root)`**.
4. Save.

If the first build does not start, push any commit to `main`. The `pages build and deployment`
workflow should appear in **Actions**.

No workflow is required. If you prefer GitHub Actions, add a Pages workflow that uploads the root
directory as the artifact.

## Tests

```bash
python -m unittest discover -s tests -v
```

The suite checks local links and assets, duplicate IDs, the language switch, analytics absence,
inline-style absence (CSP compatibility), the CSP hash against the JSON-LD block, third-party
requests, canonical/hreflang metadata, PNG dimensions, the sitemap and `security.txt`. It also checks
the skill-first order, the prompt card and copy control, the absence of a CLI section, the inline
icon system, the six transparent brand PNGs and that the page does not reference an unrelated project.

## Links

- Skill repository: <https://github.com/jparedesDS/cleanyourphone>
- App repository (early MVP, currently empty): <https://github.com/jparedesDS/cleanyourphone-app>
- Safety rules: <https://github.com/jparedesDS/cleanyourphone/blob/main/docs/SAFETY.md>
- Profile catalog: <https://github.com/jparedesDS/cleanyourphone/blob/main/profiles/README.md>
- Prompt: <https://github.com/jparedesDS/cleanyourphone/blob/main/PROMPT.md>
- Spanish prompt: <https://github.com/jparedesDS/cleanyourphone/blob/main/PROMPT.es.md>

## License

MIT. See [LICENSE](LICENSE).
