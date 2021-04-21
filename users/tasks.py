from LMS.settings import EMAIL_SENDER, SENDGRID_KEY

from celery import shared_task

from sendgrid import Mail, SendGridAPIClient


@shared_task
def send_activation_email(data):
    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=data['to_email'],
        subject=data['subject'],
        html_content=data['message']
    )
    sg = SendGridAPIClient(SENDGRID_KEY)
    sg.send(message)
