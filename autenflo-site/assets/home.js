(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  var y = $('#yr'); if (y) y.textContent = new Date().getFullYear();

  /* ---- scroll reveal ---- */
  var rv = $$('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .12, rootMargin: '0px 0px -6% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  /* ---- WhatsApp chat player ---- */
  function play(box, loop) {
    if (!box) return;
    var items = [].slice.call(box.children), tok = box._t = (box._t || 0) + 1;
    items.forEach(function (n) { n.classList.remove('show'); });
    if (reduce) { items.forEach(function (n) { if (!n.classList.contains('typing')) n.classList.add('show'); }); return; }
    (function step(i) {
      if (box._t !== tok) return;
      if (i >= items.length) { if (loop) setTimeout(function () { if (box._t === tok && !document.hidden) play(box, loop); else if (box._t === tok) setTimeout(function () { play(box, loop); }, 3000); }, 7000); return; }
      var n = items[i];
      if (n.classList.contains('typing')) {
        n.classList.add('show');
        setTimeout(function () { n.classList.remove('show'); step(i + 1); }, 800);
      } else {
        n.classList.add('show');
        setTimeout(function () { step(i + 1); }, n.classList.contains('me') ? 450 : 750);
      }
    })(0);
  }
  setTimeout(function () { play($('#heroBoard'), true); }, 500);

  /* ---- business selector ---- */
  var tabs = $$('.bt');
  function pick(i, focus) {
    tabs.forEach(function (t, k) {
      var on = k === i;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      var p = document.getElementById('pn' + k);
      if (p) p.hidden = !on;
      if (on && p) play($('.wa-b', p));
    });
    if (focus) tabs[i].focus();
  }
  tabs.forEach(function (t, i) {
    t.tabIndex = i ? -1 : 0;
    t.addEventListener('click', function () {
      pick(i);
      if (window.innerWidth < 981) { var p = document.getElementById('pn' + i); if (p) setTimeout(function () { p.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); }, 30); }
    });
    t.addEventListener('keydown', function (e) {
      var k = e.key, n = tabs.length;
      if (k === 'ArrowDown' || k === 'ArrowRight') { e.preventDefault(); pick((i + 1) % n, true); }
      if (k === 'ArrowUp' || k === 'ArrowLeft') { e.preventDefault(); pick((i + n - 1) % n, true); }
    });
  });
  var first = $('#pn0 .wa-b');
  if (first) {
    if ('IntersectionObserver' in window) {
      var io2 = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { play(first); io2.disconnect(); } }, { threshold: .35 });
      io2.observe(first);
    } else play(first);
  }

  /* ---- ROI calculator ---- */
  var r = ['r1', 'r2', 'r3', 'r4'].map(function (id) { return document.getElementById(id); });
  if (r[0]) {
    var o = ['o1', 'o2', 'o3', 'o4'].map(function (id) { return document.getElementById(id); });
    var v1 = document.getElementById('v1'), v2 = document.getElementById('v2');
    var calc = function () {
      var a = +r[0].value, b = +r[1].value, c = +r[2].value, d = +r[3].value;
      o[0].textContent = a; o[1].textContent = b; o[2].textContent = c; o[3].textContent = d;
      var t = a * b * c * 52;
      v1.textContent = '₹' + t.toLocaleString('en-IN');
      var s = Math.round(t * d / 100);
      v2.textContent = '₹' + s.toLocaleString('en-IN');
      var w = document.getElementById('rw');
      if (w) w.href = 'https://wa.me/918849031907?text=' + encodeURIComponent('Namaste autenflo, mere manual kaam ka kharcha lagbhag ₹' + t.toLocaleString('en-IN') + ' saalana hai. Mujhe apna asli hisaab karwana hai.');
    };
    r.forEach(function (e) { e.addEventListener('input', calc); });
    calc();
  }
})();
