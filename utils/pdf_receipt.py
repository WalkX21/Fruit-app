from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO
from datetime import datetime

def create_receipt_pdf(order, total_price, discount):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(90 * mm, 200 * mm))
    c.translate(mm, mm)

    store_name = "MBMAGASIN"
    address = "01 place du Centre - 01234 MAVILLE "
    infos = "06 23 45 67 89 - contact@hiboutik.com"
    transaction_date = datetime.now().strftime("Le %d %B %Y  Ticket 001")

    c.setFont("Courier-Bold", 12)
    c.drawString(10 * mm, 190 * mm, store_name)
    c.setFont("Courier", 8)
    c.drawString(10 * mm, 185 * mm, address)
    c.drawString(10 * mm, 180 * mm, infos)
    c.drawString(10 * mm, 175 * mm, transaction_date)

    c.line(5 * mm, 170 * mm, 85 * mm, 170 * mm)

    c.drawString(10 * mm, 165 * mm, "Servi par: mohammed - #1")
    c.drawString(10 * mm, 160 * mm, "Client: mohammed - #2")

    c.line(5 * mm, 155 * mm, 85 * mm, 155 * mm)

    y_position = 150
    total_price = 0.0
    c.setFont("Courier", 8)
    for product in order:
        product_total = product['quantity'] * product['price']
        total_price += product_total
        text = f"{product['name']} - {product['quantity']} kg @ {product['price']} $/kg"
        c.drawString(10 * mm, y_position * mm, text)
        c.setFont('Courier-Bold', 10)
        c.drawRightString(82 * mm, y_position * mm, f"{product_total:.2f} $")
        c.setFont("Courier", 8)
        y_position -= 10
        if y_position < 10:
            c.showPage()
            y_position = 190
            c.setFont("Courier", 8)

    c.line(5 * mm, (y_position + 5) * mm, 85 * mm, (y_position + 5) * mm)

    c.setFont("Courier-Bold", 10)
    c.drawString(10 * mm, (y_position - 5) * mm, "TOTAL")
    c.drawRightString(82 * mm, (y_position - 5) * mm, f"{total_price:.2f} $")

    if discount > 0:
        c.line(5 * mm, (y_position - 10) * mm, 85 * mm, (y_position - 10) * mm)
        y_position -= 20
        c.setFont("Courier-Bold", 10)
        c.drawString(10 * mm, (y_position - 5) * mm, "DISCOUNT")
        c.drawRightString(82 * mm, (y_position - 5) * mm, f"-{discount:.2f} $")
        y_position -= 10
        c.line(5 * mm, (y_position - 10) * mm, 85 * mm, (y_position - 10) * mm)
        y_position -= 20
        final_total = total_price - discount
        c.setFont("Courier-Bold", 10)
        c.drawString(10 * mm, (y_position - 5) * mm, "FINAL TOTAL")
        c.drawRightString(82 * mm, (y_position - 5) * mm, f"{final_total:.2f} $")

    y_position -= 20
    c.line(5 * mm, (y_position - 10) * mm, 85 * mm, (y_position - 10) * mm)

    y_position -= 20
    c.setFont("Courier", 8)
    c.drawString(10 * mm, (y_position - 5) * mm, "Payé en ESP - TVA incluse")
    c.drawString(10 * mm, (y_position - 15) * mm, "Merci de votre visite. À bientôt!")

    y_position -= 20
    c.setFont("Courier", 6)
    footer_text = "Lun - Ven 11h00-14h00 / 15h00-19h00\nSamedi 11h00 - 19h30\nwww.mbm.com\nFR00123456789 - RCS PARIS B 123456789"
    for line in footer_text.split('\n'):
        y_position -= 5
        c.drawString(10 * mm, (y_position - 5) * mm, line)

    c.save()
    buffer.seek(0)
    return buffer
