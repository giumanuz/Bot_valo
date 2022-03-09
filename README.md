[![BotValo](https://github.com/giumanuz/Bot_valo/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/giumanuz/Bot_valo/actions/workflows/python-app.yml)

## Risposte

Vediamo come si possono aggiungere e/o modificare le risposte del bot.

### Sintassi delle risposte
Le associazioni trigger-risposta stanno tutte nel file `risposte.json` dentro `resources/text_files`.
La sintassi di questo file è la seguente:
```json
{
   "trigger1": "risposta1",
   "trigger2": ["possibile risposta", "altra possibile risposta"],
   "trigger3": "ALT::trigger1"
}
```
In questo esempio, se qualcuno scrive in chat la parola "trigger1", il bot risponderà con "risposta1".
Abbastanza semplice, no?

Se, invece, specifichi una *lista* di stringhe, il bot risponderà con una delle
risposte in modo casuale. Ovvero, se si scrive in chat "trigger2", il bot risponderà con una delle due
risposte che gli sono state fornite: il 50% delle volte manderà "possibile risposta", l'altro 50% manderà
"altra possibile risposta".

Infine, per specificare un'**alternativa** a un possibile trigger, basta scrivere nella risposta `ALT::`
seguito dal trigger di cui è un'alternativa. In questo esempio, se qualcuno scrive in chat "trigger3",
il bot risponderà con "risposta1". Ovvero, "trigger3" e "trigger1" sono alternative alla stessa risposta.
Funziona anche se è l'alternativa di un insieme di risposte, ovvero era possibile scrivere
`"trigger3": "ALT::trigger2"`, in questo modo "trigger3" e "*trigger2*" diventano alternative.

> **Nota:** `ALT::` funziona solamente se come alternativa si specifica un trigger che è stato già definito.
> Non funzionerà se punta ad un'altra alternativa.

### Aggiungere o rimuovere risposte

Per aggiungerne di nuove, basta modificare il file `risposte.json` e aggiungere risposte seguendo la
sintassi specificata. Per rimuoverle, basta cancellare la rispettiva riga. 

> **Attenzione:** L'ultimo elemento del json **non deve avere la
virgola finale**.
> 
> **Nota:** Quando si elimina una risposta, bisogna stare attenti a **eliminare anche tutte le
> alternative**. Nel caso in cui un'alternativa manca, il bot manda il messaggio letterale
> (ovvero, compreso di `ALT::`) e viene loggato un warning nella console.
