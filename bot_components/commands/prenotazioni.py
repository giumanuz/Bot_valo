import json
import string

from fpdf import FPDF

testo_dichiarazione = open("dichiarazione.txt", "r").read()

settings = None
with open("frasi.json", 'r', encoding='UTF-8') as f:
    settings = json.load(f)

color = settings["color"]
size = settings["size"]
texts = settings["texts"]


def pdf_main():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B")

    for riga in texts:
        aggiungi_riga(pdf, riga)

    pdf.output("prenotazione.pdf")


def aggiungi_riga(pdf: FPDF, riga: str):
    current_pointer_position = 200
    for blocchetto in riga:
        pdf.set_x(current_pointer_position)
        pdf.set_font("Arial", size=size[blocchetto["size"]])

        colore = color[blocchetto["color"]]
        pdf.set_text_color(colore[0], colore[1], colore[2])
        lunghezza_blocco = pdf.get_string_width(blocchetto["text"])

        testo = blocchetto["text"]
        # testo = str.format(testo, )

        pdf.cell(lunghezza_blocco, 10, testo)
        current_pointer_position += lunghezza_blocco + 1


if __name__ == '__main__':
    pdf_main()
