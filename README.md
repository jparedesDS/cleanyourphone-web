# CleanYourPhone — website

Static landing page for [CleanYourPhone](https://github.com/jparedesDS/cleanyourphone), the
open-source, reversible Android debloat skill for coding agents.

Live site: **<https://jparedesds.github.io/cleanyourphone-web/>**  
Spanish: **<https://jparedesds.github.io/cleanyourphone-web/es.html>**

No framework, no build step, no external fonts, no analytics, no third-party requests.

## What is here

- A compact bilingual English/Spanish landing page with a copyable terminal quick start.
- A three-step flow: connect, review and disable, with the backup and undo command in view.
- A CLI command grid: `doctor`, `wizard`, `plan`, `apply`, `restore`, `verify` and the supporting
  commands.
- A plain-language safety section: disable never uninstall, protected packages, role checks,
  backup first, small batches, no telemetry, and `restore --from-backup` for recovery.
- A brand/profile grid for Google, Samsung, Xiaomi, Redmi, POCO and OnePlus: 156 model/firmware
  profiles, device-tested vs documented.
- A short FAQ, a final CTA and a footer with the repository, docs, prompt and changelog.
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
| `assets/logo.svg`, `assets/favicon.svg` | Brand mark. |
| `assets/banner.png` | Repository banner (1600×440). |
| `assets/og.png` | Social preview image (1280×640). |
| `assets/brand/` | `banner-web`, `banner-skill`, `social-web`, `social-skill` variants. |
| `robots.txt`, `sitemap.xml` | Crawler metadata. |
| `.well-known/security.txt` | Security contact and policy. |
| `404.html` | Not-found page. |
| `tests/test_site.py` | Link, ID, language, CSP, metadata and asset checks. |
| `tools/make_assets.py` | Regenerates `banner.png` and `og.png` (dev-only; needs Pillow). |

## Release sync

`softwareVersion` in `index.html` and `es.html` must match `VERSION` in `tools/phone.py` in the skill
repository. When the JSON-LD block changes, recompute the CSP `sha256` hash in both pages and run the
test suite again.

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
requests, canonical/hreflang metadata, PNG dimensions, the sitemap and `security.txt`. It also checks
that the page does not reference an unrelated project.

## Links

- Skill repository: <https://github.com/jparedesDS/cleanyourphone>
- Safety rules: <https://github.com/jparedesDS/cleanyourphone/blob/main/docs/SAFETY.md>
- Profile catalog: <https://github.com/jparedesDS/cleanyourphone/blob/main/profiles/README.md>
- Prompt: <https://github.com/jparedesDS/cleanyourphone/blob/main/PROMPT.md>
- Spanish prompt: <https://github.com/jparedesDS/cleanyourphone/blob/main/PROMPT.es.md>

## License

MIT. See [LICENSE](LICENSE).
