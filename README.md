# ContrattoOrologio.click

Generatore gratuito di **contratti di compravendita e di permuta di orologi usati tra privati**.
Sito: **https://contrattoorologio.click**

Il codice è pubblico perché chiunque possa verificare la promessa principale del sito:
**i dati inseriti nel modulo non vengono mai salvati né inviati a nessuno.**

---

## Cosa fa

- Contratto di **compravendita** e di **permuta** (anche più orologi, con conguaglio calcolato in automatico)
- Dati di venditore e compratore, marca, modello, materiale, referenza, matricola, colore del quadrante, full set / scatola / garanzia
- Dichiarazione di piena proprietà, lecita provenienza e manleva del venditore
- Pagamento in contanti, bonifico o assegno, con blocco del contante dai 5.000 € in su (art. 49 D.Lgs. 231/2007)
- Calcolo automatico del codice fiscale e maiuscole automatiche
- Spazio per la marca da bollo, un foglio A4 da stampare o salvare in PDF
- **Versione in bianco** da compilare a penna
- Guida alla compravendita sicura, norme di riferimento, FAQ

## Come è fatto

Tutto il sito è **un solo file**: [`index.html`](index.html). Non c'è backend, non c'è database, non ci sono librerie di terze parti e i caratteri tipografici sono ospitati nel sito stesso: **all'apertura la pagina non contatta nessun server esterno.**
Il contratto viene costruito **nel browser di chi lo compila** e stampato con la funzione di stampa del browser.

| File | A cosa serve |
|---|---|
| `index.html` | L'intero sito: pagina, modulo, generazione del contratto |
| `fonts/` | Caratteri Inter e Crimson Text (licenza SIL OFL 1.1, testi in `fonts/OFL-*.txt`) |
| `.htaccess` | Intestazioni di sicurezza per hosting Apache / LiteSpeed (Hostinger, Aruba, SiteGround…) |
| `htaccess.txt` | Copia visibile di `.htaccess`, comoda da caricare: sul server va rinominata in `.htaccess` |
| `_headers` | Le stesse intestazioni per Netlify e Cloudflare Pages |
| `tools/csp-hash.py` | Ricalcola gli hash di script e stile per la Content Security Policy |
| `robots.txt`, `sitemap.xml`, `og-image.png` | Indicizzazione e anteprima social |

---

## Privacy: cosa garantisce il codice

1. **Nessun invio dei dati del modulo.** Nel codice c'è una sola richiesta di rete fatta dalla pagina: `fetch(COMUNI_URL)`, che **scarica** l'elenco pubblico dei comuni italiani per calcolare il codice fiscale. Non invia nulla.
2. **Nessun salvataggio.** L'unico dato scritto nel browser è la scelta sui cookie (`localStorage`, chiave `co_consent`: solo "granted" o "denied" con la data). I campi del modulo vivono solo nella memoria della pagina e spariscono alla chiusura.
3. **Nessun invio di moduli.** I moduli non hanno destinazione, i campi statici non hanno attributo `name` e i pulsanti non inviano: anche con JavaScript disattivato nessun dato può finire nell'indirizzo della pagina o nei log del server.
4. **Nessuna cronologia dei campi.** `autocomplete="off"` impedisce al browser di ricordare codici fiscali e numeri di documento.
5. **Google Analytics solo con consenso.** Lo script di Google non è presente nella pagina: viene aggiunto **solo** dopo il clic su "Accetta le statistiche" (funzione `loadGA`). Se l'utente rifiuta non viene mai scaricato. Analytics non riceve i campi del modulo.
6. **Nessuna pubblicità**, nessun pixel di social network, nessun cookie di profilazione.

### Servizi esterni contattati

| Servizio | Quando | Cosa riceve |
|---|---|---|
| jsDelivr (`cdn.jsdelivr.net`) | Quando si compila il luogo di nascita | Indirizzo IP; la richiesta è un download, non contiene dati |
| Google Analytics 4 | **Solo dopo il consenso** | Pagina visitata, tipo di dispositivo, provenienza |

