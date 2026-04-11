/* ============================================================
   Privacy-respecting analytics loader
   ============================================================
   No cookies. No cross-site tracking. No fingerprinting.
   Honors Do Not Track and the Global Privacy Control.

   Default: disabled (no network requests until a provider is
   uncommented below). Pick ONE provider and uncomment it.

   Option A — Plausible (recommended, paid, cookie-free)
     1. Sign up at https://plausible.io
     2. Add "ixsuper.github.io" as a site
     3. Uncomment the Plausible block below
     4. The script auto-pings pageviews; no further work needed

   Option B — GoatCounter (free for personal use, open source)
     1. Sign up at https://www.goatcounter.com
     2. Your site becomes YOURNAME.goatcounter.com
     3. Uncomment the GoatCounter block and replace YOURNAME

   Option C — Cloudflare Web Analytics (free)
     1. Sign up at https://www.cloudflare.com/web-analytics/
     2. Add this site and copy the beacon token
     3. Uncomment the Cloudflare block and replace the token

   Option D — None. Leave everything commented. The script then
   does nothing and no requests are made.
   ============================================================ */

(function () {
    'use strict';

    // Honor user privacy signals: do not load any analytics if the
    // user has enabled Do Not Track or the Global Privacy Control.
    var dnt = navigator.doNotTrack === '1'
           || window.doNotTrack === '1'
           || navigator.globalPrivacyControl === true;
    if (dnt) return;

    // Skip analytics on localhost and dev hosts.
    var host = window.location.hostname;
    if (host === 'localhost' || host === '127.0.0.1' || host === '') return;

    function load(src, attrs) {
        var s = document.createElement('script');
        s.defer = true;
        s.src = src;
        if (attrs) {
            Object.keys(attrs).forEach(function (k) { s.setAttribute(k, attrs[k]); });
        }
        document.head.appendChild(s);
    }

    /* ---------- Option A: Plausible ----------
    load('https://plausible.io/js/script.js', {
        'data-domain': 'ixsuper.github.io'
    });
    ------------------------------------------- */

    /* ---------- Option B: GoatCounter ----------
    load('//gc.zgo.at/count.js', {
        'data-goatcounter': 'https://YOURNAME.goatcounter.com/count',
        'async': 'async'
    });
    -------------------------------------------- */

    /* ---------- Option C: Cloudflare Web Analytics ----------
    load('https://static.cloudflareinsights.com/beacon.min.js', {
        'data-cf-beacon': '{"token": "YOUR_TOKEN_HERE"}'
    });
    ---------------------------------------------------------- */

})();
