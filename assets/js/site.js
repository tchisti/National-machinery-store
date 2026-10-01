/* National Machinery Stores — site behaviour. No dependencies. */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var WA = doc.getAttribute('data-wa') || '918866688626';

  /* Mobile drawer */
  var drawer = document.getElementById('drawer');
  var openBtn = document.querySelector('[data-open-drawer]');
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle('is-open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    if (openBtn) openBtn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) { var f = drawer.querySelector('a, button'); if (f) f.focus(); }
    else if (openBtn) openBtn.focus();
  }
  if (openBtn) openBtn.addEventListener('click', function () { setDrawer(true); });
  document.querySelectorAll('[data-close-drawer]').forEach(function (el) {
    el.addEventListener('click', function () { setDrawer(false); });
  });
  if (drawer) drawer.querySelectorAll('nav a').forEach(function (a) {
    a.addEventListener('click', function () { setDrawer(false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('is-open')) setDrawer(false);
  });

  /* Scroll reveal (content stays visible without JS) */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && rv.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* Product stage filter */
  var chips = document.querySelectorAll('[data-filter]');
  var cards = document.querySelectorAll('[data-stage]');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-filter');
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      cards.forEach(function (card) {
        card.hidden = !(f === 'all' || card.getAttribute('data-stage') === f);
        if (!card.hidden) card.classList.add('is-in');
      });
    });
  });

  /* Product gallery */
  var main = document.querySelector('[data-gallery-main]');
  var thumbs = document.querySelectorAll('[data-gallery-thumb]');
  thumbs.forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (!main) return;
      main.src = btn.getAttribute('data-src');
      main.alt = btn.getAttribute('data-alt') || main.alt;
      thumbs.forEach(function (t) { t.setAttribute('aria-current', String(t === btn)); });
    });
  });

  /* Inquiry form → WhatsApp (zero-backend lead capture) */
  document.querySelectorAll('form[data-wa-form]').forEach(function (form) {
    var sel = form.querySelector('select[name="product"]');
    var other = form.querySelector('[data-other]');
    if (sel && other) {
      sel.addEventListener('change', function () {
        var show = sel.value === 'Other';
        other.hidden = !show;
        var inp = other.querySelector('input');
        if (inp) { inp.required = show; if (!show) inp.value = ''; }
      });
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var v = function (n) { var el = form.elements[n]; return el ? String(el.value || '').trim() : ''; };
      var product = v('product');
      if (product === 'Other' && v('other')) product = 'Other: ' + v('other');
      var lines = ['Hello National Machinery Stores,', ''];
      if (v('name')) lines.push('Name: ' + v('name'));
      if (v('phone')) lines.push('Phone: ' + v('phone'));
      if (v('company')) lines.push('Company: ' + v('company'));
      if (v('city')) lines.push('City/State: ' + v('city'));
      if (product) lines.push('Product: ' + product);
      if (v('capacity')) lines.push('Capacity / seed: ' + v('capacity'));
      if (v('message')) { lines.push(''); lines.push(v('message')); }
      lines.push(''); lines.push('Please share price, availability and delivery time.');
      var url = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(lines.join('\n'));
      var status = form.querySelector('.form-status');
      if (status) status.textContent = 'Opening WhatsApp with your inquiry…';
      // 'noopener' as a window feature makes window.open() return null, so sever the opener manually
      var w = window.open(url, '_blank');
      if (w) { try { w.opener = null; } catch (err) { /* cross-origin */ } }
      else window.location.href = url;
      setTimeout(function () { if (status) status.textContent = 'Sent to WhatsApp. We call back within 24–48 hours.'; form.reset(); if (other) other.hidden = true; }, 1200);
    });
  });

  /* Footer year */
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
