/* SSF, mockup del sito. Revisione del 27/09/2026, R21.
   Il bottone della barra e' dorato (commento U1 del committente), ma in ogni schermata deve esserci
   un solo oro-superficie ([3.2] M3.c). Quindi e' pieno quando nessun altro bottone dorato e' in vista,
   e diventa solo contorno dorato quando uno lo e'. Senza JavaScript il bottone resta pieno, come prima. */
(function () {
  var barra = document.querySelector('.ssf-nav > .ssf-btn--primary');
  var altri = document.querySelectorAll('main .ssf-btn--primary');
  if (!barra || !altri.length || !('IntersectionObserver' in window)) return;
  var nav = barra.parentElement;
  var visibili = new Set();
  var osservatore = null;
  var attesa = null;

  function aggiorna() {
    barra.classList.toggle('ssf-btn--in-attesa', visibili.size > 0);
  }

  function osserva() {
    if (osservatore) osservatore.disconnect();
    visibili.clear();
    /* Un bottone coperto dalla barra appiccicata non e' in vista: si toglie l'altezza della barra */
    osservatore = new IntersectionObserver(function (voci) {
      voci.forEach(function (v) {
        if (v.isIntersecting) visibili.add(v.target); else visibili.delete(v.target);
      });
      aggiorna();
    }, { rootMargin: '-' + nav.offsetHeight + 'px 0px 0px 0px' });
    altri.forEach(function (b) { osservatore.observe(b); });
  }

  osserva();
  /* La barra e' alta 56px sul telefono e 72px da 1024px: al cambio di larghezza si ricomincia */
  window.addEventListener('resize', function () {
    clearTimeout(attesa);
    attesa = setTimeout(osserva, 200);
  });
})();
