[![BotValo](https://github.com/giumanuz/Bot_valo/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/giumanuz/Bot_valo/actions/workflows/python-app.yml)

## Setup

Questo readme è temporaneo, verranno scritte delle pagine wiki dettagliate appena sarà
disponibile.

Per setuppare il bot dopo il merge `edotm/firebase-integration` è necessario avere un
file `.env` con dentro tutte le informazioni necessarie per far partire il bot. Guarda,
per riferimento, il file `.env_sample`.

Il file `.env` che va usato per il testing si trova sul server discord comune, nella
chat `#botvalo-shit`. **Importante:** discord lo fa scaricare come "env", senza il punto
davanti, ma deve essere rinominato in "**.env**" per funzionare.

## Configurazione del bot

Per configurare il bot, vai nella [**console di
firebase**](https://console.firebase.google.com/u/0/project/botvalodatabase). Se non hai
accesso a firebase come editor, chiedi a [@EdoTM](https://github.com/EdoTM) o a [@giumanuz](https://github.com/giumanuz) di fornirtelo. Il bot usa
principalmente due servizi di firebase:

+ Il [firestore database](https://console.firebase.google.com/u/0/project/botvalodatabase/firestore/),
usato per i file di configurazione. **Non modificare file se non sai quello che stai
facendo.** Prima di modificare un file, nota come è strutturato e modificalo seguendo
quella struttura, altrimenti il bot potrebbe non funzionare correttamente.

+ Lo [storage](https://console.firebase.google.com/u/0/project/botvalodatabase/storage),
  che viene usato per le foto. Si trovano tutte dentro la cartella `images/categoria/`,
  dove `categoria` è una delle sottocartelle. **Attenzione:** il nome delle categorie
  (quindi, delle sottocartelle) deve corrispondere alle rispettive voci dentro il file
  `keyword_foto` nel firestore database. Se vuoi aggiungere categorie e non sai come fare,
  chiedi a [@EdoTM](https://github.com/EdoTM).
