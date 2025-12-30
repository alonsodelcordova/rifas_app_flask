from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from datetime import datetime
import os

def generate_raffle_pdf(raffle, winner, user, number):
    filename = f"acta_sorteo_rifa_{raffle.id}.pdf"
    path = os.path.join("static/pdfs", filename)

    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>ACTA DE SORTEO</b>", styles["Title"]))
    story.append(Spacer(1, 1 * cm))

    story.append(Paragraph(f"<b>Rifa:</b> {raffle.title}", styles["Normal"]))
    story.append(Paragraph(f"<b>Número ganador:</b> {number.number}", styles["Normal"]))
    story.append(Paragraph(f"<b>Ganador:</b> {user.name}", styles["Normal"]))
    story.append(Paragraph(
        f"<b>Fecha del sorteo:</b> {winner.drawn_at.strftime('%d/%m/%Y %H:%M')}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("<b>Seed del sorteo</b>", styles["Heading2"]))
    story.append(Paragraph(winner.seed, styles["Code"]))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "El sorteo fue realizado de forma aleatoria y transparente "
        "utilizando un algoritmo reproducible basado en una seed verificable.",
        styles["Normal"]
    ))

    doc.build(story)

    return filename
