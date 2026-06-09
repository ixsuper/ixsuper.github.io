#!/usr/bin/env python3
"""
Build localized index.html files for ixsuper.github.io.

Reads the English /index.html template and writes a translated copy to
/<lang>/index.html for every language in TRANSLATIONS. Also injects a
shared hreflang block and a language-switcher <select> into every page
(including the English root).

Run from the site root:
    python3 scripts/build-locales.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index.html")

# Make sibling modules importable when run from any cwd.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n_hero import NEW_T  # noqa: E402

# -----------------------------------------------------------------------------
# Language metadata: (code, endonym, dir)
# 25 languages = English + 24 others.
# -----------------------------------------------------------------------------
LANGUAGES = [
    ("en",      "English",              "ltr"),
    ("ar",      "العربية",              "rtl"),
    ("da",      "Dansk",                "ltr"),
    ("de",      "Deutsch",              "ltr"),
    ("es",      "Español",              "ltr"),
    ("fr",      "Français",             "ltr"),
    ("hi",      "हिन्दी",                 "ltr"),
    ("id",      "Bahasa Indonesia",     "ltr"),
    ("it",      "Italiano",             "ltr"),
    ("ja",      "日本語",               "ltr"),
    ("ko",      "한국어",               "ltr"),
    ("ms",      "Bahasa Melayu",        "ltr"),
    ("nb",      "Norsk Bokmål",         "ltr"),
    ("nl",      "Nederlands",           "ltr"),
    ("pl",      "Polski",               "ltr"),
    ("pt",      "Português",            "ltr"),
    ("ru",      "Русский",              "ltr"),
    ("sv",      "Svenska",              "ltr"),
    ("th",      "ไทย",                  "ltr"),
    ("tr",      "Türkçe",               "ltr"),
    ("uk",      "Українська",           "ltr"),
    ("ur",      "اردو",                 "rtl"),
    ("vi",      "Tiếng Việt",           "ltr"),
    ("zh-Hans", "简体中文",             "ltr"),
    ("zh-Hant", "繁體中文",             "ltr"),
]

# -----------------------------------------------------------------------------
# Translation strings. Key = string key, value = dict of { lang: translation }.
# Brand names (Ziyad Alsuhaymi, Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus, Color Number Match)
# are intentionally NOT translated.
# -----------------------------------------------------------------------------
T = {
    "page_title": {
        "en": "Ziyad Alsuhaymi — iOS Apps & Games Developer",
        "ar": "زياد السحيمي — مطوّر تطبيقات وألعاب iOS",
        "da": "Ziyad Alsuhaymi — iOS-apps og spiludvikler",
        "de": "Ziyad Alsuhaymi — iOS-App- und Spieleentwickler",
        "es": "Ziyad Alsuhaymi — Desarrollador de apps y juegos para iOS",
        "fr": "Ziyad Alsuhaymi — Développeur d’apps et de jeux iOS",
        "hi": "ज़ियाद अल्सुहैमी — iOS ऐप्स और गेम्स डेवलपर",
        "id": "Ziyad Alsuhaymi — Pengembang Aplikasi & Gim iOS",
        "it": "Ziyad Alsuhaymi — Sviluppatore di app e giochi iOS",
        "ja": "Ziyad Alsuhaymi — iOSアプリ＆ゲーム開発者",
        "ko": "Ziyad Alsuhaymi — iOS 앱 및 게임 개발자",
        "ms": "Ziyad Alsuhaymi — Pembangun Aplikasi & Permainan iOS",
        "nb": "Ziyad Alsuhaymi — iOS-app- og spillutvikler",
        "nl": "Ziyad Alsuhaymi — iOS-apps en -games ontwikkelaar",
        "pl": "Ziyad Alsuhaymi — Twórca aplikacji i gier iOS",
        "pt": "Ziyad Alsuhaymi — Desenvolvedor de apps e jogos iOS",
        "ru": "Зияд Альсухайми — Разработчик приложений и игр для iOS",
        "sv": "Ziyad Alsuhaymi — iOS-app- och spelutvecklare",
        "th": "Ziyad Alsuhaymi — นักพัฒนาแอปและเกม iOS",
        "tr": "Ziyad Alsuhaymi — iOS Uygulama ve Oyun Geliştiricisi",
        "uk": "Зіяд Альсухаймі — Розробник застосунків та ігор для iOS",
        "ur": "زیاد السحیمی — iOS ایپس اور گیمز ڈیولپر",
        "vi": "Ziyad Alsuhaymi — Nhà phát triển ứng dụng & trò chơi iOS",
        "zh-Hans": "Ziyad Alsuhaymi — iOS 应用与游戏开发者",
        "zh-Hant": "Ziyad Alsuhaymi — iOS 應用與遊戲開發者",
    },
    "meta_description": {
        "en": "Premium iOS apps and games by Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus, and Color Number Match.",
        "ar": "تطبيقات وألعاب iOS متميزة من زياد السحيمي. Echoes و Upcomin' و Block Blaster Puzzle و Tempo Focus و Color Number Match.",
        "da": "Premium iOS-apps og spil af Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus og Color Number Match.",
        "de": "Premium iOS-Apps und Spiele von Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus und Color Number Match.",
        "es": "Apps y juegos premium para iOS de Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus y Color Number Match.",
        "fr": "Apps et jeux iOS premium de Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus et Color Number Match.",
        "hi": "ज़ियाद अल्सुहैमी द्वारा प्रीमियम iOS ऐप्स और गेम्स। Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus और Color Number Match।",
        "id": "Aplikasi dan gim iOS premium oleh Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus, dan Color Number Match.",
        "it": "App e giochi iOS premium di Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus e Color Number Match.",
        "ja": "Ziyad AlsuhaymiによるプレミアムiOSアプリとゲーム。Echoes、Upcomin'、Block Blaster Puzzle、Tempo Focus、Color Number Match。",
        "ko": "Ziyad Alsuhaymi의 프리미엄 iOS 앱 및 게임. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus, Color Number Match.",
        "ms": "Aplikasi dan permainan iOS premium oleh Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus, dan Color Number Match.",
        "nb": "Premium iOS-apper og spill av Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus og Color Number Match.",
        "nl": "Premium iOS-apps en -games van Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus en Color Number Match.",
        "pl": "Wysokiej jakości aplikacje i gry na iOS od Ziyada Alsuhaymiego. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus i Color Number Match.",
        "pt": "Apps e jogos premium para iOS por Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus e Color Number Match.",
        "ru": "Премиум приложения и игры для iOS от Зияда Альсухайми. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus и Color Number Match.",
        "sv": "Premium iOS-appar och spel av Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus och Color Number Match.",
        "th": "แอปและเกม iOS ระดับพรีเมียมโดย Ziyad Alsuhaymi ได้แก่ Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus และ Color Number Match",
        "tr": "Ziyad Alsuhaymi tarafından üretilen premium iOS uygulamaları ve oyunları. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus ve Color Number Match.",
        "uk": "Преміальні застосунки та ігри для iOS від Зіяда Альсухаймі. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus та Color Number Match.",
        "ur": "زیاد السحیمی کی جانب سے پریمیم iOS ایپس اور گیمز۔ Echoes، Upcomin'، Block Blaster Puzzle، Tempo Focus اور Color Number Match۔",
        "vi": "Ứng dụng và trò chơi iOS cao cấp của Ziyad Alsuhaymi. Echoes, Upcomin', Block Blaster Puzzle, Tempo Focus và Color Number Match.",
        "zh-Hans": "Ziyad Alsuhaymi 出品的高品质 iOS 应用与游戏。Echoes、Upcomin'、Block Blaster Puzzle、Tempo Focus 和 Color Number Match。",
        "zh-Hant": "Ziyad Alsuhaymi 出品的高品質 iOS 應用與遊戲。Echoes、Upcomin'、Block Blaster Puzzle、Tempo Focus 和 Color Number Match。",
    },
    "brand_subtitle": {
        "en": "iOS Apps & Games Developer",
        "ar": "مطوّر تطبيقات وألعاب iOS",
        "da": "iOS-apps og spiludvikler",
        "de": "iOS-App- und Spieleentwickler",
        "es": "Desarrollador de apps y juegos para iOS",
        "fr": "Développeur d’apps et de jeux iOS",
        "hi": "iOS ऐप्स और गेम्स डेवलपर",
        "id": "Pengembang Aplikasi & Gim iOS",
        "it": "Sviluppatore di app e giochi iOS",
        "ja": "iOSアプリ＆ゲーム開発者",
        "ko": "iOS 앱 및 게임 개발자",
        "ms": "Pembangun Aplikasi & Permainan iOS",
        "nb": "iOS-app- og spillutvikler",
        "nl": "iOS-apps en -games ontwikkelaar",
        "pl": "Twórca aplikacji i gier iOS",
        "pt": "Desenvolvedor de apps e jogos iOS",
        "ru": "Разработчик приложений и игр для iOS",
        "sv": "iOS-app- och spelutvecklare",
        "th": "นักพัฒนาแอปและเกม iOS",
        "tr": "iOS Uygulama ve Oyun Geliştiricisi",
        "uk": "Розробник застосунків та ігор для iOS",
        "ur": "iOS ایپس اور گیمز ڈیولپر",
        "vi": "Nhà phát triển ứng dụng & trò chơi iOS",
        "zh-Hans": "iOS 应用与游戏开发者",
        "zh-Hant": "iOS 應用與遊戲開發者",
    },
    "badge_new": {
        "en": "New", "ar": "جديد", "da": "Nyt", "de": "Neu", "es": "Nuevo",
        "fr": "Nouveau", "hi": "नया", "id": "Baru", "it": "Nuovo", "ja": "新着",
        "ko": "신규", "ms": "Baharu", "nb": "Nytt", "nl": "Nieuw", "pl": "Nowość",
        "pt": "Novo", "ru": "Новое", "sv": "Nytt", "th": "ใหม่", "tr": "Yeni",
        "uk": "Нове", "ur": "نیا", "vi": "Mới", "zh-Hans": "新品", "zh-Hant": "新品",
    },
    "badge_soon": {
        "en": "Coming Soon", "ar": "قريبًا", "da": "Kommer snart", "de": "Bald verfügbar",
        "es": "Próximamente", "fr": "Bientôt disponible", "hi": "जल्द आ रहा है",
        "id": "Segera Hadir", "it": "Prossimamente", "ja": "近日公開", "ko": "출시 예정",
        "ms": "Akan Datang", "nb": "Kommer snart", "nl": "Binnenkort", "pl": "Wkrótce",
        "pt": "Em breve", "ru": "Скоро", "sv": "Kommer snart", "th": "เร็วๆ นี้",
        "tr": "Çok Yakında", "uk": "Незабаром", "ur": "جلد آرہا ہے", "vi": "Sắp ra mắt",
        "zh-Hans": "即将推出", "zh-Hant": "即將推出",
    },
    "badge_live": {
        "en": "Live", "ar": "متاح", "da": "Tilgængelig", "de": "Verfügbar",
        "es": "Disponible", "fr": "Disponible", "hi": "उपलब्ध", "id": "Tersedia",
        "it": "Disponibile", "ja": "配信中", "ko": "출시됨", "ms": "Tersedia",
        "nb": "Tilgjengelig", "nl": "Beschikbaar", "pl": "Dostępne", "pt": "Disponível",
        "ru": "Доступно", "sv": "Tillgänglig", "th": "เปิดให้บริการ", "tr": "Yayında",
        "uk": "Доступно", "ur": "دستیاب", "vi": "Đã phát hành",
        "zh-Hans": "现已上架", "zh-Hant": "現已上架",
    },
    "btn_coming_soon": {
        "en": "Coming Soon", "ar": "قريبًا", "da": "Kommer snart", "de": "Bald verfügbar",
        "es": "Próximamente", "fr": "Bientôt disponible", "hi": "जल्द आ रहा है",
        "id": "Segera Hadir", "it": "Prossimamente", "ja": "近日公開", "ko": "출시 예정",
        "ms": "Akan Datang", "nb": "Kommer snart", "nl": "Binnenkort", "pl": "Wkrótce",
        "pt": "Em breve", "ru": "Скоро", "sv": "Kommer snart", "th": "เร็วๆ นี้",
        "tr": "Çok Yakında", "uk": "Незабаром", "ur": "جلد آرہا ہے", "vi": "Sắp ra mắt",
        "zh-Hans": "即将推出", "zh-Hant": "即將推出",
    },
    "btn_download": {
        "en": "Download on the App Store",
        "ar": "تنزيل من متجر App Store",
        "da": "Hent i App Store",
        "de": "Laden im App Store",
        "es": "Descargar en el App Store",
        "fr": "Télécharger dans l’App Store",
        "hi": "App Store पर डाउनलोड करें",
        "id": "Unduh di App Store",
        "it": "Scarica su App Store",
        "ja": "App Storeからダウンロード",
        "ko": "App Store에서 다운로드",
        "ms": "Muat Turun dari App Store",
        "nb": "Last ned fra App Store",
        "nl": "Download in de App Store",
        "pl": "Pobierz w App Store",
        "pt": "Baixar na App Store",
        "ru": "Загрузить в App Store",
        "sv": "Ladda ned i App Store",
        "th": "ดาวน์โหลดจาก App Store",
        "tr": "App Store’dan İndir",
        "uk": "Завантажити в App Store",
        "ur": "App Store سے ڈاؤن لوڈ کریں",
        "vi": "Tải trên App Store",
        "zh-Hans": "从 App Store 下载",
        "zh-Hant": "從 App Store 下載",
    },
    "link_learn_more": {
        "en": "Learn More", "ar": "المزيد", "da": "Læs mere", "de": "Mehr erfahren",
        "es": "Más información", "fr": "En savoir plus", "hi": "और जानें",
        "id": "Pelajari Lebih", "it": "Scopri di più", "ja": "詳細を見る",
        "ko": "자세히 보기", "ms": "Ketahui Lebih", "nb": "Les mer", "nl": "Meer info",
        "pl": "Dowiedz się więcej", "pt": "Saiba mais", "ru": "Подробнее",
        "sv": "Läs mer", "th": "เรียนรู้เพิ่ม", "tr": "Daha Fazla",
        "uk": "Детальніше", "ur": "مزید جانیں", "vi": "Tìm hiểu thêm",
        "zh-Hans": "了解更多", "zh-Hant": "了解更多",
    },
    "link_privacy": {
        "en": "Privacy Policy", "ar": "سياسة الخصوصية", "da": "Privatlivspolitik",
        "de": "Datenschutz", "es": "Política de privacidad", "fr": "Politique de confidentialité",
        "hi": "गोपनीयता नीति", "id": "Kebijakan Privasi", "it": "Privacy",
        "ja": "プライバシーポリシー", "ko": "개인정보 처리방침", "ms": "Dasar Privasi",
        "nb": "Personvern", "nl": "Privacybeleid", "pl": "Polityka prywatności",
        "pt": "Política de privacidade", "ru": "Конфиденциальность",
        "sv": "Integritetspolicy", "th": "นโยบายความเป็นส่วนตัว", "tr": "Gizlilik Politikası",
        "uk": "Конфіденційність", "ur": "رازداری پالیسی", "vi": "Chính sách quyền riêng tư",
        "zh-Hans": "隐私政策", "zh-Hant": "私隱政策",
    },
    "link_terms": {
        "en": "Terms of Use", "ar": "شروط الاستخدام", "da": "Vilkår",
        "de": "Nutzungsbedingungen", "es": "Términos de uso", "fr": "Conditions d’utilisation",
        "hi": "उपयोग की शर्तें", "id": "Syarat Penggunaan", "it": "Termini d’uso",
        "ja": "利用規約", "ko": "이용 약관", "ms": "Terma Penggunaan",
        "nb": "Vilkår", "nl": "Gebruiksvoorwaarden", "pl": "Warunki użytkowania",
        "pt": "Termos de uso", "ru": "Условия использования",
        "sv": "Användarvillkor", "th": "เงื่อนไขการใช้งาน", "tr": "Kullanım Koşulları",
        "uk": "Умови використання", "ur": "شرائط استعمال", "vi": "Điều khoản sử dụng",
        "zh-Hans": "使用条款", "zh-Hant": "使用條款",
    },
    "link_support": {
        "en": "Support", "ar": "الدعم", "da": "Support", "de": "Support",
        "es": "Soporte", "fr": "Support", "hi": "सहायता", "id": "Dukungan",
        "it": "Supporto", "ja": "サポート", "ko": "지원", "ms": "Sokongan",
        "nb": "Støtte", "nl": "Ondersteuning", "pl": "Pomoc", "pt": "Suporte",
        "ru": "Поддержка", "sv": "Support", "th": "ฝ่ายสนับสนุน", "tr": "Destek",
        "uk": "Підтримка", "ur": "سپورٹ", "vi": "Hỗ trợ",
        "zh-Hans": "支持", "zh-Hant": "支援",
    },
    "link_changelog": {
        "en": "Changelog", "ar": "سجل التغييرات", "da": "Ændringslog",
        "de": "Änderungsprotokoll", "es": "Registro de cambios", "fr": "Journal des modifications",
        "hi": "चेंजलॉग", "id": "Changelog", "it": "Changelog", "ja": "更新履歴",
        "ko": "변경 로그", "ms": "Changelog", "nb": "Endringslogg", "nl": "Wijzigingslogboek",
        "pl": "Lista zmian", "pt": "Registro de alterações", "ru": "История изменений",
        "sv": "Ändringslogg", "th": "บันทึกการเปลี่ยนแปลง", "tr": "Değişiklikler",
        "uk": "Журнал змін", "ur": "تبدیلیوں کا لاگ", "vi": "Nhật ký thay đổi",
        "zh-Hans": "更新日志", "zh-Hant": "更新日誌",
    },
    "echoes_desc": {
        "en": "Capture living memories with photo, ambient sound, weather, and location. Built for iOS 26 with Liquid Glass, on-device ML, and an immersive memory map. 14 languages.",
        "ar": "التقط ذكريات نابضة بالحياة مع الصورة والصوت المحيط والطقس والموقع. مصمَّم لنظام iOS 26 مع Liquid Glass وتعلّم الآلة على الجهاز وخريطة ذكريات غامرة. بـ 14 لغة.",
        "da": "Fang levende minder med foto, omgivelseslyd, vejr og placering. Bygget til iOS 26 med Liquid Glass, on-device ML og et medrivende hukommelseskort. 14 sprog.",
        "de": "Halte lebendige Erinnerungen mit Foto, Umgebungsgeräuschen, Wetter und Standort fest. Entwickelt für iOS 26 mit Liquid Glass, On-Device-ML und einer immersiven Erinnerungskarte. 14 Sprachen.",
        "es": "Captura recuerdos vivos con foto, sonido ambiente, clima y ubicación. Creado para iOS 26 con Liquid Glass, ML en el dispositivo y un mapa de recuerdos inmersivo. 14 idiomas.",
        "fr": "Capturez des souvenirs vivants avec photo, son ambiant, météo et lieu. Conçu pour iOS 26 avec Liquid Glass, ML sur l’appareil et une carte mémoire immersive. 14 langues.",
        "hi": "फोटो, परिवेशी ध्वनि, मौसम और स्थान के साथ जीवंत यादें कैद करें। iOS 26 के लिए Liquid Glass, ऑन-डिवाइस ML और एक इमर्सिव मेमरी मैप के साथ बनाया गया। 14 भाषाएँ।",
        "id": "Rekam kenangan hidup dengan foto, suara sekitar, cuaca, dan lokasi. Dibangun untuk iOS 26 dengan Liquid Glass, ML di perangkat, dan peta kenangan imersif. 14 bahasa.",
        "it": "Cattura ricordi vivi con foto, suono ambientale, meteo e posizione. Creato per iOS 26 con Liquid Glass, ML sul dispositivo e una mappa dei ricordi immersiva. 14 lingue.",
        "ja": "写真、環境音、天気、位置情報とともに生きた思い出を記録。iOS 26向けにLiquid Glass、オンデバイスML、没入型メモリーマップで構築。14言語対応。",
        "ko": "사진, 주변 소리, 날씨, 위치와 함께 생생한 추억을 기록하세요. Liquid Glass, 온디바이스 ML, 몰입형 메모리 맵을 탑재한 iOS 26용입니다. 14개 언어 지원.",
        "ms": "Rakam kenangan hidup dengan foto, bunyi persekitaran, cuaca dan lokasi. Dibina untuk iOS 26 dengan Liquid Glass, ML pada peranti dan peta kenangan mendalam. 14 bahasa.",
        "nb": "Fang levende minner med foto, omgivelseslyd, vær og sted. Bygget for iOS 26 med Liquid Glass, ML på enheten og et oppslukende minnekart. 14 språk.",
        "nl": "Leg levende herinneringen vast met foto, omgevingsgeluid, weer en locatie. Gemaakt voor iOS 26 met Liquid Glass, on-device ML en een meeslepende herinneringenkaart. 14 talen.",
        "pl": "Uchwyć żywe wspomnienia za pomocą zdjęcia, dźwięku otoczenia, pogody i lokalizacji. Stworzone dla iOS 26 z Liquid Glass, ML na urządzeniu i wciągającą mapą wspomnień. 14 języków.",
        "pt": "Capture memórias vivas com foto, som ambiente, clima e localização. Desenvolvido para iOS 26 com Liquid Glass, ML no dispositivo e um mapa de memórias imersivo. 14 idiomas.",
        "ru": "Запечатлейте живые воспоминания с фото, окружающим звуком, погодой и местоположением. Создано для iOS 26 с Liquid Glass, ML на устройстве и иммерсивной картой воспоминаний. 14 языков.",
        "sv": "Fånga levande minnen med foto, omgivningsljud, väder och plats. Byggd för iOS 26 med Liquid Glass, ML på enheten och en uppslukande minneskarta. 14 språk.",
        "th": "บันทึกความทรงจำที่มีชีวิตด้วยภาพถ่าย เสียงแวดล้อม สภาพอากาศ และตำแหน่ง สร้างขึ้นสำหรับ iOS 26 พร้อม Liquid Glass, ML บนอุปกรณ์ และแผนที่ความทรงจำที่สมจริง รองรับ 14 ภาษา",
        "tr": "Fotoğraf, ortam sesi, hava durumu ve konumla canlı anılar yakalayın. iOS 26 için Liquid Glass, cihazda ML ve sürükleyici bir anı haritasıyla tasarlandı. 14 dil.",
        "uk": "Записуйте живі спогади з фото, навколишнім звуком, погодою та місцем. Створено для iOS 26 з Liquid Glass, ML на пристрої та імерсивною мапою спогадів. 14 мов.",
        "ur": "تصویر، ماحولیاتی آواز، موسم اور مقام کے ساتھ زندہ یادیں محفوظ کریں۔ iOS 26 کے لیے Liquid Glass، آن-ڈیوائس ML اور عمیق میموری میپ کے ساتھ تیار کیا گیا۔ 14 زبانوں میں۔",
        "vi": "Lưu giữ những kỷ niệm sống động với ảnh, âm thanh môi trường, thời tiết và vị trí. Thiết kế cho iOS 26 với Liquid Glass, ML trên thiết bị và bản đồ kỷ niệm sống động. 14 ngôn ngữ.",
        "zh-Hans": "用照片、环境声、天气和位置捕捉鲜活的记忆。专为 iOS 26 打造，搭载 Liquid Glass、端侧机器学习和沉浸式记忆地图。支持 14 种语言。",
        "zh-Hant": "用照片、環境聲、天氣和位置捕捉鮮活的記憶。專為 iOS 26 打造，搭載 Liquid Glass、端側機器學習和沉浸式記憶地圖。支援 14 種語言。",
    },
    "blocks_desc": {
        "en": "A satisfying block puzzle game with explosive combos, sensory themes, and haptic feedback. 5 game modes, 50 adventure levels, 7 languages.",
        "ar": "لعبة ألغاز مكعّبات ممتعة مع كومبوات متفجّرة وثيمات حسّية وردود فعل لمسية. 5 أنماط لعب و50 مستوى مغامرة وبـ7 لغات.",
        "da": "Et tilfredsstillende blokspil med eksplosive combos, sansetemaer og haptisk feedback. 5 spilmodi, 50 eventyrbaner, 7 sprog.",
        "de": "Ein befriedigendes Blockpuzzle mit explosiven Combos, Sinnesthemen und haptischem Feedback. 5 Spielmodi, 50 Abenteuer-Level, 7 Sprachen.",
        "es": "Un satisfactorio juego de rompecabezas con combos explosivos, temas sensoriales y retroalimentación háptica. 5 modos de juego, 50 niveles de aventura, 7 idiomas.",
        "fr": "Un jeu de puzzle de blocs satisfaisant avec combos explosifs, thèmes sensoriels et retour haptique. 5 modes de jeu, 50 niveaux d’aventure, 7 langues.",
        "hi": "विस्फोटक कॉम्बो, सेंसरी थीम और हैप्टिक फीडबैक वाला संतोषजनक ब्लॉक पज़ल गेम। 5 गेम मोड, 50 एडवेंचर लेवल, 7 भाषाएँ।",
        "id": "Gim teka-teki blok yang memuaskan dengan kombo eksplosif, tema sensorik, dan umpan balik haptik. 5 mode permainan, 50 level petualangan, 7 bahasa.",
        "it": "Un appagante gioco di puzzle a blocchi con combo esplosive, temi sensoriali e feedback aptico. 5 modalità, 50 livelli avventura, 7 lingue.",
        "ja": "爆発的なコンボ、五感テーマ、ハプティックフィードバックが満載のブロックパズル。5つのゲームモード、50のアドベンチャーレベル、7言語対応。",
        "ko": "폭발적인 콤보, 감각 테마, 햅틱 피드백이 어우러진 만족스러운 블록 퍼즐 게임. 5가지 모드, 50개 어드벤처 레벨, 7개 언어.",
        "ms": "Permainan teka-teki blok yang memuaskan dengan kombo meletup, tema deria dan maklum balas haptik. 5 mod permainan, 50 tahap pengembaraan, 7 bahasa.",
        "nb": "Et tilfredsstillende blokkspill med eksplosive combos, sansetemaer og haptisk tilbakemelding. 5 spillmoduser, 50 eventyrnivåer, 7 språk.",
        "nl": "Een bevredigend blokpuzzelspel met explosieve combo’s, sensorische thema’s en haptische feedback. 5 spelmodi, 50 avontuurlevels, 7 talen.",
        "pl": "Satysfakcjonująca gra logiczna z blokami, wybuchowymi combosami, motywami zmysłowymi i wibracjami haptycznymi. 5 trybów, 50 poziomów przygody, 7 języków.",
        "pt": "Um jogo de quebra-cabeça de blocos satisfatório com combos explosivos, temas sensoriais e feedback háptico. 5 modos de jogo, 50 níveis de aventura, 7 idiomas.",
        "ru": "Захватывающая головоломка с блоками, взрывными комбо, сенсорными темами и тактильной отдачей. 5 режимов, 50 приключенческих уровней, 7 языков.",
        "sv": "Ett tillfredsställande blockpusselspel med explosiva kombos, sinnesteman och haptisk feedback. 5 spellägen, 50 äventyrsnivåer, 7 språk.",
        "th": "เกมปริศนาบล็อกที่สนุกเร้าใจ พร้อมคอมโบระเบิด ธีมประสาทสัมผัส และการตอบสนองแบบสัมผัส 5 โหมดเกม, 50 ด่านผจญภัย, 7 ภาษา",
        "tr": "Patlayıcı kombolar, duyusal temalar ve haptik geri bildirimle tatmin edici bir blok bulmaca oyunu. 5 oyun modu, 50 macera seviyesi, 7 dil.",
        "uk": "Приємна головоломка з блоками, вибуховими комбо, сенсорними темами та тактильним відгуком. 5 режимів, 50 пригодницьких рівнів, 7 мов.",
        "ur": "دھماکہ خیز کومبوز، حسی تھیمز اور ہیپٹک فیڈبیک کے ساتھ ایک اطمینان بخش بلاک پزل گیم۔ 5 گیم موڈز، 50 ایڈونچر لیولز، 7 زبانیں۔",
        "vi": "Trò chơi xếp khối thỏa mãn với combo bùng nổ, chủ đề cảm giác và phản hồi rung. 5 chế độ chơi, 50 màn phiêu lưu, 7 ngôn ngữ.",
        "zh-Hans": "一款令人满足的方块消除游戏，拥有爆炸性连击、感官主题和触觉反馈。5 种模式、50 个冒险关卡、7 种语言。",
        "zh-Hant": "一款令人滿足的方塊消除遊戲，擁有爆炸性連擊、感官主題和觸覺回饋。5 種模式、50 個冒險關卡、7 種語言。",
    },
    "cnm_desc": {
        "en": "A vibrant puzzle game with 2000+ levels across 10 packs. Match tiles by color or number with special tiles, Metal shaders, haptic feedback, and 24 languages including Arabic RTL.",
        "ar": "لعبة ألغاز نابضة بالحياة تضم أكثر من 2000 مستوى في 10 حزم. طابق البلاطات باللون أو الرقم مع بلاطات خاصة وتأثيرات Metal وردود فعل لمسية و24 لغة تشمل العربية من اليمين إلى اليسار.",
        "da": "Et livligt puslespil med 2000+ baner fordelt på 10 pakker. Match fliser efter farve eller tal med specielle fliser, Metal-shaders, haptisk feedback og 24 sprog inklusive arabisk RTL.",
        "de": "Ein lebendiges Puzzlespiel mit über 2000 Leveln in 10 Paketen. Verbinde Kacheln nach Farbe oder Zahl mit Spezialkacheln, Metal-Shadern, haptischem Feedback und 24 Sprachen inklusive arabisch RTL.",
        "es": "Un vibrante juego de puzles con más de 2000 niveles en 10 paquetes. Empareja fichas por color o número con fichas especiales, shaders Metal, retroalimentación háptica y 24 idiomas incluyendo árabe RTL.",
        "fr": "Un jeu de puzzle vibrant avec plus de 2000 niveaux répartis sur 10 packs. Associez les tuiles par couleur ou numéro avec des tuiles spéciales, des shaders Metal, un retour haptique et 24 langues dont l’arabe RTL.",
        "hi": "10 पैक में 2000+ स्तरों वाला जीवंत पज़ल गेम। रंग या संख्या से टाइलें मिलाएँ, विशेष टाइलें, Metal शेडर्स, हैप्टिक फीडबैक और अरबी RTL सहित 24 भाषाएँ।",
        "id": "Gim teka-teki yang hidup dengan 2000+ level dalam 10 paket. Cocokkan ubin berdasarkan warna atau angka dengan ubin spesial, shader Metal, umpan balik haptik, dan 24 bahasa termasuk Arab RTL.",
        "it": "Un vivace gioco di puzzle con oltre 2000 livelli in 10 pacchetti. Abbina le tessere per colore o numero con tessere speciali, shader Metal, feedback aptico e 24 lingue incluso l’arabo RTL.",
        "ja": "10パックにわたる2000以上のレベルを収録した色鮮やかなパズルゲーム。色や数字でタイルをマッチさせ、特殊タイル、Metalシェーダー、ハプティック、アラビア語RTL含む24言語に対応。",
        "ko": "10개 팩에 걸친 2000개 이상의 레벨을 갖춘 화려한 퍼즐 게임. 색깔이나 숫자로 타일을 맞추세요. 특수 타일, Metal 셰이더, 햅틱 피드백, 아랍어 RTL 포함 24개 언어 지원.",
        "ms": "Permainan teka-teki bertenaga dengan lebih 2000 tahap dalam 10 pakej. Padan jubin mengikut warna atau nombor dengan jubin istimewa, shader Metal, maklum balas haptik dan 24 bahasa termasuk Arab RTL.",
        "nb": "Et livlig puslespill med over 2000 brett fordelt på 10 pakker. Match brikker etter farge eller tall med spesialbrikker, Metal-shadere, haptisk tilbakemelding og 24 språk inkludert arabisk RTL.",
        "nl": "Een levendig puzzelspel met 2000+ levels in 10 pakketten. Koppel tegels op kleur of nummer met speciale tegels, Metal-shaders, haptische feedback en 24 talen inclusief Arabisch RTL.",
        "pl": "Żywiołowa gra logiczna z ponad 2000 poziomami w 10 paczkach. Dopasowuj kafelki według koloru lub liczby ze specjalnymi kafelkami, shaderami Metal, wibracjami haptycznymi i 24 językami włącznie z arabskim RTL.",
        "pt": "Um vibrante jogo de puzzle com mais de 2000 níveis em 10 pacotes. Combine peças por cor ou número com peças especiais, shaders Metal, feedback háptico e 24 idiomas incluindo árabe RTL.",
        "ru": "Яркая головоломка с более чем 2000 уровнями в 10 паках. Соединяйте плитки по цвету или числу с особыми плитками, Metal-шейдерами, тактильной отдачей и 24 языками, включая арабский RTL.",
        "sv": "Ett livfullt pusselspel med 2000+ banor fördelade på 10 paket. Matcha brickor efter färg eller nummer med specialbrickor, Metal-shaders, haptisk feedback och 24 språk inklusive arabiska RTL.",
        "th": "เกมปริศนาสีสันสดใสกว่า 2000+ ด่านใน 10 แพ็ก จับคู่ไทล์ตามสีหรือหมายเลขด้วยไทล์พิเศษ Metal shaders ระบบสัมผัส และ 24 ภาษารวมถึงอาหรับ RTL",
        "tr": "10 pakette 2000’den fazla seviyeye sahip canlı bir bulmaca oyunu. Özel karolar, Metal shader’ları, haptik geri bildirim ve Arapça RTL dahil 24 dille karoları renge veya sayıya göre eşleştirin.",
        "uk": "Яскрава головоломка з понад 2000 рівнів у 10 паках. Поєднуйте плитки за кольором чи числом зі спеціальними плитками, шейдерами Metal, тактильним відгуком і 24 мовами, включно з арабською RTL.",
        "ur": "10 پیکس میں 2000+ لیولز کے ساتھ ایک متحرک پزل گیم۔ رنگ یا نمبر سے ٹائلز ملائیں، خصوصی ٹائلز، Metal شیڈرز، ہیپٹک فیڈبیک اور عربی RTL سمیت 24 زبانیں۔",
        "vi": "Trò chơi giải đố sống động với hơn 2000 màn chơi trong 10 gói. Ghép ô theo màu hoặc số với ô đặc biệt, shader Metal, phản hồi rung và 24 ngôn ngữ bao gồm tiếng Ả Rập RTL.",
        "zh-Hans": "一款拥有 10 个关卡包、2000+ 关卡的绚丽益智游戏。按颜色或数字匹配方块，带特殊方块、Metal 着色器、触觉反馈和 24 种语言（含阿拉伯语 RTL）。",
        "zh-Hant": "一款擁有 10 個關卡包、2000+ 關卡的絢麗益智遊戲。依顏色或數字匹配方塊，帶特殊方塊、Metal 著色器、觸覺回饋和 24 種語言（含阿拉伯文 RTL）。",
    },
    "upcomin_desc": {
        "en": "Track every upcoming release — games, movies, TV, anime — in one beautifully bright iOS 26 app. Live Activities, Lock Screen widgets, Apple Intelligence guides, and a Global Launch Hub across 20 cities.",
        "ar": "تابع كل إصدار قادم — ألعاب وأفلام ومسلسلات وأنمي — في تطبيق iOS 26 واحد مشرق وجميل. أنشطة مباشرة، وودجات شاشة القفل، وأدلة Apple Intelligence، ومركز إطلاق عالمي يغطي 20 مدينة.",
        "da": "Følg alle kommende udgivelser — spil, film, tv og anime — i én smukt lys iOS 26-app. Live Activities, widgets på låseskærmen, Apple Intelligence-guider og et globalt launch-hub på tværs af 20 byer.",
        "de": "Verfolge jede kommende Veröffentlichung — Spiele, Filme, Serien, Anime — in einer wunderschön hellen iOS-26-App. Live Activities, Sperrbildschirm-Widgets, Apple-Intelligence-Guides und ein globaler Launch-Hub für 20 Städte.",
        "es": "Sigue cada próximo lanzamiento — juegos, películas, series y anime — en una sola app de iOS 26 brillante y hermosa. Live Activities, widgets de pantalla de bloqueo, guías de Apple Intelligence y un Launch Hub global con 20 ciudades.",
        "fr": "Suivez chaque sortie à venir — jeux, films, séries, anime — dans une seule app iOS 26 lumineuse et élégante. Live Activities, widgets d’écran verrouillé, guides Apple Intelligence et un Launch Hub mondial couvrant 20 villes.",
        "hi": "हर आगामी रिलीज़ को ट्रैक करें — गेम, फ़िल्में, टीवी, एनीमे — एक खूबसूरत iOS 26 ऐप में। Live Activities, लॉक स्क्रीन विजेट, Apple Intelligence गाइड और 20 शहरों वाला ग्लोबल लॉन्च हब।",
        "id": "Lacak setiap rilis mendatang — gim, film, TV, anime — dalam satu aplikasi iOS 26 yang cerah dan indah. Live Activities, widget Layar Kunci, panduan Apple Intelligence, dan Global Launch Hub di 20 kota.",
        "it": "Segui ogni uscita in arrivo — giochi, film, serie TV, anime — in un’unica app iOS 26 luminosa e curata. Live Activities, widget della schermata di blocco, guide Apple Intelligence e un Launch Hub globale in 20 città.",
        "ja": "ゲーム、映画、TV、アニメ — あらゆる新作リリースを、明るく美しいiOS 26アプリひとつで追跡。Live Activities、ロック画面ウィジェット、Apple Intelligenceガイド、20都市のグローバルローンチハブを搭載。",
        "ko": "게임, 영화, TV, 애니메이션 — 모든 출시 예정작을 하나의 아름답고 밝은 iOS 26 앱에서 추적하세요. Live Activities, 잠금 화면 위젯, Apple Intelligence 가이드, 20개 도시의 글로벌 런치 허브까지.",
        "ms": "Jejak setiap keluaran akan datang — permainan, filem, TV, anime — dalam satu aplikasi iOS 26 yang cerah dan indah. Live Activities, widget Skrin Kunci, panduan Apple Intelligence dan Global Launch Hub merentas 20 bandar.",
        "nb": "Følg alle kommende lanseringer — spill, filmer, TV og anime — i én vakkert lys iOS 26-app. Live Activities, widgeter på låst skjerm, Apple Intelligence-guider og en global launch-hub i 20 byer.",
        "nl": "Volg elke aankomende release — games, films, tv en anime — in één prachtig heldere iOS 26-app. Live Activities, toegangsscherm-widgets, Apple Intelligence-gidsen en een wereldwijde Launch Hub in 20 steden.",
        "pl": "Śledź każdą nadchodzącą premierę — gry, filmy, seriale, anime — w jednej pięknie jasnej aplikacji na iOS 26. Live Activities, widżety ekranu blokady, przewodniki Apple Intelligence i globalny Launch Hub w 20 miastach.",
        "pt": "Acompanhe cada lançamento futuro — jogos, filmes, TV e anime — em um único app iOS 26 lindamente claro. Live Activities, widgets da Tela Bloqueada, guias do Apple Intelligence e um Launch Hub global em 20 cidades.",
        "ru": "Следите за каждым будущим релизом — игры, фильмы, сериалы, аниме — в одном красивом и ярком приложении для iOS 26. Live Activities, виджеты экрана блокировки, гиды Apple Intelligence и глобальный центр запусков в 20 городах.",
        "sv": "Följ varje kommande släpp — spel, filmer, tv och anime — i en vackert ljus iOS 26-app. Live Activities, widgetar på låsskärmen, Apple Intelligence-guider och en global launch-hub i 20 städer.",
        "th": "ติดตามทุกการเปิดตัวที่กำลังจะมาถึง — เกม ภาพยนตร์ ทีวี อนิเมะ — ในแอป iOS 26 ที่สวยสดใสเพียงแอปเดียว พร้อม Live Activities วิดเจ็ตหน้าจอล็อก ไกด์ Apple Intelligence และ Global Launch Hub ครอบคลุม 20 เมือง",
        "tr": "Yaklaşan her çıkışı — oyunlar, filmler, diziler, anime — tek bir güzel ve aydınlık iOS 26 uygulamasında takip edin. Live Activities, Kilit Ekranı widget’ları, Apple Intelligence rehberleri ve 20 şehri kapsayan küresel Launch Hub.",
        "uk": "Стежте за кожним майбутнім релізом — ігри, фільми, серіали, аніме — в одному гарному та яскравому застосунку для iOS 26. Live Activities, віджети екрана блокування, гіди Apple Intelligence і глобальний хаб запусків у 20 містах.",
        "ur": "ہر آنے والی ریلیز کو ٹریک کریں — گیمز، فلمیں، ٹی وی، اینیمے — ایک خوبصورت روشن iOS 26 ایپ میں۔ Live Activities، لاک اسکرین وجٹس، Apple Intelligence گائیڈز اور 20 شہروں پر محیط عالمی لانچ ہب۔",
        "vi": "Theo dõi mọi bản phát hành sắp tới — game, phim, TV, anime — trong một ứng dụng iOS 26 tươi sáng tuyệt đẹp. Live Activities, tiện ích Màn hình khóa, hướng dẫn Apple Intelligence và Global Launch Hub tại 20 thành phố.",
        "zh-Hans": "在一款明亮精美的 iOS 26 应用中追踪每一个即将发布的作品 — 游戏、电影、剧集、动漫。支持实时活动、锁定屏幕小组件、Apple Intelligence 指南，以及覆盖 20 座城市的全球发布中心。",
        "zh-Hant": "在一款明亮精美的 iOS 26 App 中追蹤每一個即將推出的作品 — 遊戲、電影、影集、動漫。支援即時動態、鎖定畫面小工具、Apple Intelligence 指南，以及涵蓋 20 座城市的全球發佈中心。",
    },
    "tempo_desc": {
        "en": "A serious productivity tool. Pomodoro cycles, real app blocking via Screen Time, an AI coach, Live Activities, and iCloud sync. 10 languages including Arabic.",
        "ar": "أداة إنتاجية جادّة. دورات بومودورو، وحظر فعلي للتطبيقات عبر «مدة استخدام الجهاز»، ومدرّب ذكاء اصطناعي، وأنشطة مباشرة، ومزامنة iCloud. بـ 10 لغات من بينها العربية.",
        "da": "Et seriøst produktivitetsværktøj. Pomodoro-cyklusser, ægte app-blokering via Skærmtid, en AI-coach, Live Activities og iCloud-synkronisering. 10 sprog, herunder arabisk.",
        "de": "Ein ernsthaftes Produktivitätswerkzeug. Pomodoro-Zyklen, echtes App-Blocking über Bildschirmzeit, ein KI-Coach, Live Activities und iCloud-Sync. 10 Sprachen, darunter Arabisch.",
        "es": "Una herramienta de productividad seria. Ciclos Pomodoro, bloqueo real de apps mediante Tiempo de uso, un coach de IA, Live Activities y sincronización con iCloud. 10 idiomas, incluido el árabe.",
        "fr": "Un véritable outil de productivité. Cycles Pomodoro, blocage réel d’apps via Temps d’écran, un coach IA, Live Activities et synchronisation iCloud. 10 langues, dont l’arabe.",
        "hi": "एक गंभीर प्रोडक्टिविटी टूल। पोमोडोरो साइकल, Screen Time से असली ऐप ब्लॉकिंग, AI कोच, Live Activities और iCloud सिंक। अरबी सहित 10 भाषाएँ।",
        "id": "Alat produktivitas yang serius. Siklus Pomodoro, pemblokiran aplikasi sungguhan lewat Durasi Layar, pelatih AI, Live Activities, dan sinkronisasi iCloud. 10 bahasa termasuk Arab.",
        "it": "Uno strumento di produttività serio. Cicli Pomodoro, blocco reale delle app tramite Tempo di utilizzo, un coach IA, Live Activities e sincronizzazione iCloud. 10 lingue, incluso l’arabo.",
        "ja": "本気の生産性ツール。ポモドーロサイクル、スクリーンタイムによる本物のアプリブロック、AIコーチ、Live Activities、iCloud同期。アラビア語を含む10言語に対応。",
        "ko": "진지한 생산성 도구. 뽀모도로 사이클, 스크린 타임 기반의 실제 앱 차단, AI 코치, Live Activities, iCloud 동기화까지. 아랍어 포함 10개 언어 지원.",
        "ms": "Alat produktiviti yang serius. Kitaran Pomodoro, sekatan aplikasi sebenar melalui Masa Skrin, jurulatih AI, Live Activities dan penyegerakan iCloud. 10 bahasa termasuk Arab.",
        "nb": "Et seriøst produktivitetsverktøy. Pomodoro-sykluser, ekte appblokkering via Skjermtid, en AI-coach, Live Activities og iCloud-synkronisering. 10 språk, inkludert arabisk.",
        "nl": "Een serieuze productiviteitstool. Pomodoro-cycli, echte app-blokkering via Schermtijd, een AI-coach, Live Activities en iCloud-synchronisatie. 10 talen, waaronder Arabisch.",
        "pl": "Poważne narzędzie produktywności. Cykle Pomodoro, prawdziwe blokowanie aplikacji przez Czas przed ekranem, trener AI, Live Activities i synchronizacja iCloud. 10 języków, w tym arabski.",
        "pt": "Uma ferramenta de produtividade séria. Ciclos Pomodoro, bloqueio real de apps via Tempo de Uso, um coach de IA, Live Activities e sincronização com o iCloud. 10 idiomas, incluindo árabe.",
        "ru": "Серьёзный инструмент продуктивности. Циклы помодоро, настоящая блокировка приложений через Экранное время, ИИ-коуч, Live Activities и синхронизация iCloud. 10 языков, включая арабский.",
        "sv": "Ett seriöst produktivitetsverktyg. Pomodoro-cykler, riktig appblockering via Skärmtid, en AI-coach, Live Activities och iCloud-synkning. 10 språk, inklusive arabiska.",
        "th": "เครื่องมือเพิ่มประสิทธิภาพอย่างจริงจัง รอบ Pomodoro การบล็อกแอปจริงผ่าน Screen Time โค้ช AI, Live Activities และการซิงค์ iCloud รองรับ 10 ภาษารวมถึงภาษาอาหรับ",
        "tr": "Ciddi bir üretkenlik aracı. Pomodoro döngüleri, Ekran Süresi ile gerçek uygulama engelleme, yapay zekâ koçu, Live Activities ve iCloud eşitleme. Arapça dahil 10 dil.",
        "uk": "Серйозний інструмент продуктивності. Цикли помодоро, справжнє блокування застосунків через Екранний час, ШІ-коуч, Live Activities та синхронізація iCloud. 10 мов, зокрема арабська.",
        "ur": "ایک سنجیدہ پروڈکٹیویٹی ٹول۔ پومودورو سائیکلز، Screen Time کے ذریعے حقیقی ایپ بلاکنگ، AI کوچ، Live Activities اور iCloud سنک۔ عربی سمیت 10 زبانیں۔",
        "vi": "Một công cụ năng suất nghiêm túc. Chu kỳ Pomodoro, chặn ứng dụng thực sự qua Thời gian sử dụng, huấn luyện viên AI, Live Activities và đồng bộ iCloud. 10 ngôn ngữ, bao gồm tiếng Ả Rập.",
        "zh-Hans": "一款认真的效率工具。番茄钟循环、通过“屏幕使用时间”实现真正的应用屏蔽、AI 教练、实时活动和 iCloud 同步。支持包括阿拉伯语在内的 10 种语言。",
        "zh-Hant": "一款認真的生產力工具。番茄鐘循環、透過「螢幕使用時間」實現真正的 App 封鎖、AI 教練、即時動態和 iCloud 同步。支援包括阿拉伯語在內的 10 種語言。",
    },
    "copyright": {
        "en": "© 2025–2026 Ziyad Alsuhaymi. All rights reserved.",
        "ar": "© 2025–2026 زياد السحيمي. جميع الحقوق محفوظة.",
        "da": "© 2025–2026 Ziyad Alsuhaymi. Alle rettigheder forbeholdes.",
        "de": "© 2025–2026 Ziyad Alsuhaymi. Alle Rechte vorbehalten.",
        "es": "© 2025–2026 Ziyad Alsuhaymi. Todos los derechos reservados.",
        "fr": "© 2025–2026 Ziyad Alsuhaymi. Tous droits réservés.",
        "hi": "© 2025–2026 ज़ियाद अल्सुहैमी। सर्वाधिकार सुरक्षित।",
        "id": "© 2025–2026 Ziyad Alsuhaymi. Hak cipta dilindungi.",
        "it": "© 2025–2026 Ziyad Alsuhaymi. Tutti i diritti riservati.",
        "ja": "© 2025–2026 Ziyad Alsuhaymi. 無断複写・転載を禁じます。",
        "ko": "© 2025–2026 Ziyad Alsuhaymi. 모든 권리 보유.",
        "ms": "© 2025–2026 Ziyad Alsuhaymi. Hak cipta terpelihara.",
        "nb": "© 2025–2026 Ziyad Alsuhaymi. Alle rettigheter forbeholdt.",
        "nl": "© 2025–2026 Ziyad Alsuhaymi. Alle rechten voorbehouden.",
        "pl": "© 2025–2026 Ziyad Alsuhaymi. Wszelkie prawa zastrzeżone.",
        "pt": "© 2025–2026 Ziyad Alsuhaymi. Todos os direitos reservados.",
        "ru": "© 2025–2026 Зияд Альсухайми. Все права защищены.",
        "sv": "© 2025–2026 Ziyad Alsuhaymi. Alla rättigheter förbehållna.",
        "th": "© 2025–2026 Ziyad Alsuhaymi สงวนลิขสิทธิ์",
        "tr": "© 2025–2026 Ziyad Alsuhaymi. Tüm hakları saklıdır.",
        "uk": "© 2025–2026 Зіяд Альсухаймі. Усі права захищені.",
        "ur": "© 2025–2026 زیاد السحیمی۔ جملہ حقوق محفوظ ہیں۔",
        "vi": "© 2025–2026 Ziyad Alsuhaymi. Đã đăng ký bản quyền.",
        "zh-Hans": "© 2025–2026 Ziyad Alsuhaymi. 版权所有。",
        "zh-Hant": "© 2025–2026 Ziyad Alsuhaymi. 版權所有。",
    },
    "lang_label": {
        "en": "Language", "ar": "اللغة", "da": "Sprog", "de": "Sprache", "es": "Idioma",
        "fr": "Langue", "hi": "भाषा", "id": "Bahasa", "it": "Lingua", "ja": "言語",
        "ko": "언어", "ms": "Bahasa", "nb": "Språk", "nl": "Taal", "pl": "Język",
        "pt": "Idioma", "ru": "Язык", "sv": "Språk", "th": "ภาษา", "tr": "Dil",
        "uk": "Мова", "ur": "زبان", "vi": "Ngôn ngữ", "zh-Hans": "语言", "zh-Hant": "語言",
    },
}

# Merge hero/about/principles/contact translation keys from i18n_hero.py.
T.update(NEW_T)


def hreflang_block() -> str:
    """Build a hreflang <link> block listing every language version."""
    lines = []
    for code, _, _ in LANGUAGES:
        href = "https://ixsuper.github.io/" if code == "en" else f"https://ixsuper.github.io/{code}/"
        lines.append(f'    <link rel="alternate" hreflang="{code}" href="{href}">')
    lines.append('    <link rel="alternate" hreflang="x-default" href="https://ixsuper.github.io/">')
    return "\n".join(lines)


def language_switcher(current_code: str) -> str:
    """Build the language switcher <div> that sits in the header."""
    options = []
    for code, name, _ in LANGUAGES:
        href = "/" if code == "en" else f"/{code}/"
        selected = ' selected' if code == current_code else ''
        options.append(f'                <option value="{href}"{selected}>{name}</option>')
    label = T["lang_label"][current_code]
    return f'''        <div class="lang-switcher" aria-label="{label}">
            <svg viewBox="0 0 24 24" aria-hidden="true" class="lang-icon"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41C19.07 5.78 20 8.83 20 12c0 1.94-.48 3.75-1.3 5.39h-.8z"/></svg>
            <select onchange="window.location.href=this.value" aria-label="{label}">
{chr(10).join(options)}
            </select>
        </div>
'''


LANG_SWITCHER_CSS = '''
        /* ============ Language switcher ============ */
        .lang-switcher {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 100;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 14px 8px 12px;
            background: var(--card-bg, rgba(12, 16, 38, 0.55));
            border: 1px solid var(--border, rgba(255, 255, 255, 0.1));
            border-radius: 100px;
            backdrop-filter: blur(20px) saturate(140%);
            -webkit-backdrop-filter: blur(20px) saturate(140%);
            color: var(--text, #fff);
            font-size: 0.85em;
            font-weight: 500;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        .lang-switcher .lang-icon {
            width: 16px;
            height: 16px;
            fill: currentColor;
            opacity: 0.7;
        }
        .lang-switcher select {
            background: transparent;
            border: none;
            color: currentColor;
            font: inherit;
            cursor: pointer;
            outline: none;
            padding-right: 4px;
            appearance: none;
            -webkit-appearance: none;
            max-width: 140px;
        }
        .lang-switcher select option {
            background: #0a0e22;
            color: #fff;
        }
        html[dir="rtl"] .lang-switcher {
            right: auto;
            left: 20px;
        }
        @media (max-width: 500px) {
            .lang-switcher { top: 12px; right: 12px; padding: 6px 12px; font-size: 0.8em; }
            .lang-switcher select { max-width: 100px; }
            html[dir="rtl"] .lang-switcher { right: auto; left: 12px; }
        }
'''


# The exact English strings in the template we need to replace per language.
# Order matters because some substrings overlap.
REPLACEMENTS = [
    ("title_tag",            '<title>Ziyad Alsuhaymi — iOS Apps &amp; Games Developer</title>', lambda t: f'<title>{t["page_title"]}</title>'),
    ("title_tag_plain",      '<title>Ziyad Alsuhaymi — iOS Apps & Games Developer</title>',      lambda t: f'<title>{t["page_title"]}</title>'),
    ("meta_desc",            'content="Premium iOS apps and games by Ziyad Alsuhaymi. Echoes, Upcomin\', Block Blaster Puzzle, Tempo Focus, and Color Number Match."',
                             lambda t: f'content="{t["meta_description"]}"'),
    ("og_title1",            'content="Ziyad Alsuhaymi — iOS Apps &amp; Games Developer"',
                             lambda t: f'content="{t["page_title"]}"'),
    ("og_title2",            'content="Ziyad Alsuhaymi — iOS Apps & Games Developer"',
                             lambda t: f'content="{t["page_title"]}"'),
    # Badges
    ("badge_new",            '<span class="badge badge-live">New</span>',
                             lambda t: f'<span class="badge badge-live">{t["badge_new"]}</span>'),
    ("badge_soon",           '<span class="badge badge-soon">Coming Soon</span>',
                             lambda t: f'<span class="badge badge-soon">{t["badge_soon"]}</span>'),
    ("badge_live",           '<span class="badge badge-live">Live</span>',
                             lambda t: f'<span class="badge badge-live">{t["badge_live"]}</span>'),
    # Descriptions
    ("echoes_desc",          'Capture living memories with photo, ambient sound, weather, and location. Built for iOS 26 with Liquid Glass, on-device ML, and an immersive memory map. 14 languages.',
                             lambda t: t["echoes_desc"]),
    ("blocks_desc",          'A satisfying block puzzle game with explosive combos, sensory themes, and haptic feedback. 5 game modes, 50 adventure levels, 7 languages.',
                             lambda t: t["blocks_desc"]),
    ("cnm_desc",             'A vibrant puzzle game with 2000+ levels across 10 packs. Match tiles by color or number with special tiles, Metal shaders, haptic feedback, and 24 languages including Arabic RTL.',
                             lambda t: t["cnm_desc"]),
    ("upcomin_desc",         'Track every upcoming release — games, movies, TV, anime — in one beautifully bright iOS 26 app. Live Activities, Lock Screen widgets, Apple Intelligence guides, and a Global Launch Hub across 20 cities.',
                             lambda t: t["upcomin_desc"]),
    ("tempo_desc",           'A serious productivity tool. Pomodoro cycles, real app blocking via Screen Time, an AI coach, Live Activities, and iCloud sync. 10 languages including Arabic.',
                             lambda t: t["tempo_desc"]),
    # Buttons (Coming Soon appears twice as button text — use a unique pattern)
    ("btn_coming_soon",      '<button class="btn btn-soon" type="button" disabled>Coming Soon</button>',
                             lambda t: f'<button class="btn btn-soon" type="button" disabled>{t["btn_coming_soon"]}</button>'),
    # App Store CTA text
    ("btn_download",         'Download on the App Store',
                             lambda t: t["btn_download"]),
    # Info link labels
    ("link_learn_more",      '>Learn More</a>',
                             lambda t: f'>{t["link_learn_more"]}</a>'),
    ("link_privacy",         '>Privacy Policy</a>',
                             lambda t: f'>{t["link_privacy"]}</a>'),
    ("link_terms",           '>Terms of Use</a>',
                             lambda t: f'>{t["link_terms"]}</a>'),
    ("link_support",         '>Support</a>',
                             lambda t: f'>{t["link_support"]}</a>'),
    ("link_changelog",       '>Changelog</a>',
                             lambda t: f'>{t["link_changelog"]}</a>'),
    # Copyright
    ("copyright",            '<p class="copyright">© 2025–2026 Ziyad Alsuhaymi. All rights reserved.</p>',
                             lambda t: f'<p class="copyright">{t["copyright"]}</p>'),

    # ======================================================================
    # Hero / About / Principles / Contact — new sections added in redesign
    # ======================================================================

    # Hero eyebrow
    ("hero_eyebrow",         'Available for work · Saudi Arabia',
                             lambda t: t["hero_eyebrow"]),
    # Hero title (contains HTML spans — swap the entire <h1> body)
    ("hero_title_html",      '<h1 class="hero-title">Hi, I\'m <span class="hero-name">Ziyad</span>.<br>I build premium <span class="hero-grad">iOS apps</span>.</h1>',
                             lambda t: f'<h1 class="hero-title">{t["hero_title_html"]}</h1>'),
    # Hero bio paragraph
    ("hero_bio",             '<p class="hero-bio">Independent iOS developer building apps and games end-to-end. Three apps on the App Store, two more on the way, and a long list of small details I refuse to ship without.</p>',
                             lambda t: f'<p class="hero-bio">{t["hero_bio"]}</p>'),
    # Hero CTAs
    ("hero_cta_view",        'hero-btn-primary">\n                    View work\n                    <svg',
                             lambda t: f'hero-btn-primary">\n                    {t["hero_cta_view"]}\n                    <svg'),
    ("hero_cta_contact",     'hero-btn-ghost">Get in touch</a>',
                             lambda t: f'hero-btn-ghost">{t["hero_cta_contact"]}</a>'),

    # Hero stats (4 labels + 1 translated number "Solo")
    ("hero_stat_label_1",    '<span class="hero-stat-label">Live on App Store</span>',
                             lambda t: f'<span class="hero-stat-label">{t["hero_stat_label_1"]}</span>'),
    ("hero_stat_label_2",    '<span class="hero-stat-label">In development</span>',
                             lambda t: f'<span class="hero-stat-label">{t["hero_stat_label_2"]}</span>'),
    ("hero_stat_label_3",    '<span class="hero-stat-label">Puzzle levels</span>',
                             lambda t: f'<span class="hero-stat-label">{t["hero_stat_label_3"]}</span>'),
    ("hero_stat_label_4",    '<span class="hero-stat-label">Independent dev</span>',
                             lambda t: f'<span class="hero-stat-label">{t["hero_stat_label_4"]}</span>'),
    ("hero_stat_num_solo",   '<span class="hero-stat-num">Solo</span>',
                             lambda t: f'<span class="hero-stat-num">{t["hero_stat_num_solo"]}</span>'),

    # Featured Work section header
    ("work_eyebrow",         '<div class="section-eyebrow">Featured Work</div>',
                             lambda t: f'<div class="section-eyebrow">{t["work_eyebrow"]}</div>'),
    ("work_title",           '<h2 class="section-title">Five apps. One obsession with polish.</h2>',
                             lambda t: f'<h2 class="section-title">{t["work_title"]}</h2>'),

    # About section
    ("about_eyebrow",        '<div class="section-eyebrow">About</div>',
                             lambda t: f'<div class="section-eyebrow">{t["about_eyebrow"]}</div>'),
    ("about_title",          '<h2 class="section-title">A maker who sweats the details.</h2>',
                             lambda t: f'<h2 class="section-title">{t["about_title"]}</h2>'),
    ("about_p1_html",        "I'm Ziyad — a solo iOS developer based in Saudi Arabia. I design, build, and ship apps end-to-end. My first app, <strong>Color Number Match</strong>, is on the App Store today with 2,000+ levels and translations into 25 languages. Two more — <strong>Echoes</strong> and <strong>Block Blaster</strong> — are on the way.",
                             lambda t: t["about_p1_html"]),
    ("about_p2",             "What I care about is the small stuff: haptics that feel intentional, animations with a reason for being there, translations that read like a person wrote them. That's where I spend my time.",
                             lambda t: t["about_p2"]),

    # Principles section header
    ("principles_eyebrow",   '<div class="section-eyebrow">Principles</div>',
                             lambda t: f'<div class="section-eyebrow">{t["principles_eyebrow"]}</div>'),
    ("principles_title",     '<h2 class="section-title">How I work</h2>',
                             lambda t: f'<h2 class="section-title">{t["principles_title"]}</h2>'),

    # Principle 1
    ("principle_1_title",    '<h3>Solo by choice</h3>',
                             lambda t: f'<h3>{t["principle_1_title"]}</h3>'),
    ("principle_1_copy",     "One brain, one vision. It's slower than a team — and that's the point. Every decision stays intact from sketch to ship.",
                             lambda t: t["principle_1_copy"]),
    # Principle 2
    ("principle_2_title",    '<h3>Polish or wait</h3>',
                             lambda t: f'<h3>{t["principle_2_title"]}</h3>'),
    ("principle_2_copy",     "A screen isn't done until it feels right. If the haptics aren't there, it isn't shipping. Deadlines move; the bar doesn't.",
                             lambda t: t["principle_2_copy"]),
    # Principle 3
    ("principle_3_title",    '<h3>Localization, not translation</h3>',
                             lambda t: f'<h3>{t["principle_3_title"]}</h3>'),
    ("principle_3_copy",     "25 languages, proofread by humans. Arabic is the test case, never the afterthought — proper RTL, native typography, real context.",
                             lambda t: t["principle_3_copy"]),
    # Principle 4
    ("principle_4_title",    '<h3>Small surface, deep work</h3>',
                             lambda t: f'<h3>{t["principle_4_title"]}</h3>'),
    ("principle_4_copy",     "I'd rather you remember one interaction than count a hundred features. Fewer things, done with care, beats more things rushed.",
                             lambda t: t["principle_4_copy"]),

    # Contact section
    ("contact_title",        '<h2 class="contact-title">Let\'s build something.</h2>',
                             lambda t: f'<h2 class="contact-title">{t["contact_title"]}</h2>'),
    ("contact_sub",          '<p class="contact-sub">Open to freelance, collaborations, and quiet chats about indie iOS development. I read everything.</p>',
                             lambda t: f'<p class="contact-sub">{t["contact_sub"]}</p>'),
]

# For cross-page links we want to remain absolute (they already are: /echoes/ etc.)
# English stays at / -- translated pages link to the same absolute paths, so there's
# nothing path-specific to rewrite.


def build_translations_dict(code: str) -> dict:
    """Return a flat dict of all translated strings for the given language."""
    return {k: v.get(code, v["en"]) for k, v in T.items()}


def update_selected_option(html: str, code: str) -> str:
    """Update the <select> in the existing lang-switcher so the option matching
    this locale is marked selected. Called on every locale — the English source
    starts with value="/" selected, so we strip and reapply every run."""
    # Strip any existing selected attribute on options inside .lang-switcher
    html = re.sub(
        r'(<option value="[^"]+")\s+selected(\s*>)',
        r'\1\2',
        html,
    )
    # Add selected to the target option
    target_value = "/" if code == "en" else f"/{code}/"
    pattern = re.compile(r'(<option value="' + re.escape(target_value) + r'")(>)')
    html = pattern.sub(r'\1 selected\2', html, count=1)
    return html


def localize(src: str, code: str, direction: str) -> str:
    """Produce the localized HTML for a single language.

    The source index.html already contains the sticky topbar, baked-in
    hreflang block, language switcher markup, and inline CSS — this function
    only needs to swap text strings, update meta tags, and re-flag the
    correct <option> as selected."""
    t = build_translations_dict(code)
    html = src

    # 1) Set <html lang="..." dir="...">
    html = re.sub(r'<html\s+lang="[^"]*"[^>]*>', f'<html lang="{code}" dir="{direction}">', html, count=1)

    # 2) Set the canonical URL + og:url + og:locale to the localized page
    canonical = "https://ixsuper.github.io/" if code == "en" else f"https://ixsuper.github.io/{code}/"
    html = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{canonical}">', html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{canonical}">', html, count=1)
    html = re.sub(r'<meta property="og:locale" content="[^"]+">', f'<meta property="og:locale" content="{code}">', html, count=1)

    # 2b) Point app landing links (topbar + cards) at the localized copies.
    # Subpages (privacy/terms/support/changelog) only exist in English.
    if code != "en":
        for app in ("echoes", "block-blaster", "colornumbermatch", "tempo-focus"):
            html = html.replace(f'href="/{app}/"', f'href="/{code}/{app}/"')

    # 3) String replacements
    for _, needle, make_repl in REPLACEMENTS:
        replacement = make_repl(t)
        if needle in html:
            html = html.replace(needle, replacement)

    # 4) Update the lang-switcher <option selected>
    html = update_selected_option(html, code)

    return html


def main():
    if not os.path.exists(SRC):
        print(f"ERROR: source not found: {SRC}", file=sys.stderr)
        sys.exit(1)
    with open(SRC) as f:
        src = f.read()

    # The source file is the English root. Regenerate it with hreflang + switcher,
    # then write a localized copy for each other language.
    for code, _, direction in LANGUAGES:
        out_path = SRC if code == "en" else os.path.join(ROOT, code, "index.html")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        localized = localize(src, code, direction)
        with open(out_path, "w") as f:
            f.write(localized)
        print(f"  wrote {os.path.relpath(out_path, ROOT)}")

    print(f"\nGenerated {len(LANGUAGES)} localized pages.")


if __name__ == "__main__":
    main()
