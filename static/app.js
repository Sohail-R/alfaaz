// ── Toast ────────────────────────────────────────────────
window.showToast = function(msg) {
    var t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(function() { t.classList.remove('show'); }, 3000);
};

// ── Site-wide transliteration ────────────────────────────
var TranslitManager = (function() {
    var enabled = sessionStorage.getItem('alfaaz_roman') === 'true';
    var cache = {};

    function updateBtn() {
        var btn = document.getElementById('translitToggle');
        if (!btn) return;
        btn.textContent = enabled ? 'Roman: ON' : 'Roman';
        enabled ? btn.classList.add('active') : btn.classList.remove('active');
    }

    function getElements() {
        return Array.from(document.querySelectorAll('[data-urdu]'));
    }

    function applyState() {
        var els = getElements();
        if (els.length === 0) return;

        if (!enabled) {
            els.forEach(function(el) {
                el.textContent = el.getAttribute('data-urdu');
                el.setAttribute('dir', 'rtl');
                el.classList.remove('is-roman');
            });
            return;
        }

        // collect texts not yet cached
        var toFetch = [];
        els.forEach(function(el) {
            var u = el.getAttribute('data-urdu');
            if (!cache[u]) toFetch.push(u);
        });

        function render() {
            els.forEach(function(el) {
                var u = el.getAttribute('data-urdu');
                var roman = cache[u] || u;
                el.textContent = roman;
                el.setAttribute('dir', 'ltr');
                el.classList.add('is-roman');
            });
        }

        if (toFetch.length === 0) { render(); return; }

        fetch('/transliterate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ lines: toFetch })
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            toFetch.forEach(function(t, i) { cache[t] = data.lines[i] || t; });
            render();
        })
        .catch(render);
    }

    return {
        toggle: function() {
            enabled = !enabled;
            sessionStorage.setItem('alfaaz_roman', enabled);
            updateBtn();
            applyState();
        },
        init: function() {
            updateBtn();
            applyState();
        },
        refresh: function() { applyState(); }
    };
})();

document.addEventListener('DOMContentLoaded', function() {
    TranslitManager.init();
});