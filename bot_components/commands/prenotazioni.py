from fpdf import FPDF


def pdf_main():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(130, 56, 31)
    pdf.cell(200, 10, txt="Prenotazioni aule per ESAME - ricevuta di prenotazione", ln=1, align="L")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="FIOCCHI EDOARDO", ln=1, align="L")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt="matr.1934851", ln=1, align="L")

    cellMultiColorName = (
        {
            'text': 'EDOARDO FIOCCHI',
            'color': [0, 0, 0],
            'font': {
                'tema': "Arial",
                'style': "B",
                'size': 12
            }
        },
        {
            'text': 'matr.1943520',
            'color': [0, 0, 0],
            'font': {
                'tema' : "Arial",
                'style': "B",
                'size' : 11
            }
        }
    )

    currentPointerPosition = 0
    for diz in cellMultiColorName:
        pdf.set_x(currentPointerPosition)
        pdf.set_font(diz["font"]["tema"], style=diz["font"]["style"], size=diz["font"]["size"],)
        pdf.set_text_color(diz["color"][0], diz["color"][1], diz["color"][2])
        size = pdf.get_string_width(diz["text"])
        pdf.cell(size, 10, diz["text"])
        currentPointerPosition += size + 1

    # Prenotazioni aule per ESAME - ricevuta di prenotazione
    # 130 56 31  rosso scuro

    # Date rosso chiaro
    # 255 0 0

    # blu
    # 0 0 255

    # blu scuro
    # 17 85 204

    pdf.output("python.pdf")


if __name__ == '__main__':
    pdf_main()
