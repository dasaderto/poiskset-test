from typing import List

from django.core.mail import EmailMultiAlternatives

from testDotaDjango.celery import celery_app


@celery_app.task
def html_email_sender(subject: str, content: str, html_content, message_from: str, emails: List[str], **kwargs):
    email = EmailMultiAlternatives(subject=subject, body=content, from_email=message_from, to=emails)
    email.attach_alternative(html_content, "text/html")
    email.send()
    return True
