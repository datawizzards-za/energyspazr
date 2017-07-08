import time
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors


def generate_pdf(client, order, address, system, suppliers):

    formatted_time = time.ctime()
    pdf_file_generate = client.firstname + \
                        client.lastname + \
                        str(formatted_time).replace(' ','').replace(':','')

    slips_dir = 'app/static/app/slips/'
    document = SimpleDocTemplate(slips_dir + pdf_file_generate+".pdf",
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

    ptext = '<font size=12>Dear %s</font>' % client.firstname
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
             address.building_name.upper() + '\n' +
             address.street_name.upper() + '\n' +
             address.city.upper() + '\n' +
             address.suburb.upper() + '\n' +
             str(address.zip_code)]]

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
    data = [['Intended Use',
             order.intended_use.upper().replace('_', ' ')],
            ['Need Finance', str(system.need_finance).upper()],
            ['Site Visit', str(order.site_visit).upper()],
            ['Include Instalation',
             str(system.include_installation).upper()],
            ['Property Type', order.property_type.upper()],
            ['Roof Inclination', order.roof_inclination.upper()],
            ]

    table = Table(data, colWidths=190)
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

    return pdf_file_generate



    # if __name__ == '__main__':
    #     values = {'username': 'ofentswel@gmail.com',
    #               'first_name': 'Ofentswe',
    #               'last_name': 'Lebogo',
    #               'intended_use': 'main_power',
    #               'physical_address': '406 City Place, 111 WF Nkomo, Pretoria, 0002',
    #               'roof_inclination': 'tilted',
    #               'contact_number': '0715795960',
    #               'site_visit': 'yes',
    #               'need_finance': 'yes',
    #               'property_type': 'flat',
    #               'place_order': 'FINISH',
    #               'include_installation': 'yes'}
    #     generate_pdf(values)
