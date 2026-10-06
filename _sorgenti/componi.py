# -*- coding: utf-8 -*-
"""Compone le pagine del mockup: modello.html + pagine/<file>.html -> ../<file>.html

Le pagine composte NON si modificano a mano: si modifica il frammento o il
modello e si rilancia  python componi.py

Ogni frammento comincia con  <!-- titolo: Corsi | voce: corsi -->
(voce = la voce di menu da segnare come attiva; "-" per nessuna).

Scorciatoie dentro i frammenti e il modello:
  {{icona:nome}}            SVG di assets/icons/nome.svg, in linea
  {{icona-grande:nome}}     lo stesso, con la classe .ic
  {{foto 4x5 | testo}}      riquadro segnaposto; tipi: foto video mappa
                            recensioni tavola logo; proporzioni: 16x9 3x2
                            4x5 1x1 3x1 auto, "16x9/tel-4x5";
                            "sfondo/16x9/tel-4x5" = foto sotto il testo della prima schermata
  {{righe 4}}               barre grigie che mostrano quanto testo ci andra'
  {{giglio}}                filigrana del giglio
"""
import re
from pathlib import Path

QUI = Path(__file__).resolve().parent
SITO = QUI.parent
ICONE = SITO / "assets" / "icons"

# Revisione del 27/09: «Corsi e costi», perche' i costi si trovino dal menu; Sponsor scende nel piede.
# 06/10: «Sedi» (Firenze e Livorno) e, sotto «Chi siamo», la sottovoce «Istruttori»
VOCI = [("corsi.html", "Corsi e costi", "corsi", []),
        ("sedi.html", "Sedi", "sedi", []),
        ("chi-siamo.html", "Chi siamo", "chi-siamo", [("istruttori.html", "Istruttori", "istruttori")]),
        ("eventi.html", "Eventi", "eventi", []),
        ("foto-e-video.html", "Foto e video", "foto-e-video", []),
        ("blog.html", "Blog", "blog", []),
        ("contatti.html", "Contatti", "contatti", [])]

TIPI = {"foto": ("FOTO", "foto"), "video": ("VIDEO", "video"), "mappa": ("MAPPA", "mappa"),
        "recensioni": ("RECENSIONI GOOGLE", "stella"),
        "tavola": ("TAVOLA DEL TRATTATO", "ssf-ic-hema-treatise"),
        "logo": ("LOGO", "logo-sponsor")}


def icona(nome, classe=""):
    svg = (ICONE / (nome + ".svg")).read_text(encoding="utf-8")
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    attr = ' aria-hidden="true" focusable="false"' + (' class="%s"' % classe if classe else "")
    return svg.replace("<svg", "<svg" + attr, 1)


def segnaposto(m):
    tipo, prop, testo = m.group(1), m.group(2) or "auto", m.group(3).strip()
    etichetta, ic = TIPI[tipo]
    parti = prop.split("/")
    classi = ["ph"] + [("ssf-hero__foto" if p == "sfondo" else "ph--" + p) for p in parti]
    misure = [p for p in parti if p not in ("sfondo", "auto")]
    leggibile = ""
    if misure:
        leggibile = misure[0].replace("x", ":")
        if len(misure) > 1:
            leggibile += ", sul telefono " + misure[1].replace("tel-", "").replace("x", ":")
    coda = " · " + leggibile if leggibile else ""
    return ('<figure class="%s">%s<figcaption><strong>%s</strong> · %s%s</figcaption></figure>'
            % (" ".join(classi), icona(ic), etichetta, testo, coda))


def righe(m):
    return ('<div class="ph-righe" aria-hidden="true">' + "<span></span>" * int(m.group(1)) + "</div>")


def espandi(html):
    html = re.sub(r"\{\{icona-grande:([\w-]+)\}\}", lambda m: icona(m.group(1), "ic"), html)
    html = re.sub(r"\{\{icona:([\w-]+)\}\}", lambda m: icona(m.group(1)), html)
    html = re.sub(r"\{\{(foto|video|mappa|recensioni|tavola|logo)(?:\s+([\w/-]+))?\s*\|\s*(.*?)\}\}",
                  segnaposto, html, flags=re.S)
    html = re.sub(r"\{\{righe (\d+)\}\}", righe, html)
    html = html.replace("{{giglio}}", '<svg class="ssf-filigrana" viewBox="0 0 524 549.4" '
                        'aria-hidden="true" focusable="false"><use href="#giglio"/></svg>')
    resto = re.findall(r"\{\{.*?\}\}", html)
    if resto:
        raise SystemExit("Scorciatoia sconosciuta: " + resto[0])
    return html


def giglio_symbol():
    svg = (SITO / "assets" / "img" / "giglio.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    corpo = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1).strip()
    return '<symbol id="giglio" viewBox="0 0 524.0 549.4">' + corpo + "</symbol>"


def voce(href, nome, chiave, attiva, classe="ssf-nav__voce"):
    corrente = ' aria-current="page"' if chiave == attiva else ""
    return '<a class="%s" href="%s"%s>%s</a>' % (classe, href, corrente, nome)


def voci(attiva):
    """Le voci con sottovoci diventano un gruppo: sul telefono la sottovoce sta rientrata
    sotto la voce madre, da 1024px si apre a tendina al passaggio o al fuoco."""
    righe_html = []
    for href, nome, chiave, figlie in VOCI:
        if not figlie:
            righe_html.append("    " + voce(href, nome, chiave, attiva))
            continue
        madre = "ssf-nav__voce" + (" ssf-nav__voce--madre" if attiva in [f[2] for f in figlie] else "")
        sotto = "".join(voce(h, n, c, attiva, "ssf-nav__voce ssf-nav__voce--figlia") for h, n, c in figlie)
        righe_html.append('    <div class="ssf-nav__gruppo">%s<div class="ssf-nav__sotto">%s</div></div>'
                          % (voce(href, nome, chiave, attiva, madre), sotto))
    return "\n".join(righe_html)


def main():
    modello = (QUI / "modello.html").read_text(encoding="utf-8")
    giglio = giglio_symbol()
    fatte = []
    for frammento in sorted((QUI / "pagine").glob("*.html")):
        testo = frammento.read_text(encoding="utf-8")
        testa = re.match(r"\s*<!--\s*titolo:\s*(.*?)\s*\|\s*voce:\s*([\w-]+)\s*-->\s*", testo)
        if not testa:
            raise SystemExit("Manca l'intestazione in " + frammento.name)
        titolo, voce = testa.group(1), testa.group(2)
        pagina = (modello.replace("%%TITOLO%%", titolo)
                         .replace("%%VOCI%%", voci(voce))
                         .replace("%%CONTENUTO%%", testo[testa.end():].rstrip())
                         .replace("%%GIGLIO%%", giglio))
        (SITO / frammento.name).write_text(espandi(pagina), encoding="utf-8")
        fatte.append(frammento.name)
    print("Composte %d pagine: %s" % (len(fatte), ", ".join(fatte)))


if __name__ == "__main__":
    main()
