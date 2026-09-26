# Mockup del sito di Scherma Storica Firenze

Uno **scheletro navigabile** del nuovo sito di A.S.D. Scherma Storica Firenze, per raccogliere dai
soci i commenti sulla **struttura**: quali pagine ci sono, in che ordine, con quali sezioni, e come
si arriva a chiedere i tre allenamenti gratuiti.

**Non è il sito ufficiale.** Testi e foto sono segnaposto. Le pagine sono escluse da Google
(`noindex`).

## Come è fatto

- HTML e CSS statici, niente JavaScript. Menu del telefono e domande si aprono con `<details>`.
- `assets/css/tokens.css` è la copia dei token del brand, da non modificare. Se i token cambiano, si
  ricopia da `Sito Web/Brand Identity/verifiche/tokens.css`.
- `assets/css/sistema.css` contiene griglia, tipografia e componenti del design system ([4.2],
  [4.3]); `assets/css/mockup.css` solo la fascia e i segnaposto.
- **Le pagine `*.html` in questa cartella sono generate: non si modificano a mano.** Barra, piede,
  fascia e bottone WhatsApp stanno in `_sorgenti/modello.html`; il contenuto di ogni pagina sta in
  `_sorgenti/pagine/<nome>.html`.

## Come si aggiorna

1. Modifica il frammento in `_sorgenti/pagine/`, oppure `_sorgenti/modello.html` per le parti comuni.
2. `python _sorgenti/componi.py` rigenera le pagine.
3. `python ../prove/verifica.py` controlla collegamenti, larghezze, `noindex` e prima schermata.
4. Commit e invio: GitHub Pages ripubblica da solo.

Le scorciatoie dei frammenti (`{{foto 4x5 | …}}`, `{{righe 3}}`, `{{icona:…}}`, `{{giglio}}`) sono
spiegate in testa a `_sorgenti/componi.py`.

## Come si pubblica (una volta sola)

1. Account GitHub **intestato all'associazione**, repository **pubblico** `mockup-sito-web`.
2. Da questa cartella: collegare il repository remoto, fare il commit e inviare.
3. Su GitHub: Settings → Pages → Build and deployment → Source «Deploy from a branch», ramo `main`,
   cartella `/ (root)` → Save.
4. Dopo un paio di minuti il mockup è su `https://scherma-storica-firenze.github.io/mockup-sito-web/`. Controllare che
   `…/_sorgenti/componi.py` risponda 404: Jekyll esclude le cartelle che iniziano con «_».

## Crediti

Glifo di WhatsApp: [Simple Icons](https://simpleicons.org), licenza CC0. Icone HEMA e di servizio:
disegnate per SSF; il contorno del libro deriva da Lucide (ISC).
