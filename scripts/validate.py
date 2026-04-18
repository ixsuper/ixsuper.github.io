#!/usr/bin/env python3
"""
Site integrity check.

Verifies:
  1. Every locale has the same set of pages as the English root.
  2. Every <link rel="alternate" hreflang="..." href="..."> URL resolves
     to a real file on disk.
  3. Every <link rel="canonical" href="..."> URL resolves to a real file.
  4. No HTML file regressed back to a large inline <style> block (we
     extracted shared styles to /assets/{home,site}.css; new inline
     styles likely indicate a copy-paste mistake).

Exits non-zero on any failure so it can run in CI.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://ixsuper.github.io"
LOCALES = ["ar", "da", "de", "es", "fr", "hi", "id", "it", "ja", "ko",
           "ms", "nb", "nl", "pl", "pt", "ru", "sv", "th", "tr", "uk",
           "ur", "vi", "zh-Hans", "zh-Hant"]
APPS = ["echoes", "block-blaster", "colornumbermatch"]
INLINE_STYLE_BUDGET = 60  # lines; anything bigger is a regression

errors: list[str] = []
warnings: list[str] = []


def url_to_path(url: str) -> Path | None:
    """Map a site URL to the file on disk that GitHub Pages will serve."""
    if not url.startswith(SITE_URL):
        return None
    rel = url[len(SITE_URL):].lstrip("/")
    if not rel:
        return ROOT / "index.html"
    candidate = ROOT / rel
    if candidate.is_file():
        return candidate
    # Pretty URL -> directory index.html
    if (candidate / "index.html").is_file():
        return candidate / "index.html"
    # Maybe extension-less HTML file (e.g. /colornumbermatch/changelog)
    html = candidate.with_suffix(".html")
    if html.is_file():
        return html
    return None


def check_locale_parity() -> None:
    """Each locale dir must contain the same index.html / app subfolders as root."""
    expected = {"index.html"} | {f"{app}/index.html" for app in APPS}
    for locale in LOCALES:
        locale_root = ROOT / locale
        if not locale_root.is_dir():
            errors.append(f"missing locale directory: {locale}/")
            continue
        for rel in expected:
            if not (locale_root / rel).is_file():
                errors.append(f"missing page: {locale}/{rel}")


def check_links(html: Path) -> None:
    """Verify hreflang + canonical URLs in this file resolve on disk."""
    text = html.read_text(encoding="utf-8")
    for m in re.finditer(r'<link[^>]+rel="(alternate|canonical)"[^>]*>', text):
        tag = m.group(0)
        href_m = re.search(r'href="([^"]+)"', tag)
        if not href_m:
            continue
        href = href_m.group(1)
        if not href.startswith(SITE_URL):
            continue
        # Skip non-HTML alternates (RSS, etc.) — we only check page links.
        if 'type="application/rss+xml"' in tag:
            continue
        if url_to_path(href) is None:
            rel = html.relative_to(ROOT)
            errors.append(f"{rel}: broken link href={href}")


def check_inline_style_size(html: Path) -> None:
    """Flag large inline <style> blocks as a regression."""
    text = html.read_text(encoding="utf-8")
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.DOTALL):
        line_count = m.group(1).count("\n")
        if line_count > INLINE_STYLE_BUDGET:
            rel = html.relative_to(ROOT)
            warnings.append(
                f"{rel}: inline <style> has {line_count} lines "
                f"(budget {INLINE_STYLE_BUDGET}) — extract to a stylesheet?"
            )


def main() -> int:
    check_locale_parity()
    for html in ROOT.rglob("*.html"):
        # Skip files that aren't part of the published site
        if any(part.startswith(".") or part == "node_modules" for part in html.parts):
            continue
        check_links(html)
        check_inline_style_size(html)

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"\nOK — 0 errors, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
