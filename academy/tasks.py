from LMS.settings import EMAIL_RECIPIENT, EMAIL_SENDER, SENDGRID_KEY

from celery import shared_task

from django.template.loader import render_to_string

from sendgrid import Mail, SendGridAPIClient


@shared_task
def send_email(data):
    context = {
        'name': data['name'],
        'email': data['email'],
        'body': data['body']
    }
    content = render_to_string('emails/added_feedback.html', context)
    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=EMAIL_RECIPIENT,
        subject='Added new feedback',
        html_content=content
    )
    sg = SendGridAPIClient(SENDGRID_KEY)
    sg.send(message)