### Content Security Policy

La **Content Security Policy** è scritta in due punti: dentro `index.html` (tag `<meta http-equiv="Content-Security-Policy">`, quindi visibile a chiunque apra il codice della pagina e valida su qualsiasi hosting) e nelle intestazioni del server (`.htaccess` / `_headers`), che aggiungono le protezioni possibili solo lato server (HSTS, `frame-ancestors`, `X-Frame-Options`). La policy:

- consente connessioni **solo** verso `cdn.jsdelivr.net` e i domini di Google Analytics (`connect-src`);
- vieta l'invio di qualsiasi modulo (`form-action 'none'`);
- esegue **solo** lo script e lo stile di `index.html` i cui hash sha256 sono dichiarati (`script-src`, `style-src`), più lo script di Analytics quando c'è il consenso;
- carica i caratteri solo dal sito stesso (`font-src 'self'`) e non invia il referrer (`Referrer-Policy: no-referrer`).

In pratica, anche se qualcuno modificasse il sito per rubare dati, **sarebbe il browser stesso a bloccare l'invio** verso qualsiasi altro indirizzo.

Se modifichi `index.html`, ricalcola gli hash e aggiorna in automatico `.htaccess`, `_headers` e il meta di `index.html`:

```bash
python3 tools/csp-hash.py --write
```

---

## Installazione su hosting Apache / LiteSpeed (es. Hostinger)

1. Carica tutti i file nella cartella principale del sito (`public_html`), compresa la cartella `fonts/`.
2. Carica `htaccess.txt` e **rinominalo in `.htaccess`** dal File Manager dell'hosting.
3. Verifica: `https://contrattoorologio.click/fonts/` deve rispondere **403 Forbidden**. Se invece vedi l'elenco dei file, il `.htaccess` non è attivo.

## Come verificarlo da soli

**Senza competenze tecniche**
1. Apri https://contrattoorologio.click
2. Metti il telefono o il computer in **modalità aereo**
3. Compila e genera il contratto: funziona lo stesso, perché tutto avviene sul tuo dispositivo.

**Con il browser**
1. Apri il sito, premi `F12` e vai nella scheda **Rete** (Network)
2. Compila il modulo e genera il contratto
3. Non comparirà nessuna richiesta che contiene i dati inseriti.

**Leggendo il codice**
- Cerca in `index.html`: `fetch(`, `XMLHttpRequest`, `sendBeacon`, `WebSocket`, `localStorage`, `action=`
- Troverai solo il download dell'elenco dei comuni e il salvataggio della scelta sui cookie.

**Con strumenti indipendenti**
- [Webbkoll](https://webbkoll.dataskydd.net/en/) – cookie e connessioni verso terzi
- [Blacklight](https://themarkup.org/blacklight) – tracker e profilazione
- [Mozilla HTTP Observatory](https://developer.mozilla.org/en-US/observatory) – intestazioni di sicurezza

**Verificare che il sito online sia questo codice**
Scarica la pagina pubblicata e confrontala con `index.html` di questo repository:
```bash
curl -s https://contrattoorologio.click/ | sha256sum
sha256sum index.html
```
I due valori devono coincidere.

---

## Esclusione di responsabilità

Il sito e i modelli di contratto sono offerti gratuitamente, a solo scopo informativo, e non costituiscono consulenza legale, fiscale o professionale. Il titolare non si assume alcuna responsabilità per l'uso dei documenti generati, per i dati inseriti, per l'identità delle parti, per l'autenticità o la provenienza dei beni, per i pagamenti e per il rispetto delle norme sul contante. Ogni responsabilità relativa al contratto ricade sulle parti che lo firmano.

## Contatti

Alessandro Di Bella – info@contrattoorologio.click
Segnalazioni di problemi o di dubbi sulla privacy: apri una [Issue](https://github.com/dibbellas/contrattoorologio.click/issues) in questo repository.

© 2026 Alessandro Di Bella. Il codice è pubblicato per trasparenza e verifica. Tutti i diritti riservati.
