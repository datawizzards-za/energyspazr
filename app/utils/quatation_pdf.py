import time
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors


def generate_pdf(user_details):
    formatted_time = time.ctime()
    pdf_file_generate = user_details['first_name'] + \
                        user_details['last_name'] + str(formatted_time)
    slips_dir = 'app/static/app/slips/'
    document = SimpleDocTemplate(slips_dir + pdf_file_generate+".pdf",
                                 pagesize=letter,
                                 rightMargin=72, leftMargin=72,
                                 topMargin=72, bottomMargin=18)
    elements = []
    logo = "app/static/common/icon.png"

    address_parts = ["411 State St.", "Marshalltown, IA 50158"]

    image = Image(logo, 2 * inch, 2 * inch)
    elements.append(image)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    ptext = '<font size=12>%s</font>' % formatted_time

    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Create return address
    ptext = '<font size=12>%s</font>' % user_details['first_name']
    elements.append(Paragraph(ptext, styles["Normal"]))
    for part in address_parts:
        ptext = '<font size=12>%s</font>' % part.strip()
        elements.append(Paragraph(ptext, styles["Normal"]))

    elements.append(Spacer(1, 12))
    ptext = '<font size=12>Dear %s</font>' % user_details['first_name']
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(1, 12))
    ptext = '<font size=12>' \
            'The document quotation is provided for the item requested below ' \
            '</font>'

    elements.append(Paragraph(ptext, styles["Justify"]))
    elements.append(Spacer(1, 12))

    ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
    elements.append(Paragraph(ptext, styles["Justify"]))
    elements.append(Spacer(1, 12))

    ptext = '<font size=12>Sincerely,</font>'
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(1, 48))

    ptext = '<font size=16>Personal Details</font>'
    elements.append(Paragraph(ptext, styles["Center"]))
    elements.append(Spacer(1, 12))

    data = [['Email', user_details['username']],
            ['First Name', user_details['first_name']],
            ['Last Name', user_details['last_name']],
            ['Contact Number', user_details['contact_number']],
            ['Physical Address',
             user_details['physical_address'].replace(',', '\n')]]

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
    data = [['Intended Use', user_details['intended_use']],
            ['Need Finance', user_details['need_finance']],
            ['Site Visit', user_details['site_visit']],
            ['Include Instalation', user_details['include_installation']],
            ['Property Type', user_details['property_type']],
            ['Roof Inclination', user_details['roof_inclination']]
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
