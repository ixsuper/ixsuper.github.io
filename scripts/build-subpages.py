#!/usr/bin/env python3
"""
Build localized subpages for ixsuper.github.io.

Two jobs:

1. For the 3 app landing pages (echoes, block-blaster, colornumbermatch),
   generate a localized copy at /<lang>/<app>/index.html for each of the
   25 supported languages. Hero badge, tagline, CTA buttons, feature card
   titles, stat labels, and section headings are translated. Feature
   descriptions and longer body copy remain in English (for now).

2. For all OTHER subpages (changelog, support pages, privacy/terms),
   inject the language-switcher pill + hreflang declarations so users
   can jump from any page to a localized homepage. The subpages
   themselves stay English.

Run from site root AFTER scripts/build-locales.py:
    python3 scripts/build-subpages.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Reuse LANGUAGES, hreflang_block, language_switcher, LANG_SWITCHER_CSS
# by importing the sister module.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_locales import (  # noqa: E402
    LANGUAGES,
    T,
    hreflang_block,
    language_switcher,
    LANG_SWITCHER_CSS,
)


# -----------------------------------------------------------------------------
# App-specific translations.
# Each dict is { key: { lang: translation } }.
# -----------------------------------------------------------------------------

# Shared strings across landing pages (stat labels, common CTAs).
SHARED_T = {
    "stat_levels": {
        "en": "Levels", "ar": "مستويات", "da": "Baner", "de": "Level", "es": "Niveles",
        "fr": "Niveaux", "hi": "स्तर", "id": "Level", "it": "Livelli", "ja": "レベル",
        "ko": "레벨", "ms": "Tahap", "nb": "Brett", "nl": "Levels", "pl": "Poziomy",
        "pt": "Níveis", "ru": "Уровни", "sv": "Nivåer", "th": "ด่าน", "tr": "Seviye",
        "uk": "Рівні", "ur": "لیولز", "vi": "Màn", "zh-Hans": "关卡", "zh-Hant": "關卡",
    },
    "stat_packs": {
        "en": "Level Packs", "ar": "حزم المستويات", "da": "Banepakker", "de": "Level-Pakete",
        "es": "Paquetes", "fr": "Packs", "hi": "पैक", "id": "Paket Level", "it": "Pacchetti",
        "ja": "パック", "ko": "레벨 팩", "ms": "Pek Tahap", "nb": "Brettpakker", "nl": "Pakketten",
        "pl": "Paczki", "pt": "Pacotes", "ru": "Паки уровней", "sv": "Paket", "th": "แพ็ก",
        "tr": "Paketler", "uk": "Паки", "ur": "پیکس", "vi": "Gói", "zh-Hans": "关卡包",
        "zh-Hant": "關卡包",
    },
    "stat_languages": {
        "en": "Languages", "ar": "اللغات", "da": "Sprog", "de": "Sprachen", "es": "Idiomas",
        "fr": "Langues", "hi": "भाषाएँ", "id": "Bahasa", "it": "Lingue", "ja": "言語",
        "ko": "언어", "ms": "Bahasa", "nb": "Språk", "nl": "Talen", "pl": "Języki",
        "pt": "Idiomas", "ru": "Языки", "sv": "Språk", "th": "ภาษา", "tr": "Diller",
        "uk": "Мови", "ur": "زبانیں", "vi": "Ngôn ngữ", "zh-Hans": "语言", "zh-Hant": "語言",
    },
    "stat_achievements": {
        "en": "Achievements", "ar": "إنجازات", "da": "Bedrifter", "de": "Erfolge", "es": "Logros",
        "fr": "Succès", "hi": "उपलब्धियाँ", "id": "Pencapaian", "it": "Obiettivi", "ja": "実績",
        "ko": "업적", "ms": "Pencapaian", "nb": "Prestasjoner", "nl": "Prestaties", "pl": "Osiągnięcia",
        "pt": "Conquistas", "ru": "Достижения", "sv": "Prestationer", "th": "ความสำเร็จ",
        "tr": "Başarımlar", "uk": "Досягнення", "ur": "کامیابیاں", "vi": "Thành tích",
        "zh-Hans": "成就", "zh-Hant": "成就",
    },
    "stat_grid": {
        "en": "Grid Size", "ar": "حجم الشبكة", "da": "Gitterstørrelse", "de": "Rastergröße",
        "es": "Tamaño de cuadrícula", "fr": "Grille", "hi": "ग्रिड आकार", "id": "Ukuran Grid",
        "it": "Dimensioni griglia", "ja": "グリッドサイズ", "ko": "그리드 크기", "ms": "Saiz Grid",
        "nb": "Rutenett", "nl": "Rasterformaat", "pl": "Rozmiar siatki", "pt": "Tamanho da grade",
        "ru": "Размер сетки", "sv": "Rutnät", "th": "ขนาดกริด", "tr": "Izgara Boyutu",
        "uk": "Розмір сітки", "ur": "گرڈ سائز", "vi": "Kích thước lưới", "zh-Hans": "网格尺寸",
        "zh-Hant": "網格尺寸",
    },
    "stat_modes": {
        "en": "Game Modes", "ar": "أوضاع اللعب", "da": "Spiltilstande", "de": "Spielmodi",
        "es": "Modos de juego", "fr": "Modes de jeu", "hi": "गेम मोड", "id": "Mode Permainan",
        "it": "Modalità di gioco", "ja": "ゲームモード", "ko": "게임 모드", "ms": "Mod Permainan",
        "nb": "Spillmoduser", "nl": "Spelmodi", "pl": "Tryby gry", "pt": "Modos de jogo",
        "ru": "Режимы игры", "sv": "Spellägen", "th": "โหมดเกม", "tr": "Oyun Modları",
        "uk": "Режими гри", "ur": "گیم موڈز", "vi": "Chế độ chơi", "zh-Hans": "游戏模式",
        "zh-Hant": "遊戲模式",
    },
    "cta_learn_more": {
        "en": "Learn More", "ar": "اعرف المزيد", "da": "Læs mere", "de": "Mehr erfahren",
        "es": "Más información", "fr": "En savoir plus", "hi": "और जानें", "id": "Pelajari Lebih",
        "it": "Scopri di più", "ja": "詳細", "ko": "자세히 보기", "ms": "Ketahui Lagi",
        "nb": "Les mer", "nl": "Meer info", "pl": "Dowiedz się więcej", "pt": "Saiba mais",
        "ru": "Подробнее", "sv": "Läs mer", "th": "เรียนรู้เพิ่มเติม", "tr": "Daha Fazla",
        "uk": "Дізнатись більше", "ur": "مزید جانیں", "vi": "Tìm hiểu thêm", "zh-Hans": "了解更多",
        "zh-Hant": "了解更多",
    },
    "cta_coming_soon": {
        "en": "Coming Soon to the App Store", "ar": "قريبًا على App Store", "da": "Kommer snart på App Store",
        "de": "Bald im App Store", "es": "Próximamente en el App Store", "fr": "Bientôt sur l’App Store",
        "hi": "जल्द App Store पर", "id": "Segera di App Store", "it": "Prossimamente su App Store",
        "ja": "App Storeに近日登場", "ko": "App Store 출시 예정", "ms": "Akan Datang di App Store",
        "nb": "Kommer snart til App Store", "nl": "Binnenkort in de App Store",
        "pl": "Wkrótce w App Store", "pt": "Em breve na App Store", "ru": "Скоро в App Store",
        "sv": "Kommer snart till App Store", "th": "เร็ว ๆ นี้บน App Store",
        "tr": "Yakında App Store’da", "uk": "Незабаром у App Store", "ur": "App Store پر جلد",
        "vi": "Sắp ra mắt trên App Store", "zh-Hans": "即将登陆 App Store",
        "zh-Hant": "即將登陸 App Store",
    },
    "cta_release_notes": {
        "en": "Release Notes", "ar": "ملاحظات الإصدار", "da": "Udgivelsesnoter", "de": "Versionshinweise",
        "es": "Notas de la versión", "fr": "Notes de version", "hi": "रिलीज़ नोट्स",
        "id": "Catatan Rilis", "it": "Note di rilascio", "ja": "リリースノート",
        "ko": "릴리스 노트", "ms": "Nota Keluaran", "nb": "Utgivelsesnotater", "nl": "Release-opmerkingen",
        "pl": "Informacje o wydaniu", "pt": "Notas da versão", "ru": "Примечания к выпуску",
        "sv": "Utgåvenoteringar", "th": "บันทึกรุ่น", "tr": "Sürüm Notları",
        "uk": "Примітки до випуску", "ur": "ریلیز نوٹس", "vi": "Ghi chú phát hành",
        "zh-Hans": "版本说明", "zh-Hant": "版本說明",
    },
    "cta_download": {
        "en": "Download on the App Store", "ar": "حمّل من App Store", "da": "Hent på App Store",
        "de": "Im App Store laden", "es": "Descargar en el App Store", "fr": "Télécharger sur l’App Store",
        "hi": "App Store पर डाउनलोड करें", "id": "Unduh di App Store", "it": "Scarica dall’App Store",
        "ja": "App Storeからダウンロード", "ko": "App Store에서 다운로드", "ms": "Muat Turun di App Store",
        "nb": "Last ned fra App Store", "nl": "Downloaden in de App Store",
        "pl": "Pobierz z App Store", "pt": "Baixar na App Store", "ru": "Загрузить в App Store",
        "sv": "Ladda ner på App Store", "th": "ดาวน์โหลดบน App Store",
        "tr": "App Store’dan indir", "uk": "Завантажити в App Store", "ur": "App Store سے ڈاؤن لوڈ کریں",
        "vi": "Tải trên App Store", "zh-Hans": "在 App Store 下载",
        "zh-Hant": "在 App Store 下載",
    },
    "nav_support": {
        "en": "Support", "ar": "الدعم", "da": "Support", "de": "Support", "es": "Soporte",
        "fr": "Assistance", "hi": "सहायता", "id": "Dukungan", "it": "Supporto", "ja": "サポート",
        "ko": "지원", "ms": "Sokongan", "nb": "Support", "nl": "Ondersteuning", "pl": "Wsparcie",
        "pt": "Suporte", "ru": "Поддержка", "sv": "Support", "th": "ช่วยเหลือ", "tr": "Destek",
        "uk": "Підтримка", "ur": "سپورٹ", "vi": "Hỗ trợ", "zh-Hans": "支持", "zh-Hant": "支援",
    },
    "nav_changelog": {
        "en": "Changelog", "ar": "سجل التغييرات", "da": "Ændringslog", "de": "Änderungsprotokoll",
        "es": "Registro de cambios", "fr": "Journal des modifications", "hi": "चेंजलॉग",
        "id": "Log Perubahan", "it": "Registro modifiche", "ja": "変更履歴", "ko": "변경 내역",
        "ms": "Log Perubahan", "nb": "Endringslogg", "nl": "Changelog", "pl": "Dziennik zmian",
        "pt": "Registro de alterações", "ru": "История изменений", "sv": "Ändringslogg",
        "th": "บันทึกการเปลี่ยนแปลง", "tr": "Değişiklik Günlüğü", "uk": "Журнал змін",
        "ur": "چینج لاگ", "vi": "Nhật ký thay đổi", "zh-Hans": "更新日志", "zh-Hant": "更新日誌",
    },
}

# ---------- Echoes landing ----------
ECHOES_T = {
    "badge": {
        "en": "Coming Soon · iOS 26", "ar": "قريبًا · iOS 26", "da": "Kommer snart · iOS 26",
        "de": "Bald verfügbar · iOS 26", "es": "Próximamente · iOS 26", "fr": "Bientôt · iOS 26",
        "hi": "जल्द · iOS 26", "id": "Segera · iOS 26", "it": "Prossimamente · iOS 26",
        "ja": "近日公開 · iOS 26", "ko": "출시 예정 · iOS 26", "ms": "Akan Datang · iOS 26",
        "nb": "Kommer snart · iOS 26", "nl": "Binnenkort · iOS 26", "pl": "Wkrótce · iOS 26",
        "pt": "Em breve · iOS 26", "ru": "Скоро · iOS 26", "sv": "Kommer snart · iOS 26",
        "th": "เร็ว ๆ นี้ · iOS 26", "tr": "Yakında · iOS 26", "uk": "Незабаром · iOS 26",
        "ur": "جلد · iOS 26", "vi": "Sắp ra mắt · iOS 26", "zh-Hans": "即将推出 · iOS 26",
        "zh-Hant": "即將推出 · iOS 26",
    },
    "tagline": {
        "en": "Capture living memories that blend a photo, ambient sound, weather, and the exact place you were when it happened. Revisit them on an immersive map. Built natively for iOS 26.",
        "ar": "التقط ذكريات حية تمزج بين الصورة والصوت المحيط والطقس والمكان الدقيق الذي كنت فيه. استعرضها على خريطة غامرة. مصمم أصلاً لـ iOS 26.",
        "da": "Fang levende minder, der blander foto, omgivende lyd, vejr og stedet, du var, da det skete. Genoplev dem på et medrivende kort. Bygget til iOS 26.",
        "de": "Erfasse lebendige Erinnerungen, die Foto, Umgebungsgeräusche, Wetter und genauen Ort vereinen. Erlebe sie auf einer immersiven Karte. Nativ für iOS 26 gebaut.",
        "es": "Captura recuerdos vivos que combinan foto, sonido ambiente, clima y el lugar exacto donde estuviste. Revívelos en un mapa inmersivo. Nativo para iOS 26.",
        "fr": "Capturez des souvenirs vivants mêlant photo, son ambiant, météo et l’endroit exact où vous étiez. Revivez-les sur une carte immersive. Conçu pour iOS 26.",
        "hi": "जीवंत यादें कैद करें जो फोटो, परिवेश ध्वनि, मौसम और सटीक स्थान को एक साथ लाती हैं। एक इमर्सिव मानचित्र पर उन्हें फिर से जिएं। iOS 26 के लिए मूल रूप से निर्मित।",
        "id": "Tangkap kenangan hidup yang memadukan foto, suara sekitar, cuaca, dan tempat persis Anda berada. Kunjungi lagi di peta imersif. Dibuat untuk iOS 26.",
        "it": "Cattura ricordi vivi che uniscono foto, suono ambientale, meteo e luogo esatto. Rivivili su una mappa immersiva. Nativo per iOS 26.",
        "ja": "写真、環境音、天気、そして正確な場所を融合した生きた記憶をキャプチャ。没入感のあるマップで振り返ろう。iOS 26向けにネイティブ構築。",
        "ko": "사진, 주변 소리, 날씨, 정확한 장소를 결합한 생생한 기억을 포착하세요. 몰입감 있는 지도에서 다시 체험하세요. iOS 26용 네이티브 앱.",
        "ms": "Rakam kenangan hidup yang menggabungkan foto, bunyi persekitaran, cuaca dan tempat tepat anda berada. Lawati semula pada peta imersif. Dibina untuk iOS 26.",
        "nb": "Fang levende minner som blander foto, omgivelseslyd, vær og stedet du var. Besøk dem på et medrivende kart. Bygget for iOS 26.",
        "nl": "Leg levendige herinneringen vast met foto, omgevingsgeluid, weer en de exacte locatie. Beleef ze opnieuw op een meeslepende kaart. Gebouwd voor iOS 26.",
        "pl": "Uchwyć żywe wspomnienia łączące zdjęcie, dźwięk otoczenia, pogodę i dokładne miejsce. Wracaj do nich na immersyjnej mapie. Zbudowane dla iOS 26.",
        "pt": "Capture memórias vivas que unem foto, som ambiente, clima e o lugar exato. Reviva-as num mapa imersivo. Nativo para iOS 26.",
        "ru": "Запечатлевайте живые воспоминания, объединяющие фото, окружающий звук, погоду и точное место. Переживайте их на захватывающей карте. Нативно для iOS 26.",
        "sv": "Fånga levande minnen som förenar foto, omgivningsljud, väder och platsen du var. Återupplev dem på en medryckande karta. Byggd för iOS 26.",
        "th": "บันทึกความทรงจำที่มีชีวิตซึ่งผสานภาพถ่าย เสียงบรรยากาศ สภาพอากาศ และสถานที่ที่คุณอยู่ ย้อนดูบนแผนที่อันสมจริง สร้างสำหรับ iOS 26",
        "tr": "Fotoğraf, ortam sesi, hava durumu ve bulunduğun tam yeri birleştiren canlı anıları yakala. Sürükleyici bir haritada yeniden yaşa. iOS 26 için özel.",
        "uk": "Захоплюй живі спогади, що поєднують фото, навколишній звук, погоду й точне місце. Повертайся до них на захопливій карті. Нативно для iOS 26.",
        "ur": "جاندار یادیں محفوظ کریں جو تصویر، ماحول کی آواز، موسم اور صحیح مقام کو ملاتی ہیں۔ ایک حسی نقشے پر انہیں دوبارہ جئیں۔ iOS 26 کے لیے بنایا گیا۔",
        "vi": "Ghi lại ký ức sống động kết hợp ảnh, âm thanh môi trường, thời tiết và đúng nơi bạn đã ở. Xem lại trên bản đồ đắm chìm. Xây dựng cho iOS 26.",
        "zh-Hans": "捕捉融合照片、环境声、天气与准确地点的鲜活回忆，在沉浸式地图上再次体验。专为 iOS 26 原生打造。",
        "zh-Hant": "捕捉融合照片、環境聲、天氣與確切地點的鮮活回憶，在沉浸式地圖上再次體驗。專為 iOS 26 原生打造。",
    },
    "feat1": {  # Living Memories
        "en": "Living Memories", "ar": "ذكريات حية", "da": "Levende minder", "de": "Lebendige Erinnerungen",
        "es": "Recuerdos vivos", "fr": "Souvenirs vivants", "hi": "जीवंत यादें", "id": "Kenangan Hidup",
        "it": "Ricordi vivi", "ja": "生きた記憶", "ko": "살아있는 기억", "ms": "Kenangan Hidup",
        "nb": "Levende minner", "nl": "Levendige herinneringen", "pl": "Żywe wspomnienia",
        "pt": "Memórias vivas", "ru": "Живые воспоминания", "sv": "Levande minnen",
        "th": "ความทรงจำที่มีชีวิต", "tr": "Canlı Anılar", "uk": "Живі спогади",
        "ur": "جاندار یادیں", "vi": "Ký ức sống động", "zh-Hans": "鲜活回忆", "zh-Hant": "鮮活回憶",
    },
    "feat2": {  # Memory Map
        "en": "Memory Map", "ar": "خريطة الذكريات", "da": "Mindekort", "de": "Erinnerungskarte",
        "es": "Mapa de recuerdos", "fr": "Carte des souvenirs", "hi": "स्मृति मानचित्र",
        "id": "Peta Kenangan", "it": "Mappa dei ricordi", "ja": "メモリーマップ", "ko": "기억 지도",
        "ms": "Peta Kenangan", "nb": "Minnekart", "nl": "Herinneringskaart", "pl": "Mapa wspomnień",
        "pt": "Mapa de memórias", "ru": "Карта воспоминаний", "sv": "Minneskarta",
        "th": "แผนที่ความทรงจำ", "tr": "Anı Haritası", "uk": "Карта спогадів",
        "ur": "یادوں کا نقشہ", "vi": "Bản đồ ký ức", "zh-Hans": "记忆地图", "zh-Hant": "記憶地圖",
    },
    "feat3": {  # On-Device ML
        "en": "On-Device ML", "ar": "تعلّم آلي على الجهاز", "da": "ML på enheden",
        "de": "ML auf dem Gerät", "es": "ML en el dispositivo", "fr": "ML sur l’appareil",
        "hi": "ऑन-डिवाइस ML", "id": "ML di Perangkat", "it": "ML sul dispositivo",
        "ja": "オンデバイスML", "ko": "온디바이스 ML", "ms": "ML pada Peranti",
        "nb": "ML på enheten", "nl": "ML op het apparaat", "pl": "ML na urządzeniu",
        "pt": "ML no dispositivo", "ru": "ML на устройстве", "sv": "ML på enheten",
        "th": "ML บนอุปกรณ์", "tr": "Cihazda ML", "uk": "ML на пристрої",
        "ur": "ڈیوائس پر ML", "vi": "ML trên thiết bị", "zh-Hans": "本机机器学习",
        "zh-Hant": "本機機器學習",
    },
    "feat4": {  # Liquid Glass UI
        "en": "Liquid Glass UI", "ar": "واجهة Liquid Glass", "da": "Liquid Glass UI",
        "de": "Liquid Glass UI", "es": "Interfaz Liquid Glass", "fr": "Interface Liquid Glass",
        "hi": "Liquid Glass UI", "id": "UI Liquid Glass", "it": "Interfaccia Liquid Glass",
        "ja": "Liquid Glass UI", "ko": "Liquid Glass UI", "ms": "UI Liquid Glass",
        "nb": "Liquid Glass UI", "nl": "Liquid Glass-UI", "pl": "Interfejs Liquid Glass",
        "pt": "Interface Liquid Glass", "ru": "Интерфейс Liquid Glass", "sv": "Liquid Glass-UI",
        "th": "UI Liquid Glass", "tr": "Liquid Glass Arayüzü", "uk": "Інтерфейс Liquid Glass",
        "ur": "Liquid Glass انٹرفیس", "vi": "Giao diện Liquid Glass", "zh-Hans": "Liquid Glass 界面",
        "zh-Hant": "Liquid Glass 介面",
    },
    "feat5": {  # Ambient Audio
        "en": "Ambient Audio", "ar": "صوت محيط", "da": "Omgivende lyd", "de": "Umgebungsaudio",
        "es": "Audio ambiente", "fr": "Audio ambiant", "hi": "परिवेश ऑडियो", "id": "Audio Sekitar",
        "it": "Audio ambientale", "ja": "環境音", "ko": "주변 오디오", "ms": "Audio Persekitaran",
        "nb": "Omgivelseslyd", "nl": "Omgevingsaudio", "pl": "Dźwięk otoczenia",
        "pt": "Áudio ambiente", "ru": "Окружающий звук", "sv": "Omgivningsljud",
        "th": "เสียงแวดล้อม", "tr": "Ortam Sesi", "uk": "Навколишній звук",
        "ur": "ماحولیاتی آڈیو", "vi": "Âm thanh môi trường", "zh-Hans": "环境音频", "zh-Hant": "環境音訊",
    },
    "feat6": {  # 11 Languages
        "en": "11 Languages", "ar": "11 لغة", "da": "11 sprog", "de": "11 Sprachen",
        "es": "11 idiomas", "fr": "11 langues", "hi": "11 भाषाएँ", "id": "11 Bahasa",
        "it": "11 lingue", "ja": "11言語", "ko": "11개 언어", "ms": "11 Bahasa",
        "nb": "11 språk", "nl": "11 talen", "pl": "11 języków", "pt": "11 idiomas",
        "ru": "11 языков", "sv": "11 språk", "th": "11 ภาษา", "tr": "11 dil",
        "uk": "11 мов", "ur": "11 زبانیں", "vi": "11 ngôn ngữ", "zh-Hans": "11 种语言",
        "zh-Hant": "11 種語言",
    },
    "section_heading": {
        "en": "Built on Apple’s Latest", "ar": "مبني على أحدث تقنيات Apple", "da": "Bygget på Apples nyeste",
        "de": "Auf Apples Neuestem gebaut", "es": "Basado en lo último de Apple",
        "fr": "Conçu sur les dernières technologies d’Apple", "hi": "Apple की नवीनतम पर निर्मित",
        "id": "Dibangun di atas yang Terbaru dari Apple", "it": "Costruito sulle ultime tecnologie Apple",
        "ja": "Appleの最新技術で構築", "ko": "Apple의 최신 기술 기반", "ms": "Dibina atas Teknologi Apple Terkini",
        "nb": "Bygget på Apples nyeste", "nl": "Gebouwd op Apples nieuwste",
        "pl": "Zbudowane na najnowszej technologii Apple", "pt": "Construído sobre o mais recente da Apple",
        "ru": "Построено на новейших технологиях Apple", "sv": "Byggd på Apples senaste",
        "th": "สร้างบนเทคโนโลยี Apple ล่าสุด", "tr": "Apple’ın En Yenisi Üzerine İnşa",
        "uk": "Створено на найновіших технологіях Apple", "ur": "Apple کی جدید ترین ٹیکنالوجی پر تعمیر",
        "vi": "Xây dựng trên công nghệ Apple mới nhất", "zh-Hans": "基于 Apple 最新技术打造",
        "zh-Hant": "基於 Apple 最新技術打造",
    },
}

# ---------- Block Blaster landing ----------
BLOCKS_T = {
    "badge": {
        "en": "Coming Soon", "ar": "قريبًا", "da": "Kommer snart", "de": "Bald verfügbar",
        "es": "Próximamente", "fr": "Bientôt", "hi": "जल्द आ रहा है", "id": "Segera Hadir",
        "it": "Prossimamente", "ja": "近日公開", "ko": "출시 예정", "ms": "Akan Datang",
        "nb": "Kommer snart", "nl": "Binnenkort", "pl": "Wkrótce", "pt": "Em breve",
        "ru": "Скоро", "sv": "Kommer snart", "th": "เร็ว ๆ นี้", "tr": "Yakında",
        "uk": "Незабаром", "ur": "جلد آرہا ہے", "vi": "Sắp ra mắt", "zh-Hans": "即将推出",
        "zh-Hant": "即將推出",
    },
    "tagline": {
        "en": "A satisfying block puzzle game with explosive combos, beautiful sensory themes, and haptic feedback that makes every line clear feel incredible.",
        "ar": "لعبة ألغاز بلوكات ممتعة مع كومبو انفجاري وسمات حسية جميلة وردود فعل لمسية تجعل كل إزالة خط تبدو مذهلة.",
        "da": "Et tilfredsstillende blokpuslespil med eksplosive combos, smukke sensoriske temaer og haptisk feedback, der gør hver linje ryddet utrolig.",
        "de": "Ein befriedigendes Blockpuzzle mit explosiven Combos, schönen sensorischen Themes und haptischem Feedback, das jede gelöschte Linie fantastisch macht.",
        "es": "Un satisfactorio juego de bloques con combos explosivos, hermosos temas sensoriales y retroalimentación háptica que hace que cada línea despejada se sienta increíble.",
        "fr": "Un jeu de blocs satisfaisant avec des combos explosifs, de beaux thèmes sensoriels et un retour haptique qui rend chaque ligne effacée incroyable.",
        "hi": "संतोषजनक ब्लॉक पज़ल गेम, विस्फोटक कॉम्बो, सुंदर संवेदी थीम और हैप्टिक फीडबैक के साथ जो हर लाइन क्लियर को अविश्वसनीय बनाता है।",
        "id": "Gim teka-teki blok yang memuaskan dengan kombo eksplosif, tema sensorik yang indah, dan umpan balik haptik yang membuat setiap garis yang dibersihkan terasa luar biasa.",
        "it": "Un soddisfacente gioco di blocchi con combo esplosive, bellissimi temi sensoriali e feedback aptico che rende ogni linea cancellata incredibile.",
        "ja": "爆発的なコンボ、美しい感覚テーマ、そしてあらゆるライン消去を素晴らしく感じさせるハプティックフィードバックを備えた満足のいくブロックパズル。",
        "ko": "폭발적인 콤보, 아름다운 감각적 테마, 그리고 모든 라인 제거를 놀랍게 만드는 햅틱 피드백을 갖춘 만족스러운 블록 퍼즐 게임.",
        "ms": "Permainan teka-teki blok yang memuaskan dengan kombo letupan, tema deria yang indah dan maklum balas haptik yang menjadikan setiap baris dikosongkan terasa hebat.",
        "nb": "Et tilfredsstillende blokkpuslespill med eksplosive combos, vakre sanselige temaer og haptisk tilbakemelding som gjør hver linje ryddet utrolig.",
        "nl": "Een bevredigend blokkenpuzzelspel met explosieve combo’s, prachtige zintuiglijke thema’s en haptische feedback die elke gewiste lijn ongelooflijk maakt.",
        "pl": "Satysfakcjonująca gra logiczna z wybuchowymi kombinacjami, pięknymi zmysłowymi motywami i wibracjami, które sprawiają, że każda wyczyszczona linia jest niesamowita.",
        "pt": "Um jogo de blocos satisfatório com combos explosivos, belos temas sensoriais e feedback háptico que torna cada linha limpa incrível.",
        "ru": "Увлекательная головоломка с блоками, взрывными комбо, красивыми сенсорными темами и тактильной отдачей, которая делает каждую очищенную линию невероятной.",
        "sv": "Ett tillfredsställande blockpussel med explosiva combos, vackra sensoriska teman och haptisk feedback som gör varje rensad linje otrolig.",
        "th": "เกมปริศนาบล็อกที่น่าพึงพอใจพร้อมคอมโบระเบิด ธีมสัมผัสที่สวยงาม และระบบสัมผัสที่ทำให้ทุกเส้นที่เคลียร์รู้สึกน่าทึ่ง",
        "tr": "Patlayıcı kombolar, güzel duyusal temalar ve her silinen satırı harika hissettiren haptik geri bildirimle tatmin edici bir blok bulmaca oyunu.",
        "uk": "Приємна гра-головоломка з блоками, вибуховими комбо, красивими сенсорними темами та тактильним відгуком, який робить кожну очищену лінію неймовірною.",
        "ur": "ایک تسلی بخش بلاک پزل گیم جس میں دھماکہ خیز کومبوز، خوبصورت حسی تھیمز اور ہیپٹک فیڈبیک ہے جو ہر لائن کلیئر کو حیرت انگیز بناتا ہے۔",
        "vi": "Trò chơi xếp khối thỏa mãn với combo bùng nổ, chủ đề cảm giác đẹp mắt và phản hồi rung khiến mỗi lần xóa hàng trở nên tuyệt vời.",
        "zh-Hans": "一款令人满足的方块消除游戏，拥有爆炸性连击、美丽的感官主题和触觉反馈，让每一行消除都感觉不可思议。",
        "zh-Hant": "一款令人滿足的方塊消除遊戲，擁有爆炸性連擊、美麗的感官主題和觸覺回饋，讓每一行消除都感覺不可思議。",
    },
    "feat1": {  # Explosive Combos
        "en": "Explosive Combos", "ar": "كومبوز انفجارية", "da": "Eksplosive combos",
        "de": "Explosive Combos", "es": "Combos explosivos", "fr": "Combos explosifs",
        "hi": "विस्फोटक कॉम्बो", "id": "Kombo Eksplosif", "it": "Combo esplosive",
        "ja": "爆発的なコンボ", "ko": "폭발적인 콤보", "ms": "Kombo Letupan",
        "nb": "Eksplosive combos", "nl": "Explosieve combo’s", "pl": "Wybuchowe kombinacje",
        "pt": "Combos explosivos", "ru": "Взрывные комбо", "sv": "Explosiva combos",
        "th": "คอมโบระเบิด", "tr": "Patlayıcı Kombolar", "uk": "Вибухові комбо",
        "ur": "دھماکہ خیز کومبوز", "vi": "Combo bùng nổ", "zh-Hans": "爆炸连击", "zh-Hant": "爆炸連擊",
    },
    "feat2": {  # Sensory Packs
        "en": "Sensory Packs", "ar": "حزم حسية", "da": "Sansepakker", "de": "Sensorik-Pakete",
        "es": "Paquetes sensoriales", "fr": "Packs sensoriels", "hi": "संवेदी पैक",
        "id": "Paket Sensorik", "it": "Pacchetti sensoriali", "ja": "感覚パック",
        "ko": "감각 팩", "ms": "Pek Deria", "nb": "Sansepakker", "nl": "Zintuiglijke pakketten",
        "pl": "Pakiety zmysłowe", "pt": "Pacotes sensoriais", "ru": "Сенсорные паки",
        "sv": "Sensoriska paket", "th": "ชุดสัมผัส", "tr": "Duyusal Paketler",
        "uk": "Сенсорні паки", "ur": "حسی پیکس", "vi": "Gói cảm giác", "zh-Hans": "感官主题包",
        "zh-Hant": "感官主題包",
    },
    "feat3": {  # Power-Ups
        "en": "Power-Ups", "ar": "معززات", "da": "Power-ups", "de": "Power-Ups",
        "es": "Potenciadores", "fr": "Bonus", "hi": "पावर-अप", "id": "Power-Up",
        "it": "Potenziamenti", "ja": "パワーアップ", "ko": "파워업", "ms": "Kuasa Khas",
        "nb": "Power-ups", "nl": "Power-ups", "pl": "Ulepszenia", "pt": "Melhorias",
        "ru": "Усиления", "sv": "Power-ups", "th": "พาวเวอร์อัป", "tr": "Güçlendirmeler",
        "uk": "Підсилення", "ur": "پاور اپس", "vi": "Tăng cường", "zh-Hans": "增益道具",
        "zh-Hant": "增益道具",
    },
    "feat4": {  # CoreHaptics
        "en": "CoreHaptics", "ar": "CoreHaptics", "da": "CoreHaptics", "de": "CoreHaptics",
        "es": "CoreHaptics", "fr": "CoreHaptics", "hi": "CoreHaptics", "id": "CoreHaptics",
        "it": "CoreHaptics", "ja": "CoreHaptics", "ko": "CoreHaptics", "ms": "CoreHaptics",
        "nb": "CoreHaptics", "nl": "CoreHaptics", "pl": "CoreHaptics", "pt": "CoreHaptics",
        "ru": "CoreHaptics", "sv": "CoreHaptics", "th": "CoreHaptics", "tr": "CoreHaptics",
        "uk": "CoreHaptics", "ur": "CoreHaptics", "vi": "CoreHaptics", "zh-Hans": "CoreHaptics",
        "zh-Hant": "CoreHaptics",
    },
    "feat5": {  # Metal Shaders
        "en": "Metal Shaders", "ar": "تأثيرات Metal", "da": "Metal-shaders", "de": "Metal-Shader",
        "es": "Shaders Metal", "fr": "Shaders Metal", "hi": "Metal शेडर्स", "id": "Shader Metal",
        "it": "Shader Metal", "ja": "Metalシェーダー", "ko": "Metal 셰이더", "ms": "Shader Metal",
        "nb": "Metal-shadere", "nl": "Metal-shaders", "pl": "Shadery Metal", "pt": "Shaders Metal",
        "ru": "Metal-шейдеры", "sv": "Metal-shaders", "th": "Metal Shaders", "tr": "Metal Shader’ları",
        "uk": "Шейдери Metal", "ur": "Metal شیڈرز", "vi": "Shader Metal", "zh-Hans": "Metal 着色器",
        "zh-Hant": "Metal 著色器",
    },
    "feat6": {  # 7 Languages
        "en": "7 Languages", "ar": "7 لغات", "da": "7 sprog", "de": "7 Sprachen",
        "es": "7 idiomas", "fr": "7 langues", "hi": "7 भाषाएँ", "id": "7 Bahasa",
        "it": "7 lingue", "ja": "7言語", "ko": "7개 언어", "ms": "7 Bahasa",
        "nb": "7 språk", "nl": "7 talen", "pl": "7 języków", "pt": "7 idiomas",
        "ru": "7 языков", "sv": "7 språk", "th": "7 ภาษา", "tr": "7 dil",
        "uk": "7 мов", "ur": "7 زبانیں", "vi": "7 ngôn ngữ", "zh-Hans": "7 种语言",
        "zh-Hant": "7 種語言",
    },
    "section_heading": {
        "en": "Five Ways to Play", "ar": "خمس طرق للعب", "da": "Fem måder at spille på",
        "de": "Fünf Arten zu spielen", "es": "Cinco formas de jugar", "fr": "Cinq façons de jouer",
        "hi": "खेलने के पाँच तरीके", "id": "Lima Cara Bermain", "it": "Cinque modi di giocare",
        "ja": "5つのプレイスタイル", "ko": "다섯 가지 플레이 방식", "ms": "Lima Cara Bermain",
        "nb": "Fem måter å spille på", "nl": "Vijf manieren om te spelen",
        "pl": "Pięć sposobów gry", "pt": "Cinco maneiras de jogar", "ru": "Пять способов играть",
        "sv": "Fem sätt att spela", "th": "ห้าวิธีเล่น", "tr": "Beş Oynama Yolu",
        "uk": "П’ять способів гри", "ur": "کھیلنے کے پانچ طریقے", "vi": "Năm cách chơi",
        "zh-Hans": "五种玩法", "zh-Hant": "五種玩法",
    },
}

# ---------- Color Number Match landing ----------
CNM_T = {
    "badge": {
        "en": "v1.2 · Live on the App Store", "ar": "v1.2 · متوفر على App Store",
        "da": "v1.2 · Live på App Store", "de": "v1.2 · Live im App Store",
        "es": "v1.2 · Disponible en el App Store", "fr": "v1.2 · Disponible sur l’App Store",
        "hi": "v1.2 · App Store पर उपलब्ध", "id": "v1.2 · Tersedia di App Store",
        "it": "v1.2 · Disponibile su App Store", "ja": "v1.2 · App Storeで配信中",
        "ko": "v1.2 · App Store 출시", "ms": "v1.2 · Tersedia di App Store",
        "nb": "v1.2 · Tilgjengelig på App Store", "nl": "v1.2 · Beschikbaar in de App Store",
        "pl": "v1.2 · Dostępne w App Store", "pt": "v1.2 · Disponível na App Store",
        "ru": "v1.2 · Доступно в App Store", "sv": "v1.2 · Tillgänglig på App Store",
        "th": "v1.2 · ใน App Store แล้ว", "tr": "v1.2 · App Store’da",
        "uk": "v1.2 · Доступно в App Store", "ur": "v1.2 · App Store پر دستیاب",
        "vi": "v1.2 · Đã có trên App Store", "zh-Hans": "v1.2 · App Store 现已上架",
        "zh-Hant": "v1.2 · App Store 現已上架",
    },
    "tagline": {
        "en": "A vibrant puzzle game where you match tiles by color, number, or both. 2000+ levels, special tiles, Metal shader effects, CoreHaptics, and full localization for 24 languages including Arabic RTL.",
        "ar": "لعبة ألغاز نابضة بالحياة تطابق فيها البلاطات باللون أو الرقم أو كليهما. أكثر من 2000 مستوى وبلاطات خاصة وتأثيرات Metal وCoreHaptics وتعريب كامل لـ 24 لغة تشمل العربية من اليمين لليسار.",
        "da": "Et livligt puslespil, hvor du matcher fliser efter farve, tal eller begge. 2000+ baner, specielle fliser, Metal shader-effekter, CoreHaptics og fuld lokalisering til 24 sprog inklusive arabisk RTL.",
        "de": "Ein lebendiges Puzzlespiel, bei dem du Kacheln nach Farbe, Zahl oder beidem verbindest. Über 2000 Level, Spezialkacheln, Metal-Shader, CoreHaptics und volle Lokalisierung in 24 Sprachen inklusive arabisch RTL.",
        "es": "Un vibrante juego de puzles donde emparejas fichas por color, número o ambos. Más de 2000 niveles, fichas especiales, shaders Metal, CoreHaptics y localización completa a 24 idiomas incluyendo árabe RTL.",
        "fr": "Un jeu de puzzle vibrant où vous associez les tuiles par couleur, numéro ou les deux. Plus de 2000 niveaux, tuiles spéciales, shaders Metal, CoreHaptics et localisation complète en 24 langues dont l’arabe RTL.",
        "hi": "एक जीवंत पज़ल गेम जहाँ आप रंग, संख्या, या दोनों से टाइलें मिलाते हैं। 2000+ स्तर, विशेष टाइलें, Metal शेडर प्रभाव, CoreHaptics और अरबी RTL सहित 24 भाषाओं में पूर्ण स्थानीयकरण।",
        "id": "Gim teka-teki hidup di mana Anda mencocokkan ubin berdasarkan warna, angka, atau keduanya. 2000+ level, ubin spesial, efek shader Metal, CoreHaptics, dan lokalisasi lengkap untuk 24 bahasa termasuk Arab RTL.",
        "it": "Un vivace gioco di puzzle dove abbini le tessere per colore, numero o entrambi. Oltre 2000 livelli, tessere speciali, effetti shader Metal, CoreHaptics e localizzazione completa in 24 lingue incluso l’arabo RTL.",
        "ja": "色、数字、またはその両方でタイルをマッチさせる色鮮やかなパズルゲーム。2000以上のレベル、特殊タイル、Metalシェーダー、CoreHapticsに加え、アラビア語RTLを含む24言語に完全対応。",
        "ko": "색상, 숫자, 또는 둘 다로 타일을 맞추는 화려한 퍼즐 게임. 2000개 이상의 레벨, 특수 타일, Metal 셰이더 효과, CoreHaptics, 아랍어 RTL 포함 24개 언어 완전 지원.",
        "ms": "Permainan teka-teki bertenaga di mana anda memadankan jubin mengikut warna, nombor, atau kedua-duanya. 2000+ tahap, jubin istimewa, kesan shader Metal, CoreHaptics dan penyetempatan penuh untuk 24 bahasa termasuk Arab RTL.",
        "nb": "Et livlig puslespill der du matcher brikker etter farge, tall eller begge. Over 2000 brett, spesialbrikker, Metal-shader-effekter, CoreHaptics og full lokalisering til 24 språk inkludert arabisk RTL.",
        "nl": "Een levendig puzzelspel waarin je tegels koppelt op kleur, nummer of beide. 2000+ levels, speciale tegels, Metal-shader-effecten, CoreHaptics en volledige lokalisatie voor 24 talen inclusief Arabisch RTL.",
        "pl": "Żywiołowa gra logiczna, w której dopasowujesz kafelki według koloru, liczby lub obu. Ponad 2000 poziomów, specjalne kafelki, efekty shaderów Metal, CoreHaptics i pełna lokalizacja w 24 językach włącznie z arabskim RTL.",
        "pt": "Um vibrante jogo de puzzle onde você combina peças por cor, número ou ambos. Mais de 2000 níveis, peças especiais, efeitos de shader Metal, CoreHaptics e localização completa em 24 idiomas incluindo árabe RTL.",
        "ru": "Яркая головоломка, где вы соединяете плитки по цвету, числу или обоим. Более 2000 уровней, особые плитки, эффекты Metal-шейдеров, CoreHaptics и полная локализация на 24 языка, включая арабский RTL.",
        "sv": "Ett livfullt pusselspel där du matchar brickor efter färg, nummer eller båda. 2000+ banor, specialbrickor, Metal shader-effekter, CoreHaptics och full lokalisering till 24 språk inklusive arabiska RTL.",
        "th": "เกมปริศนาสีสันสดใสที่คุณจับคู่ไทล์ตามสี หมายเลข หรือทั้งสอง 2000+ ด่าน ไทล์พิเศษ เอฟเฟกต์ Metal shader, CoreHaptics และรองรับเต็มรูปแบบ 24 ภาษารวมถึงอาหรับ RTL",
        "tr": "Karoları renge, sayıya veya her ikisine göre eşleştirdiğiniz canlı bir bulmaca oyunu. 2000’den fazla seviye, özel karolar, Metal shader efektleri, CoreHaptics ve Arapça RTL dahil 24 dil için tam yerelleştirme.",
        "uk": "Яскрава головоломка, де ви поєднуєте плитки за кольором, числом або обома. Понад 2000 рівнів, особливі плитки, ефекти шейдерів Metal, CoreHaptics та повна локалізація 24 мовами, включаючи арабську RTL.",
        "ur": "ایک متحرک پزل گیم جہاں آپ رنگ، نمبر یا دونوں کے ذریعے ٹائلز ملاتے ہیں۔ 2000+ لیولز، خصوصی ٹائلز، Metal شیڈر ایفیکٹس، CoreHaptics اور عربی RTL سمیت 24 زبانوں میں مکمل لوکلائزیشن۔",
        "vi": "Trò chơi giải đố sống động nơi bạn ghép ô theo màu, số, hoặc cả hai. 2000+ màn chơi, ô đặc biệt, hiệu ứng shader Metal, CoreHaptics và bản địa hóa đầy đủ cho 24 ngôn ngữ bao gồm tiếng Ả Rập RTL.",
        "zh-Hans": "一款绚丽的益智游戏，按颜色、数字或两者匹配方块。2000+ 关卡、特殊方块、Metal 着色器特效、CoreHaptics，并完整本地化为 24 种语言（含阿拉伯语 RTL）。",
        "zh-Hant": "一款絢麗的益智遊戲，依顏色、數字或兩者匹配方塊。2000+ 關卡、特殊方塊、Metal 著色器特效、CoreHaptics，並完整本地化為 24 種語言（含阿拉伯文 RTL）。",
    },
    "feat1": {  # 2000+ Levels
        "en": "2000+ Levels", "ar": "+2000 مستوى", "da": "2000+ baner", "de": "2000+ Level",
        "es": "Más de 2000 niveles", "fr": "2000+ niveaux", "hi": "2000+ स्तर",
        "id": "2000+ Level", "it": "Oltre 2000 livelli", "ja": "2000以上のレベル",
        "ko": "2000개 이상 레벨", "ms": "2000+ Tahap", "nb": "2000+ brett", "nl": "2000+ levels",
        "pl": "Ponad 2000 poziomów", "pt": "Mais de 2000 níveis", "ru": "Более 2000 уровней",
        "sv": "2000+ banor", "th": "กว่า 2000 ด่าน", "tr": "2000’den fazla seviye",
        "uk": "Понад 2000 рівнів", "ur": "2000+ لیولز", "vi": "2000+ màn", "zh-Hans": "2000+ 关卡",
        "zh-Hant": "2000+ 關卡",
    },
    "feat2": {  # Special Tiles
        "en": "Special Tiles", "ar": "بلاطات خاصة", "da": "Specielle fliser", "de": "Spezialkacheln",
        "es": "Fichas especiales", "fr": "Tuiles spéciales", "hi": "विशेष टाइलें",
        "id": "Ubin Spesial", "it": "Tessere speciali", "ja": "特殊タイル", "ko": "특수 타일",
        "ms": "Jubin Istimewa", "nb": "Spesialbrikker", "nl": "Speciale tegels",
        "pl": "Specjalne kafelki", "pt": "Peças especiais", "ru": "Особые плитки",
        "sv": "Specialbrickor", "th": "ไทล์พิเศษ", "tr": "Özel Karolar", "uk": "Особливі плитки",
        "ur": "خصوصی ٹائلز", "vi": "Ô đặc biệt", "zh-Hans": "特殊方块", "zh-Hant": "特殊方塊",
    },
    "feat3": {  # Metal Shaders
        "en": "Metal Shaders", "ar": "تأثيرات Metal", "da": "Metal-shaders", "de": "Metal-Shader",
        "es": "Shaders Metal", "fr": "Shaders Metal", "hi": "Metal शेडर्स", "id": "Shader Metal",
        "it": "Shader Metal", "ja": "Metalシェーダー", "ko": "Metal 셰이더", "ms": "Shader Metal",
        "nb": "Metal-shadere", "nl": "Metal-shaders", "pl": "Shadery Metal", "pt": "Shaders Metal",
        "ru": "Metal-шейдеры", "sv": "Metal-shaders", "th": "Metal Shaders", "tr": "Metal Shader’ları",
        "uk": "Шейдери Metal", "ur": "Metal شیڈرز", "vi": "Shader Metal", "zh-Hans": "Metal 着色器",
        "zh-Hant": "Metal 著色器",
    },
    "feat4": {  # CoreHaptics
        "en": "CoreHaptics", "ar": "CoreHaptics", "da": "CoreHaptics", "de": "CoreHaptics",
        "es": "CoreHaptics", "fr": "CoreHaptics", "hi": "CoreHaptics", "id": "CoreHaptics",
        "it": "CoreHaptics", "ja": "CoreHaptics", "ko": "CoreHaptics", "ms": "CoreHaptics",
        "nb": "CoreHaptics", "nl": "CoreHaptics", "pl": "CoreHaptics", "pt": "CoreHaptics",
        "ru": "CoreHaptics", "sv": "CoreHaptics", "th": "CoreHaptics", "tr": "CoreHaptics",
        "uk": "CoreHaptics", "ur": "CoreHaptics", "vi": "CoreHaptics", "zh-Hans": "CoreHaptics",
        "zh-Hant": "CoreHaptics",
    },
    "feat5": {  # Game Center
        "en": "Game Center", "ar": "Game Center", "da": "Game Center", "de": "Game Center",
        "es": "Game Center", "fr": "Game Center", "hi": "Game Center", "id": "Game Center",
        "it": "Game Center", "ja": "Game Center", "ko": "Game Center", "ms": "Game Center",
        "nb": "Game Center", "nl": "Game Center", "pl": "Game Center", "pt": "Game Center",
        "ru": "Game Center", "sv": "Game Center", "th": "Game Center", "tr": "Game Center",
        "uk": "Game Center", "ur": "Game Center", "vi": "Game Center", "zh-Hans": "Game Center",
        "zh-Hant": "Game Center",
    },
    "feat6": {  # Daily Challenges
        "en": "Daily Challenges", "ar": "تحديات يومية", "da": "Daglige udfordringer",
        "de": "Tägliche Herausforderungen", "es": "Desafíos diarios", "fr": "Défis quotidiens",
        "hi": "दैनिक चुनौतियाँ", "id": "Tantangan Harian", "it": "Sfide giornaliere",
        "ja": "デイリーチャレンジ", "ko": "일일 도전", "ms": "Cabaran Harian",
        "nb": "Daglige utfordringer", "nl": "Dagelijkse uitdagingen", "pl": "Codzienne wyzwania",
        "pt": "Desafios diários", "ru": "Ежедневные задания", "sv": "Dagliga utmaningar",
        "th": "ภารกิจรายวัน", "tr": "Günlük Meydan Okumalar", "uk": "Щоденні виклики",
        "ur": "روزانہ چیلنجز", "vi": "Thử thách hằng ngày", "zh-Hans": "每日挑战",
        "zh-Hant": "每日挑戰",
    },
    "feat7": {  # 24 Languages
        "en": "24 Languages", "ar": "24 لغة", "da": "24 sprog", "de": "24 Sprachen",
        "es": "24 idiomas", "fr": "24 langues", "hi": "24 भाषाएँ", "id": "24 Bahasa",
        "it": "24 lingue", "ja": "24言語", "ko": "24개 언어", "ms": "24 Bahasa",
        "nb": "24 språk", "nl": "24 talen", "pl": "24 języki", "pt": "24 idiomas",
        "ru": "24 языка", "sv": "24 språk", "th": "24 ภาษา", "tr": "24 dil",
        "uk": "24 мови", "ur": "24 زبانیں", "vi": "24 ngôn ngữ", "zh-Hans": "24 种语言",
        "zh-Hant": "24 種語言",
    },
    "feat8": {  # Accessibility
        "en": "Accessibility", "ar": "إمكانية الوصول", "da": "Tilgængelighed", "de": "Barrierefreiheit",
        "es": "Accesibilidad", "fr": "Accessibilité", "hi": "सुलभता", "id": "Aksesibilitas",
        "it": "Accessibilità", "ja": "アクセシビリティ", "ko": "접근성", "ms": "Kebolehcapaian",
        "nb": "Tilgjengelighet", "nl": "Toegankelijkheid", "pl": "Dostępność", "pt": "Acessibilidade",
        "ru": "Доступность", "sv": "Tillgänglighet", "th": "การเข้าถึง", "tr": "Erişilebilirlik",
        "uk": "Доступність", "ur": "قابلِ رسائی", "vi": "Trợ năng", "zh-Hans": "无障碍",
        "zh-Hant": "無障礙",
    },
    "section_heading": {
        "en": "What’s New in v1.2 — “Engagement Update”",
        "ar": "الجديد في v1.2 — «تحديث التفاعل»",
        "da": "Nyt i v1.2 — “Engagement-opdatering”",
        "de": "Neu in v1.2 — „Engagement-Update“",
        "es": "Novedades en v1.2 — «Actualización de participación»",
        "fr": "Nouveautés de v1.2 — « Mise à jour Engagement »",
        "hi": "v1.2 में नया — “सगाई अपडेट”",
        "id": "Yang Baru di v1.2 — “Pembaruan Keterlibatan”",
        "it": "Novità in v1.2 — “Aggiornamento Engagement”",
        "ja": "v1.2の新機能 — 「エンゲージメントアップデート」",
        "ko": "v1.2의 새로운 기능 — “참여 업데이트”",
        "ms": "Baharu dalam v1.2 — “Kemas Kini Penglibatan”",
        "nb": "Nytt i v1.2 — «Engasjementsoppdatering»",
        "nl": "Nieuw in v1.2 — “Engagement-update”",
        "pl": "Nowości w v1.2 — „Aktualizacja zaangażowania”",
        "pt": "Novidades na v1.2 — “Atualização de engajamento”",
        "ru": "Что нового в v1.2 — «Обновление вовлечённости»",
        "sv": "Nytt i v1.2 — ”Engagemangsuppdatering”",
        "th": "ใหม่ใน v1.2 — “อัปเดตการมีส่วนร่วม”",
        "tr": "v1.2’de Yeni — “Etkileşim Güncellemesi”",
        "uk": "Нове у v1.2 — «Оновлення залучення»",
        "ur": "v1.2 میں نیا — ”انگیجمنٹ اپڈیٹ“",
        "vi": "Mới trong v1.2 — “Bản cập nhật tương tác”",
        "zh-Hans": "v1.2 新增内容 — “参与度更新”",
        "zh-Hant": "v1.2 新增內容 — 「參與度更新」",
    },
    "view_changelog": {
        "en": "View full changelog →", "ar": "عرض سجل التغييرات كاملًا ←",
        "da": "Se hele ændringsloggen →", "de": "Vollständiges Änderungsprotokoll anzeigen →",
        "es": "Ver registro de cambios completo →", "fr": "Voir le journal complet →",
        "hi": "पूर्ण चेंजलॉग देखें →", "id": "Lihat log perubahan lengkap →",
        "it": "Vedi registro completo →", "ja": "完全な変更履歴を見る →",
        "ko": "전체 변경 내역 보기 →", "ms": "Lihat log perubahan penuh →",
        "nb": "Se full endringslogg →", "nl": "Bekijk volledige changelog →",
        "pl": "Zobacz pełny dziennik zmian →", "pt": "Ver registro completo →",
        "ru": "Смотреть полный журнал →", "sv": "Visa hela ändringsloggen →",
        "th": "ดูบันทึกการเปลี่ยนแปลงทั้งหมด →", "tr": "Tüm değişiklik günlüğünü gör →",
        "uk": "Переглянути повний журнал →", "ur": "مکمل چینج لاگ دیکھیں ←",
        "vi": "Xem toàn bộ nhật ký →", "zh-Hans": "查看完整更新日志 →",
        "zh-Hant": "查看完整更新日誌 →",
    },
}


APP_SPECS = {
    "echoes": {
        "src_path": "echoes/index.html",
        "t": ECHOES_T,
        "url_path": "echoes",
        "replacements": [
            ('<span class="hero-badge">Coming Soon · iOS 26</span>', "badge", 'span'),
            ('<p class="tagline">Capture living memories that blend a photo, ambient sound, weather, and the exact place you were when it happened. Revisit them on an immersive map. Built natively for iOS 26.</p>', "tagline", "tagline"),
            ("<h3>Living Memories</h3>", "feat1", "h3"),
            ("<h3>Memory Map</h3>", "feat2", "h3"),
            ("<h3>On-Device ML</h3>", "feat3", "h3"),
            ("<h3>Liquid Glass UI</h3>", "feat4", "h3"),
            ("<h3>Ambient Audio</h3>", "feat5", "h3"),
            ("<h3>11 Languages</h3>", "feat6", "h3"),
            ("<h2>Built on Apple&rsquo;s Latest</h2>", "section_heading", "h2"),
        ],
        "shared_replacements": [
            ('<span class="btn btn-soon">Coming Soon to the App Store</span>', "cta_coming_soon", "btn-soon"),
            ('class="btn btn-ghost">Learn More</a>', "cta_learn_more", "btn-ghost"),
            ('<a href="/echoes/support">Support</a>', "nav_support", "nav-support-echoes"),
        ],
    },
    "block-blaster": {
        "src_path": "block-blaster/index.html",
        "t": BLOCKS_T,
        "url_path": "block-blaster",
        "replacements": [
            ('<span class="hero-badge">Coming Soon</span>', "badge", "span"),
            ('<p class="tagline">A satisfying block puzzle game with explosive combos, beautiful sensory themes, and haptic feedback that makes every line clear feel incredible.</p>', "tagline", "tagline"),
            ("<h3>Explosive Combos</h3>", "feat1", "h3"),
            ("<h3>Sensory Packs</h3>", "feat2", "h3"),
            ("<h3>Power-Ups</h3>", "feat3", "h3"),
            ("<h3>CoreHaptics</h3>", "feat4", "h3"),
            ("<h3>Metal Shaders</h3>", "feat5", "h3"),
            ("<h3>7 Languages</h3>", "feat6", "h3"),
            ("<h2>Five Ways to Play</h2>", "section_heading", "h2"),
            ("<div class=\"stat-label\">Grid Size</div>", "_shared_stat_grid", None),
            ("<div class=\"stat-label\">Game Modes</div>", "_shared_stat_modes", None),
            ("<div class=\"stat-label\">Achievements</div>", "_shared_stat_achievements", None),
            ("<div class=\"stat-label\">Languages</div>", "_shared_stat_languages", None),
        ],
        "shared_replacements": [
            ('<span class="btn btn-soon">Coming Soon to the App Store</span>', "cta_coming_soon", "btn-soon"),
            ('class="btn btn-ghost">Learn More</a>', "cta_learn_more", "btn-ghost"),
            ('<a href="/block-blaster/support">Support</a>', "nav_support", "nav-support-blocks"),
        ],
    },
    "colornumbermatch": {
        "src_path": "colornumbermatch/index.html",
        "t": CNM_T,
        "url_path": "colornumbermatch",
        "replacements": [
            ('<span class="hero-badge live">v1.2 &middot; Live on the App Store</span>', "badge", "live-badge"),
            ('<p class="tagline">A vibrant puzzle game where you match tiles by color, number, or both. 2000+ levels, special tiles, Metal shader effects, CoreHaptics, and full localization for 24 languages including Arabic RTL.</p>', "tagline", "tagline"),
            ("<h3>2000+ Levels</h3>", "feat1", "h3"),
            ("<h3>Special Tiles</h3>", "feat2", "h3"),
            ("<h3>Metal Shaders</h3>", "feat3", "h3"),
            ("<h3>CoreHaptics</h3>", "feat4", "h3"),
            ("<h3>Game Center</h3>", "feat5", "h3"),
            ("<h3>Daily Challenges</h3>", "feat6", "h3"),
            ("<h3>24 Languages</h3>", "feat7", "h3"),
            ("<h3>Accessibility</h3>", "feat8", "h3"),
            ('<h2>What&rsquo;s New in v1.2 &mdash; &ldquo;Engagement Update&rdquo;</h2>', "section_heading", "h2"),
            ('View full changelog &rarr;', "view_changelog", "raw"),
            ("<div class=\"stat-label\">Levels</div>", "_shared_stat_levels", None),
            ("<div class=\"stat-label\">Level Packs</div>", "_shared_stat_packs", None),
            ("<div class=\"stat-label\">Languages</div>", "_shared_stat_languages", None),
            ("<div class=\"stat-label\">Achievements</div>", "_shared_stat_achievements", None),
        ],
        "shared_replacements": [
            ('Download on the App Store', "cta_download", "raw"),
            ('class="btn btn-ghost">Release Notes</a>', "cta_release_notes", "btn-ghost-release"),
            ('<a href="/colornumbermatch/changelog">Changelog</a>', "nav_changelog", "nav-changelog"),
        ],
    },
}


def apply_replacement(html: str, needle: str, value: str, wrapper: str) -> str:
    if needle not in html:
        return html
    if wrapper == "span":
        repl = f'<span class="hero-badge">{value}</span>'
    elif wrapper == "live-badge":
        repl = f'<span class="hero-badge live">{value}</span>'
    elif wrapper == "h3":
        repl = f'<h3>{value}</h3>'
    elif wrapper == "h2":
        repl = f'<h2>{value}</h2>'
    elif wrapper == "tagline":
        repl = f'<p class="tagline">{value}</p>'
    elif wrapper == "btn-soon":
        repl = f'<span class="btn btn-soon">{value}</span>'
    elif wrapper == "btn-ghost":
        repl = f'class="btn btn-ghost">{value}</a>'
    elif wrapper == "btn-ghost-release":
        repl = f'class="btn btn-ghost">{value}</a>'
    elif wrapper == "nav-support-echoes":
        repl = f'<a href="/echoes/support">{value}</a>'
    elif wrapper == "nav-support-blocks":
        repl = f'<a href="/block-blaster/support">{value}</a>'
    elif wrapper == "nav-changelog":
        repl = f'<a href="/colornumbermatch/changelog">{value}</a>'
    else:  # "raw"
        repl = value
    return html.replace(needle, repl, 1)


def app_hreflang_block(url_path: str) -> str:
    """hreflang alternates for a specific app landing page."""
    lines = []
    for code, _, _ in LANGUAGES:
        href = f"https://ixsuper.github.io/{url_path}/" if code == "en" else f"https://ixsuper.github.io/{code}/{url_path}/"
        lines.append(f'    <link rel="alternate" hreflang="{code}" href="{href}">')
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="https://ixsuper.github.io/{url_path}/">')
    return "\n".join(lines)


def app_language_switcher(current_code: str, url_path: str) -> str:
    """Switcher that routes to the same app page in the chosen language."""
    options = []
    for code, name, _ in LANGUAGES:
        href = f"/{url_path}/" if code == "en" else f"/{code}/{url_path}/"
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


def localize_app(src: str, app_key: str, code: str, direction: str) -> str:
    spec = APP_SPECS[app_key]
    app_t = {k: v.get(code, v["en"]) for k, v in spec["t"].items()}
    shared_t = {k: v.get(code, v["en"]) for k, v in SHARED_T.items()}
    html = src

    # 1) Set html lang + dir
    html = re.sub(r'<html\s+lang="[^"]*"[^>]*>', f'<html lang="{code}" dir="{direction}">', html, count=1)

    # 2) Canonical + og:url
    url_path = spec["url_path"]
    canonical = f"https://ixsuper.github.io/{url_path}/" if code == "en" else f"https://ixsuper.github.io/{code}/{url_path}/"
    html = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{canonical}">', html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{canonical}">', html, count=1)

    # 3) App-specific replacements
    for needle, key, wrapper in spec["replacements"]:
        if key == "_skip":
            continue
        if key.startswith("_shared_"):
            real_key = key[len("_shared_"):]
            value = shared_t.get(real_key, shared_t.get(real_key, ""))
            if wrapper is None:
                # stat label is <div class="stat-label">English</div>
                # value is plain text; build the div ourselves
                repl = f'<div class="stat-label">{value}</div>'
                html = html.replace(needle, repl, 1)
            continue
        value = app_t.get(key, "")
        if not value:
            continue
        html = apply_replacement(html, needle, value, wrapper)

    # 4) Shared replacements (CTAs, nav)
    for needle, key, wrapper in spec["shared_replacements"]:
        value = shared_t.get(key, "")
        if not value:
            continue
        html = apply_replacement(html, needle, value, wrapper)

    # 5) Inject hreflang block after <link rel="canonical" ...>
    #    (idempotent: skip if an alternate hreflang block already exists)
    if '<link rel="alternate" hreflang="en"' not in html:
        canon_re = re.compile(r'(<link rel="canonical" href="[^"]+">)')
        html = canon_re.sub(lambda m: m.group(1) + "\n" + app_hreflang_block(url_path), html, count=1)

    # 6) Inject language switcher CSS before first </style>
    #    (idempotent: skip if the switcher CSS marker is already present)
    if '/* ============ Language switcher ============ */' not in html:
        html = html.replace('</style>', LANG_SWITCHER_CSS + '    </style>', 1)

    # 7) Inject language switcher markup after <body>
    #    (idempotent: skip if already present)
    if '<div class="lang-switcher"' not in html:
        body_re = re.compile(r'(<body[^>]*>)')
        html = body_re.sub(lambda m: m.group(1) + "\n" + app_language_switcher(code, url_path), html, count=1)

    # 8) Rewrite internal paths for localized pages so cross-app links
    #    and top-nav back link stay within the same language.
    if code != "en":
        prefix = f"/{code}"
        # Only rewrite app and section links, not asset paths
        html = html.replace('href="/"', f'href="{prefix}/"')
        for other in ("echoes", "block-blaster", "colornumbermatch"):
            html = html.replace(f'href="/{other}/"', f'href="{prefix}/{other}/"')

    return html


# -----------------------------------------------------------------------------
# Light-touch injection for non-landing subpages:
# add a language-switcher pill that routes to /<lang>/ homepage.
# These pages stay in English but gain a multilingual escape hatch.
# -----------------------------------------------------------------------------
HOMEPAGE_SWITCHER_MARKUP = language_switcher("en")  # routes to / (English homepage)

NON_LANDING_SUBPAGES = [
    "404.html",
    "colornumbermatch/changelog.html",
    "colornumbermatch/support.html",
    "echoes/support.html",
    "echoes/privacy.html",
    "echoes/terms.html",
    "block-blaster/privacy.html",
    "block-blaster/terms.html",
    "block-blaster/support.html",
    "privacy.html",
    "terms.html",
]


def inject_switcher_into_subpage(path: str) -> bool:
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return False
    with open(full) as f:
        s = f.read()

    # Skip if switcher already present
    if "lang-switcher" in s:
        return False

    # 1) Inject switcher CSS before first </style>, OR add inline <style> in <head>
    if "</style>" in s:
        s = s.replace("</style>", LANG_SWITCHER_CSS + "    </style>", 1)
    else:
        style_block = "    <style>" + LANG_SWITCHER_CSS + "    </style>\n</head>"
        s = s.replace("</head>", style_block, 1)

    # 2) Inject switcher markup after <body>
    body_re = re.compile(r'(<body[^>]*>)')
    s = body_re.sub(lambda m: m.group(1) + "\n" + HOMEPAGE_SWITCHER_MARKUP, s, count=1)

    with open(full, "w") as f:
        f.write(s)
    return True


def main():
    # Part 1: generate localized landing pages for each app × each language
    generated_count = 0
    for app_key, spec in APP_SPECS.items():
        src_path = os.path.join(ROOT, spec["src_path"])
        if not os.path.exists(src_path):
            print(f"  WARN: missing {spec['src_path']}", file=sys.stderr)
            continue
        with open(src_path) as f:
            src = f.read()

        for code, _, direction in LANGUAGES:
            if code == "en":
                # Regenerate English with hreflang + switcher
                out_path = src_path
            else:
                out_path = os.path.join(ROOT, code, spec["url_path"], "index.html")
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            localized = localize_app(src, app_key, code, direction)
            with open(out_path, "w") as f:
                f.write(localized)
            generated_count += 1

    print(f"  generated {generated_count} app landing pages")

    # Part 2: inject switcher into remaining subpages
    injected = 0
    for p in NON_LANDING_SUBPAGES:
        if inject_switcher_into_subpage(p):
            injected += 1
            print(f"  injected switcher into {p}")
    print(f"  injected switcher into {injected} subpages")

    print("\nDone.")


if __name__ == "__main__":
    main()
