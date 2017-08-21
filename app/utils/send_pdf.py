from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class TransactionVerification:
    """Lets user verify the flagged transaction as a precaution and
    attempt to successfully identify fraudulent transactions.
    Attributes:
        data (dict): transaction data.

    """

    def __init__(self, data, uuid, order_number):
        """Initialise transaction verification object with transaction
        data.

        Args:
            data (dict): transaction data.
        Returns:
            Void.

        """

        self.data = data
        self.uuid = uuid
        self.order_number = order_number

    def send_verification_mail(self):
        """Given transaction data, send the user verification email to
        let them acknowledge the fraud while also verifying whether or
        not the transaction is fraudulent.

        Args:
            None.

        Returns (Boolean):
            State of the mail sending; true when sent successfully,
            otherwise false.
        """

        subject = 'EnergySpazr Quotation(s) \
                   '
        from_email = settings.EMAIL_HOST_USER
        to = self.data['email']
        text_content = 'Please find the attached quotation(s).'
        html_content = '''<p>Kind Regards.\n EnergySpazr</p>'''

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        if self.order_number == '4':
            msg.attach_file('app/static/app/slips/' + self.uuid + '_' +
                            str(2) + '.pdf')
            msg.attach_file('app/static/app/slips/' + self.uuid + '_' +
                            str(2) + '.pdf')
            msg.attach_file('app/static/app/slips/' + self.uuid + '_' +
                            str(3) + '.pdf')
        else:
            msg.attach_file('app/static/app/slips/' + self.uuid + '_' +
                        str(self.order_number) + '.pdf')
        msg.send()
