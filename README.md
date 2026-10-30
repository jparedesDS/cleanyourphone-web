# CleanYourPhone — website

Static landing page for [CleanYourPhone](https://github.com/jparedesDS/cleanyourphone), the
open-source, reversible Android debloat skill for coding agents.

Published site (after enabling Pages): **<https://jparedesds.github.io/cleanyourphone-web/>**  
Spanish: **<https://jparedesds.github.io/cleanyourphone-web/es.html>**

No framework, no build step, no external fonts, no analytics, no third-party requests.

## What is here

- A bilingual English/Spanish landing page with a before/after home-screen demo using real app
  marks (Google, Facebook, TikTok, Netflix, Spotify, Booking.com, AliExpress).
- Brand tabs for Google, Samsung, Xiaomi, Redmi, POCO and OnePlus with profile counts and evidence.
- A three-command setup section and a copyable terminal walkthrough.
- A plain-language safety section: disable never uninstall, protected packages, role checks,
  backup first, small batches, no telemetry.
- The profile story: 157 model/firmware profiles, 6 brands, device vs documented.
- A comparison against random ADB scripts and root debloaters.
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
| `app.js` | Before/after app grid and copy buttons. |
| `assets/logo.svg`, `assets/favicon.svg` | Brand mark. |
| `assets/banner.png` | Website banner (1600×440). |
| `assets/og.png` | Social preview image (1280×640). |
| `assets/brand/` | `banner-web`, `banner-skill`, `social-web`, `social-skill` variants. |
| `assets/apps/` | Local app marks for the demo; see `assets/apps/README.md`. |
| `robots.txt`, `sitemap.xml` | Crawler metadata. |
| `.well-known/security.txt` | Security contact and policy. |
| `404.html` | Not-found page. |
| `tests/test_site.py` | Link, ID, language, CSP, metadata and asset checks. |
| `tools/make_assets.py` | Regenerates `banner.png` and `og.png` (dev-only; needs Pillow). |

## Brand assets

The banner and social preview are generated from code, so the layout is reproducible:

```bash
python -m pip install pillow
python tools/make_assets.py
```

- `assets/banner.png` / `assets/og.png` — website and default social preview (phone mockup).
- `assets/brand/banner-web.png` / `assets/brand/social-web.png` — copies of the web direction.
- `assets/brand/banner-skill.png` / `assets/brand/social-skill.png` — terminal-first variant for the
  skill repository and its social preview.

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
requests, canonical/hreflang metadata, PNG dimensions, the sitemap and `security.txt`.

## Links

- Skill repository: <https://github.com/jparedesDS/cleanyourphone>
- Safety rules: <https://github.com/jparedesDS/cleanyourphone/blob/main/docs/SAFETY.md>
- Profile catalog: <https://github.com/jparedesDS/cleanyourphone/blob/main/profiles/README.md>
- Prompt: <https://github.com/jparedesDS/cleanyourphone/blob/main/PROMPT.md>
- Spanish prompt: <https://github.com/jparedesDS/cleanyourphone/blob/main/PROMPT.es.md>

## License

MIT. See [LICENSE](LICENSE).
