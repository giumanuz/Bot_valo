import json
import os
import random

import qrcode
from fpdf import FPDF

with open("dichiarazione.json", 'r', encoding='UTF-8') as f:
    testo_dichiarazione = json.load(f)

with open("frasi.json", 'r', encoding='UTF-8') as f:
    settings = json.load(f)

color = settings["color"]
size = settings["size"]
texts = settings["texts"]


def pdf_main():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B")

    qr = qrcode.make('1936736' + "," + "10/03/2022" + ",RM02" + "1")
    type(qr)
    num=str(random.randint(1, 10000))
    qr.save(f'{num}.png')

    pdf.image(f'{num}.png', x=80, y=10, w=60, h=60)
    os.remove(f'{num}.png')
    pdf.cell(0, 70, ln=1)

    for riga in texts:
        aggiungi_riga(pdf, riga)

    pdf.output(f'{num}.pdf')


def aggiungi_riga(pdf: FPDF, riga: str):
    for i in range(len(riga)):
        blocchetto = riga[i]
        pdf.set_font("Arial", "B", size=size[blocchetto["size"]])

        colore = color[blocchetto["color"]]
        pdf.set_text_color(colore[0], colore[1], colore[2])

        testo = blocchetto["text"]

        if testo == "{dichiarazione}":
            for pezzo in testo_dichiarazione:
                pdf.multi_cell(0, 6, pezzo, 0)
                pdf.cell(0, 4, "", ln=1)
            continue

        testo = str.format(testo,
                           nome="Edoardo Fiocchi",
                           matricola="1939007",
                           giorno="12/12/2001",
                           aula="A6",
                           edificio="1",
                           via="ariosto",
                           collocazione="circonvallazione",
                           inizio="12",
                           fine="15")

        ln = 0
        if i == len(riga) - 1:
            ln = 1

        pdf.cell(pdf.get_string_width(testo), 8, testo, ln=ln)


if __name__ == '__main__':
    pdf_main()
