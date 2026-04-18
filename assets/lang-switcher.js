/* ============================================================
   Context-aware language switcher.
   Replaces the inline `onchange="window.location.href=this.value"`.
   When the user picks a language, navigate to the same page in the
   chosen locale (e.g. /echoes/privacy → /ar/echoes/privacy).
   ============================================================ */
(function () {
    var LOCALES = ['ar', 'da', 'de', 'es', 'fr', 'hi', 'id', 'it', 'ja', 'ko',
                   'ms', 'nb', 'nl', 'pl', 'pt', 'ru', 'sv', 'th', 'tr', 'uk',
                   'ur', 'vi', 'zh-Hans', 'zh-Hant'];
    var LOCALE_RE = new RegExp('^/(' + LOCALES.join('|') + ')(/|$)');

    function currentSubpath() {
        // Returns the path after the locale prefix, always starting with "/".
        var p = window.location.pathname;
        var m = p.match(LOCALE_RE);
        if (m) return p.substring(m[1].length + 1) || '/';
        return p || '/';
    }

    function targetUrl(value) {
        // `value` is the option value, either "/" (English) or "/<lang>/".
        var sub = currentSubpath();
        if (value === '/' || value === '') {
            return sub;
        }
        // value is like "/ar/" — drop trailing slash, prepend to sub.
        var lang = value.replace(/^\/|\/$/g, '');
        if (sub === '/') return '/' + lang + '/';
        return '/' + lang + sub;
    }

    function preselect(select) {
        // Mark the option matching the current locale as selected, so the
        // dropdown reflects where you are even on subpages.
        var p = window.location.pathname;
        var m = p.match(LOCALE_RE);
        var current = m ? '/' + m[1] + '/' : '/';
        Array.prototype.forEach.call(select.options, function (opt) {
            opt.selected = (opt.value === current);
        });
    }

    function attach(select) {
        // Strip any inline onchange so we own navigation.
        select.onchange = null;
        select.removeAttribute('onchange');
        preselect(select);
        select.addEventListener('change', function (e) {
            window.location.href = targetUrl(e.target.value);
        });
    }

    function init() {
        var selects = document.querySelectorAll('.lang-switcher select');
        Array.prototype.forEach.call(selects, attach);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
