import time
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from app.utils import pricing
from app import models


def generate_pdf(client, system):
    best_three_prices, products, supplier = pricing.QuotationCharges(
        [3, 4]).get_prices()
    status_response = 2
    formatted_time = time.ctime()
    try:
        for i in range(3):
            pdf_file_generate = str(system.order_number)
            slips_dir = 'app/static/app/slips/'
            document = SimpleDocTemplate(slips_dir +
                                         pdf_file_generate +
                                         "_" + str(i) + ".pdf",
                                         pagesize=letter,
                                         rightMargin=72, leftMargin=72,
                                         topMargin=72, bottomMargin=18)
            elements = []
            logo = "app/static/common/icon.png"

            image = Image(logo, 2 * inch, 2 * inch)
            elements.append(image)

            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
            styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
            styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

            ptext = '<font size=12>%s</font>' % formatted_time

            elements.append(Paragraph(ptext, styles["Right"]))
            elements.append(Spacer(1, 12))

            ptext = '<font size=12>Dear %s</font>' % client.firstname.capitalize()
            elements.append(Paragraph(ptext, styles["Normal"]))
            elements.append(Spacer(1, 12))
            ptext = '<font size=12>' \
                    'The document quotation is provided for the item requested below ' \
                    '</font>'

            elements.append(Paragraph(ptext, styles["Justify"]))
            elements.append(Spacer(1, 12))

            ptext = '<font size=12>Thank you very much and we look forward to ' \
                    'serving you.</font>'

            elements.append(Paragraph(ptext, styles["Justify"]))
            elements.append(Spacer(1, 12))

            ptext = '<font size=12>Sincerely,</font>'
            elements.append(Paragraph(ptext, styles["Normal"]))
            elements.append(Spacer(1, 48))

            ptext = '<font size=16>Personal Details</font>'
            elements.append(Paragraph(ptext, styles["Center"]))
            elements.append(Spacer(1, 12))

            data = [['Email', client.username.upper()],
                    ['First Name', client.firstname.upper()],
                    ['Last Name', client.lastname.upper()],
                    ['Contact Number', client.contact_number.upper()],
                    ['Physical Address',
                     client.physical_address.building_name.upper() + '\n' +
                     client.physical_address.street_name.upper() + '\n' +
                     client.physical_address.city.upper() + '\n' +
                     client.physical_address.suburb.upper() + '\n' +
                     str(client.physical_address.zip_code)]]

            table = Table(data, colWidths=190)
            table.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 24))
            ptext = '<font size=16 style="text-transform:uppercase">System ' \
                    'Details</font></center>'
            elements.append(Paragraph(ptext, styles["Center"]))
            elements.append(Spacer(1, 12))
            data = [['Order number', str(system.order_number).upper()],
                    #['Intended Use',
                    # order.intended_use.upper().replace('_', ' ')],
                    ['Need Finance', str(system.need_finance).upper()],
                    #['Site Visit', str(order.site_visit).upper()],
                    ['Include Instalation', str(
                        system.include_installation).upper()],
                    #['Property Type', order.property_type.upper()],
                    #['Roof Inclination', order.roof_inclination.upper()],
                    ]

            table = Table(data, colWidths=190)
            table.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 24))

            product_count = 0
            for product in products:
                data = []
                ptext = '<font size=16 style="text-transform:uppercase">Supplier ' \
                        'Details</font></center>'
                elements.append(Paragraph(ptext, styles["Center"]))
                elements.append(Spacer(1, 12))
                data.append(['Company Name', str(supplier[product][
                    product_count].company_name).upper()])
                data.append(['Contact Number', str(supplier[product][
                    product_count].contact_number).upper()])
                data.append(['Web Address',
                             str(supplier[product][product_count].web_address).upper()])

                table = Table(data, colWidths=190)
                table.setStyle(TableStyle([
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ]))

                elements.append(table)
                elements.append(Spacer(1, 24))

                elements.append(Spacer(1, 24))
                ptext = '<font size=16 style="text-transform:uppercase">Charges ' \
                        '</font></center>'
                elements.append(Paragraph(ptext, styles["Center"]))
                elements.append(Spacer(1, 12))
                data_ = []
                try:
                    data_.append(['Amount ', 'R' + str(best_three_prices[
                        product][product_count]
                        .price).upper()])
                    data_.append(['Items ', str(product).upper()])
                except:
                    data_.append(['Amount ', 'Not Available '])
                    data_.append(['Items ', str(product).upper()])
                product_count += 1
                table = Table(data_, colWidths=190)
                table.setStyle(TableStyle([
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ]))

            elements.append(table)
            elements.append(Spacer(1, 24))

            ptext = '<font size=12> Powered by \
                     <a href="http://www.itechhub.co.za" color="blue">iTechHub</a>\
                     </font>'

            elements.append(Paragraph(ptext, styles["Center"]))

            document.build(elements)
            status_response = 1
    except:
        print("No Prices Available from Suppliers")

    return pdf_file_generate, status_response
