from __future__ import annotations

import base64
import hashlib
import json
import re
import struct
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "es.html", "404.html")
PAGES_WITH_JSONLD = ("index.html", "es.html")
BASE_URL = "https://jparedesds.github.io/cleanyourphone-web/"


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path.name} is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


class SiteTest(unittest.TestCase):
    def test_pages_exist(self):
        for name in PAGES:
            self.assertTrue((ROOT / name).is_file(), name)

    def test_titles_and_viewport(self):
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn("<title>", text)
                self.assertIn('name="viewport"', text)

    def test_unique_ids(self):
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            ids = re.findall(r'id="([^"]+)"', text)
            duplicates = [item for item, count in Counter(ids).items() if count > 1]
            with self.subTest(page=name):
                self.assertEqual(duplicates, [])

    def test_local_links_and_assets_resolve(self):
        for name in PAGES:
            page = ROOT / name
            text = page.read_text(encoding="utf-8")
            for attr in ("href", "src"):
                for target in re.findall(rf'{attr}="([^"]+)"', text):
                    if target.startswith(("#", "http://", "https://", "mailto:", "tel:")):
                        continue
                    target = target.split("#", 1)[0]
                    if not target:
                        continue
                    with self.subTest(page=name, target=target):
                        self.assertTrue((page.parent / target).resolve().exists())

    def test_language_switch(self):
        english = (ROOT / "index.html").read_text(encoding="utf-8")
        spanish = (ROOT / "es.html").read_text(encoding="utf-8")
        self.assertIn('href="es.html"', english)
        self.assertIn('href="index.html"', spanish)

    def test_no_analytics_or_tracking(self):
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8").lower()
            with self.subTest(page=name):
                for marker in ("google-analytics", "googletagmanager", "plausible.io",
                               "matomo", "hotjar", "segment.com"):
                    self.assertNotIn(marker, text)

    def test_start_nav_link_points_to_start_section(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("color: var(--accent-2) !important;", css)
        for name, label, next_label in (
            ("index.html", "Start", "How it works"),
            ("es.html", "Empieza", "Cómo funciona"),
        ):
            text = (ROOT / name).read_text(encoding="utf-8")
            nav = text.split('<nav class="nav"', 1)[1].split("</nav>", 1)[0]
            with self.subTest(page=name):
                self.assertIn(f'class="nav-start" href="#start">{label}</a>', nav)
                self.assertLess(nav.index("nav-start"), nav.index(next_label))
                self.assertIn('id="start"', text)

    def test_mail_cross_link_after_faq(self):
        for name in ("index.html", "es.html"):
            text = (ROOT / name).read_text(encoding="utf-8")
            nav = text.split('<nav class="nav"', 1)[1].split("</nav>", 1)[0]
            with self.subTest(page=name):
                self.assertLess(nav.index(">FAQ<"), nav.index("https://jparedesds.github.io/cleanyourmail-web"))
                self.assertIn('class="wordmark-mail"', nav)
                self.assertIn(">Mail</span>", nav)
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("--mail-accent: #ffb38a;", css)

    def test_skill_first_hero_and_no_cli_section(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        hero = text.split('<section class="hero">', 1)[1].split("</section>", 1)[0]
        self.assertIn("Download for Windows", hero)
        self.assertIn("cleanyourphone-app/releases/latest", hero)
        self.assertLess(hero.index("Open the skill"), hero.index("Download for Windows"))

        spanish = (ROOT / "es.html").read_text(encoding="utf-8")
        es_hero = spanish.split('<section class="hero">', 1)[1].split("</section>", 1)[0]
        self.assertIn("Descargar para Windows", es_hero)
        self.assertIn("cleanyourphone-app/releases/latest", es_hero)
        self.assertLess(es_hero.index("Abrir la skill"), es_hero.index("Descargar para Windows"))

        self.assertIn('class="app-window"', hero)
        self.assertIn('class="app-bar"', hero)
        self.assertEqual(hero.count("<span></span>"), 3)
        self.assertIn("CleanYourPhone · skill", hero)
        self.assertIn("data-copy=", hero)
        self.assertIn("Copy prompt", hero)
        self.assertIn("https://github.com/jparedesDS/cleanyourphone", hero)
        prompt_block = hero.split('class="prompt-block"', 1)[1].split("</pre>", 1)[0]
        self.assertIn("Read SKILL.md from", prompt_block)
        self.assertIn("https://github.com/jparedesDS/cleanyourphone", prompt_block.replace("<wbr>", ""))
        self.assertNotIn('id="cli"', text)

    def test_section_order_is_skill_first(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        hero = text.index('<section class="hero">')
        positions = [text.index(f'id="{section}"') for section in ("start", "how", "profiles", "safety", "faq")]
        self.assertLess(hero, positions[0])
        self.assertEqual(positions, sorted(positions))

    def test_choose_path_puts_skill_before_app(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        path = text.split('id="start"', 1)[1].split("</section>", 1)[0]
        self.assertIn("App · Early MVP", path)
        self.assertIn("Download the app", path)
        self.assertIn("cleanyourphone-app/releases/latest", path)
        self.assertLess(path.index("Use the skill"), path.index("App · Early MVP"))

        spanish = (ROOT / "es.html").read_text(encoding="utf-8")
        es_path = spanish.split('id="start"', 1)[1].split("</section>", 1)[0]
        self.assertIn("App · MVP temprano", es_path)
        self.assertIn("Descarga la app", es_path)
        self.assertIn("cleanyourphone-app/releases/latest", es_path)
        self.assertLess(es_path.index("Usa la skill"), es_path.index("App · MVP temprano"))

        self.assertIn("path-card-primary", path)
        self.assertIn("copy-inline", path)
        copy_control = path.split('class="copy-inline"', 1)[1].split("</button>", 1)[0]
        self.assertIn("https://github.com/jparedesDS/cleanyourphone", copy_control)

    def test_inline_icons_are_defined_and_used(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="icon-sprite"', text)
        for icon in (
            "i-github", "i-skill", "i-app", "i-cli",
            "i-docs", "i-shield", "i-chat", "i-license", "i-globe",
        ):
            with self.subTest(icon=icon):
                self.assertIn(f'id="{icon}"', text)
                self.assertIn(f'href="#{icon}"', text)
        inline_icons = re.findall(r'<svg class="icon"([^>]*)>', text)
        self.assertGreaterEqual(len(inline_icons), 15)
        for attrs in inline_icons:
            with self.subTest(attrs=attrs):
                self.assertIn('aria-hidden="true"', attrs)

    def test_footer_has_icons_for_every_link(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        footer = text.split("<footer", 1)[1]
        for icon in ("i-app", "i-cli", "i-github", "i-docs", "i-shield", "i-chat", "i-license", "i-globe"):
            with self.subTest(icon=icon):
                self.assertIn(f'href="#{icon}"', footer)

    def test_purple_white_graphite_palette(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        for token in (
            "--ink: #121316;",
            "--text: #f3f1ec;",
            "--muted: #a19e96;",
            "--accent: #a78bfa;",
            "--mail-accent: #ffb38a;",
        ):
            with self.subTest(token=token):
                self.assertIn(token, css)
        self.assertNotIn("#e2c15c", css.lower())
        self.assertNotIn("#efd07a", css.lower())
        for name in ("index.html", "es.html"):
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn('<meta name="theme-color" content="#121316">', text)
        for name in ("logo.svg", "favicon.svg"):
            svg = (ROOT / "assets" / name).read_text(encoding="utf-8")
            with self.subTest(asset=name):
                self.assertIn('stroke="#A78BFA"', svg)
                self.assertIn('stroke="#F3F1EC"', svg)
                self.assertNotIn("#E2C15C", svg.upper())

    def test_brand_logos_are_transparent_pngs(self):
        for brand in ("google", "samsung", "xiaomi", "redmi", "poco", "oneplus"):
            path = ROOT / "assets" / "brands" / f"{brand}.png"
            with self.subTest(brand=brand):
                data = path.read_bytes()
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                width, height, _depth, color_type = struct.unpack(">IIBB", data[16:26])
                self.assertGreater(width, 0)
                self.assertGreater(height, 0)
                self.assertIn(color_type, (4, 6), "logo must keep an alpha channel")

    def test_provider_strip_uses_phone_brands(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("animation: provider-marquee 90s linear infinite;", css)
        self.assertIn(".provider-strip:hover .provider-strip-track { animation-play-state: paused; }", css)
        self.assertIn("animation-duration: 90s !important;", css)
        for name in ("index.html", "es.html"):
            text = (ROOT / name).read_text(encoding="utf-8")
            hero_start = text.index('<section class="hero">')
            hero_end = text.index("</section>", hero_start)
            strip_start = text.index('<div class="provider-strip"', hero_end)
            start = text.index('id="start"', strip_start)
            strip = text[strip_start:start]
            with self.subTest(page=name):
                self.assertLess(hero_end, strip_start)
                self.assertLess(strip_start, start)
                self.assertIn('aria-hidden="true"', strip)
                self.assertEqual(strip.count('class="provider-strip-group"'), 4)
                self.assertEqual(strip.count('class="provider-strip-item"'), 24)
                for brand in ("google", "samsung", "xiaomi", "redmi", "poco", "oneplus"):
                    self.assertEqual(strip.count(f"assets/brands/{brand}.png"), 4)

    def test_app_is_labelled_early_mvp_and_has_a_download(self):
        for name, label, note in (
            ("index.html", "Early MVP", "Download the app"),
            ("es.html", "MVP temprano", "Descarga la app"),
        ):
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn(label, text)
                self.assertIn(note, text)
                self.assertIn("Windows 10/11", text)
                self.assertIn("OnePlus 6T", text)
                self.assertIn("v0.2.0", text)
                self.assertIn("cleanyourphone-app/releases/latest", text)
                self.assertIn("docs/CONNECT.md", text)

    def test_app_ctas_download_the_release(self):
        for name, cta_label, heading, step, final in (
            (
                "index.html",
                "Download for Windows",
                "Use the skill. The app is in development.",
                "Open the repo, enable USB debugging",
                "The app is still in development.",
            ),
            (
                "es.html",
                "Descargar para Windows",
                "Usa la skill. La app está en desarrollo.",
                "Abre el repo, activa la depuración USB",
                "La app aún está en desarrollo.",
            ),
        ):
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn(heading, text)
                self.assertIn(step, text)
                self.assertIn(final, text)
                links = re.findall(
                    r'<a class="button button-ghost" href="https://github\.com/jparedesDS/cleanyourphone-app/releases/latest"[^>]*>(.*?)</a>',
                    text,
                )
                self.assertEqual(len(links), 3)
                for inner in links:
                    self.assertIn(cta_label, inner)
                self.assertNotIn("App status", text)
                self.assertNotIn("Estado de la app", text)
                self.assertNotIn("open the app", text.lower())
                self.assertNotIn("abre la app", text.lower())

    def test_no_unrelated_project_reference(self):
        """The site must not claim an unrelated project as its inspiration."""
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8").lower()
            with self.subTest(page=name):
                self.assertNotIn("cleanyour.tv", text)

    def test_no_todo_markers(self):
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertNotIn("TODO", text)
                self.assertNotIn("FIXME", text)

    def test_no_inline_styles(self):
        """The CSP allows style-src 'self', so inline style attributes must not be used."""
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertNotIn("style=", text)

    def test_csp_hash_matches_json_ld(self):
        for name in PAGES_WITH_JSONLD:
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                block = re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
                self.assertIsNotNone(block)
                payload = block.group(1)
                json.loads(payload)
                digest = base64.b64encode(hashlib.sha256(payload.encode("utf-8")).digest()).decode()
                csp = re.search(r'Content-Security-Policy" content="([^"]+)"', text)
                self.assertIsNotNone(csp)
                self.assertIn(f"'sha256-{digest}'", csp.group(1))

    def test_no_third_party_requests(self):
        """The landing page must not load external scripts, styles, fonts or images."""
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            for target in re.findall(r'src="([^"]+)"', text):
                with self.subTest(page=name, src=target):
                    self.assertFalse(target.startswith("http"), target)
            for tag in re.findall(r"<link\b[^>]*>", text):
                if 'rel="stylesheet"' in tag or 'rel="icon"' in tag:
                    href = re.search(r'href="([^"]+)"', tag)
                    if href:
                        with self.subTest(page=name, link=href.group(1)):
                            self.assertFalse(href.group(1).startswith("http"), href.group(1))

        css = (ROOT / "styles.css").read_text(encoding="utf-8").lower()
        self.assertNotIn("@import", css)
        self.assertNotIn("url(http", css)

        js = (ROOT / "app.js").read_text(encoding="utf-8").lower()
        for marker in ("xmlhttprequest", "websocket", "sendbeacon"):
            self.assertNotIn(marker, js)
        self.assertEqual(js.count("fetch("), 1)

    def test_feedback_form_only_posts_to_the_worker(self):
        endpoint = "https://cleanyourphone-feedback.subtitleme.workers.dev"
        for name in ("index.html", "es.html"):
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn('id="feedback-form"', text)
                self.assertIn(f'data-endpoint="{endpoint}"', text)
                self.assertIn("feedback-consent", text)
                self.assertIn(f"connect-src {endpoint}", text)
        js = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn(f"const endpoint", js)
        self.assertIn("fetch(endpoint", js)
        self.assertIn("Content-Type", js)

    def test_canonical_and_alternates(self):
        cases = {
            "index.html": BASE_URL,
            "es.html": f"{BASE_URL}es.html",
        }
        for name, canonical in cases.items():
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn(f'<link rel="canonical" href="{canonical}">', text)
                self.assertIn('hreflang="en"', text)
                self.assertIn('hreflang="es"', text)
                self.assertIn('hreflang="x-default"', text)

    def test_social_metadata(self):
        for name in PAGES_WITH_JSONLD:
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertEqual(text.count('name="twitter:card"'), 1)
                self.assertIn('property="og:image"', text)
                self.assertIn('property="og:image:width" content="1280"', text)
                self.assertIn('property="og:image:height" content="640"', text)
                self.assertIn('name="description"', text)

    def test_brand_assets(self):
        self.assertEqual(png_size(ROOT / "assets" / "og.png"), (1280, 640))
        self.assertEqual(png_size(ROOT / "assets" / "banner.png"), (1600, 440))
        self.assertTrue((ROOT / "assets" / "logo.svg").is_file())
        self.assertTrue((ROOT / "assets" / "favicon.svg").is_file())
        for name, size in (("banner-web.png", (1600, 440)), ("banner-skill.png", (1600, 440)),
                           ("social-web.png", (1280, 640)), ("social-skill.png", (1280, 640))):
            with self.subTest(asset=name):
                self.assertEqual(png_size(ROOT / "assets" / "brand" / name), size)

    def test_security_txt(self):
        security = (ROOT / ".well-known" / "security.txt").read_text(encoding="utf-8")
        self.assertIn("Contact:", security)
        self.assertIn("Expires:", security)
        self.assertIn("Canonical:", security)

    def test_sitemap(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn(BASE_URL, sitemap)
        self.assertIn(f"{BASE_URL}es.html", sitemap)


if __name__ == "__main__":
    unittest.main()
