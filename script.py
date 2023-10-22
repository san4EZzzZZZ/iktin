from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Устанавливаем шрифт Arial
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))


# Функция для создания PDF-документа
def create_pdf(filename, data):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    # Создаем таблицу с данными
    table_data = []
    table_data.append(["Режим отправки", data[0]])
    table_data.append(["Количество мест", data[1]])
    table_data.append(["Описание вложений", data[2]])
    table_data.append(["Габариты вложений (ДxШxВ, см)", data[3]])
    table_data.append(["Вес каждого места (кг)", data[4]])
    table_data.append(["Стоимость вложения (общая)", data[5]])
    table_data.append(["Стоимость вложения (по местам)", data[6]])
    table_data.append(["Точный адрес отправки", data[7]])
    table_data.append(["Точный адрес доставки", data[8]])
    table_data.append(["Способ оплаты", data[9]])

    table = Table(table_data, colWidths=6 * cm, rowHeights=0.6 * cm)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    story.append(table)

    doc.build(story)


# Считываем данные от пользователя
data = []
data.append(input("Режим отправки (дверь-дверь / склад-склад / склад-дверь / дверь-склад): "))
data.append(input("Количество мест: "))
data.append(input("Описание вложений: "))
data.append(input("Габариты вложений (ДxШxВ, см): "))
data.append(input("Вес каждого места (кг): "))
data.append(input("Стоимость вложения (общая): "))
data.append(input("Стоимость вложения (по местам): "))
data.append(input("Точный адрес отправки: "))
data.append(input("Точный адрес доставки: "))
data.append(input("Способ оплаты (Оплата получателем / Отправителем по договору): "))

# Создаем PDF-документ
create_pdf("tovarnaya_nakladnaya.pdf", data)

print("Товарная накладная успешно создана в файле tovarnaya_nakladnaya.pdf")
