### Piccole regolette che è meglio seguire

1. Prima di committare, **esegui sempre i test**. PyCharm lo può fare in automatico, se non sai come si fa chiedi a
   qualcuno. Anche GitHub ora lo fa da solo, e se questa immagine:
   [![BotValo](https://github.com/giumanuz/Bot_valo/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/giumanuz/Bot_valo/actions/workflows/python-app.yml)
   non dice "passing" in verde, controlla il codice perché ci sono errori.

2. Non fare il merge dal *dev* al *main* se ci sono altri branch attivi nel *dev*.

3. Se vuoi modificare il programma, fallo nel *dev* se esiste, o crea un branch da *dev*. Solo quando hai finito, e il
   programma funziona, fai il merge nel *dev*. Se non esiste *dev*, fai un branch dal *main* e quando hai fatto mergia
   nel *main*.
   **Non creare branch dal *main* se esiste *dev***, se non strettamente necessario.

4. In generale, non fare mai dei merge diretti di un branch se altre persone ci stanno lavorando sopra. Invece, crea
   una [**pull request**](https://github.com/giumanuz/Bot_valo/compare) e aspetta che gli altri abbiano finito di
   lavorarci.
