#!/usr/bin/env python3
"""
Inject a sticky topbar into every HTML page on the site.

Idempotent: skips files that already contain `<nav class="topbar"`.

Run from the site root:
    python3 scripts/inject-topbar.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 25 supported language codes (must match build_locales.py)
LANGS = [
    "en", "ar", "da", "de", "es", "fr", "hi", "id", "it", "ja", "ko",
    "ms", "nb", "nl", "pl", "pt", "ru", "sv", "th", "tr", "uk", "ur",
    "vi", "zh-Hans", "zh-Hant",
]

# Per-language nav labels.
# Brand names (Echoes, Block Blaster, Color Match) stay in English.
NAV = {
    "home":      {
        "en": "Home", "ar": "الرئيسية", "da": "Hjem", "de": "Start",
        "es": "Inicio", "fr": "Accueil", "hi": "होम", "id": "Beranda",
        "it": "Home", "ja": "ホーム", "ko": "홈", "ms": "Laman Utama",
        "nb": "Hjem", "nl": "Home", "pl": "Strona główna", "pt": "Início",
        "ru": "Главная", "sv": "Hem", "th": "หน้าแรก", "tr": "Ana Sayfa",
        "uk": "Головна", "ur": "ہوم", "vi": "Trang chủ",
        "zh-Hans": "首页", "zh-Hant": "首頁",
    },
    "changelog": {
        "en": "Changelog", "ar": "سجل التغييرات", "da": "Ændringslog",
        "de": "Änderungen", "es": "Cambios", "fr": "Journal",
        "hi": "बदलाव", "id": "Catatan Perubahan", "it": "Novità",
        "ja": "更新履歴", "ko": "변경 내역", "ms": "Log Perubahan",
        "nb": "Endringslogg", "nl": "Wijzigingen", "pl": "Zmiany",
        "pt": "Novidades", "ru": "История", "sv": "Ändringslogg",
        "th": "บันทึกการเปลี่ยนแปลง", "tr": "Değişiklikler",
        "uk": "Зміни", "ur": "تبدیلیاں", "vi": "Nhật ký",
        "zh-Hans": "更新日志", "zh-Hant": "更新日誌",
    },
}

def prefix_for(lang: str) -> str:
    return "/" if lang == "en" else f"/{lang}/"

def topbar_html(lang: str, current: str) -> str:
    """
    current is one of: home, echoes, blocks, colors, other
    """
    p = prefix_for(lang)
    home_label = NAV["home"].get(lang, NAV["home"]["en"])
    changelog_label = NAV["changelog"].get(lang, NAV["changelog"]["en"])

    def link(href: str, label: str, key: str, extra_class: str = "") -> str:
        cls = f' class="{extra_class}"' if extra_class else ""
        aria = ' aria-current="page"' if current == key else ""
        return f'            <a href="{href}"{cls}{aria}>{label}</a>'

    links = "\n".join([
        link(p,                                 home_label,        "home"),
        link(f"{p}echoes/",                     "Echoes",          "echoes"),
        link(f"{p}block-blaster/",              "Block Blaster",   "blocks"),
        link(f"{p}colornumbermatch/",           "Color Match",     "colors"),
        link(f"{p}colornumbermatch/changelog",  changelog_label,   "changelog", "topbar-changelog"),
    ])

    return (
        '    <nav class="topbar" aria-label="Primary">\n'
        f'        <a class="topbar-brand" href="{p}">\n'
        '            <span class="topbar-mark" aria-hidden="true">Z</span>\n'
        '            <span class="topbar-name">Ziyad Alsuhaymi</span>\n'
        '        </a>\n'
        '        <div class="topbar-links">\n'
        f'{links}\n'
        '        </div>\n'
        '    </nav>\n'
    )


def detect_lang_from_path(rel_path: str) -> str:
    """
    Returns the language code based on the file's position under the site root.
    Default is 'en' for files at the root.
    """
    parts = rel_path.split(os.sep)
    if parts and parts[0] in LANGS and parts[0] != "en":
        return parts[0]
    return "en"


def detect_current_section(rel_path: str) -> str:
    """
    Returns one of: home, echoes, blocks, colors, other
    """
    parts = rel_path.split(os.sep)
    # Strip leading lang dir if present
    if parts and parts[0] in LANGS and parts[0] != "en":
        parts = parts[1:]
    if not parts or parts == [""]:
        return "home"
    head = parts[0]
    if head == "index.html":
        return "home"
    if head == "echoes":
        return "echoes"
    if head == "block-blaster":
        return "blocks"
    if head == "colornumbermatch":
        if len(parts) >= 2 and parts[1].startswith("changelog"):
            return "changelog"
        return "colors"
    return "other"


def inject_into_file(abs_path: str, rel_path: str) -> bool:
    with open(abs_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Idempotent: skip if topbar already injected
    if '<nav class="topbar"' in html:
        return False

    lang = detect_lang_from_path(rel_path)
    current = detect_current_section(rel_path)
    bar = topbar_html(lang, current)

    # Insert immediately after <body ...> tag
    body_re = re.compile(r"(<body[^>]*>)")
    new_html, n = body_re.subn(lambda m: m.group(1) + "\n" + bar, html, count=1)
    if n == 0:
        return False

    # Hide the legacy nav.nav back-link by adding the topbar — CSS already
    # hides it for subpages, but on translated index.html the homepage CSS
    # is inline and there is no .nav, so nothing extra to do here.

    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    return True


def is_target_html(rel_path: str) -> bool:
    if not rel_path.endswith(".html"):
        return False
    parts = rel_path.split(os.sep)
    skip_dirs = {"node_modules", "scripts", ".git"}
    if any(p in skip_dirs for p in parts):
        return False
    return True


def main() -> int:
    changed = 0
    skipped = 0
    for dirpath, _dirs, files in os.walk(ROOT):
        for fn in files:
            abs_path = os.path.join(dirpath, fn)
            rel_path = os.path.relpath(abs_path, ROOT)
            if not is_target_html(rel_path):
                continue
            if inject_into_file(abs_path, rel_path):
                changed += 1
                print(f"  injected: {rel_path}")
            else:
                skipped += 1

    print(f"\nDone. {changed} files updated, {skipped} skipped (already had topbar or no <body>).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
