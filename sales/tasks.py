import os
import tempfile
import pdfkit
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template 


def generatePDf(context = {}):
    # Specify the path to the wkhtmltopdf executable
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

    # Render the HTML template to a string
    template = get_template('invoice/pdf_template.html')
    html = template.render(context)

    # Define the options for PDF generation
    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
    }

    # Generate the PDF using pdfkit and save it to a temporary file
    pdf_file_path = tempfile.mktemp(suffix='.pdf')
    pdfkit.from_string(html, pdf_file_path, configuration=config,  options=options)

    return pdf_file_path



def emailInvoiceClient(to_email, from_client, filepath):
    from_email = settings.EMAIL_HOST_USER
    subject = '[Skolo] Invoice Notification'
    body = """
    Good day,
    Please find attached invoice from {} for your immediate attention.
    regards,
    Skolo Online Learning
    """.format(from_client)

    message = EmailMessage(subject, body, from_email, [to_email])
    message.attach_file(filepath)
    message.send()