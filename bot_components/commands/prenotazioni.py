import json
from fpdf import FPDF

testo_dichiarazione = ""
with open("dichiarazione.json", 'r', encoding='UTF-8') as f:
    testo_dichiarazione = json.load(f)

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
