import logging
from smtplib import SMTPServerDisconnected
import time

from celery.exceptions import MaxRetriesExceededError
from celery import shared_task
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="core.test_retryable_task",
    queue="default",
    default_retry_delay=5,
    retry_kwargs={"max_retries": 5},
)
def test_send_email_retry(self, recipient: str):
    """Sample send email task with retries error handled"""
    try:
        logger.info(f"Sending email to '{recipient}'...")
        time.sleep(5)
        send_mail(
            "Hello from {{cookiecutter.project_slug}}",
            "Welcome to out site, {{cookiecutter.project_slug}}!",
            "admin@example.com",
            [recipient],
            fail_silently=False,
        )
        logger.info("Email sent!")
    except SMTPServerDisconnected as e:
        try:
            self.retry(exc=e)
        except MaxRetriesExceededError:
            logger.info(f"Couldn't send email to '{recipient}'")


@shared_task(name="core.sample_default_task", queue="default")
def sample_default_priority_task():
    logger.info("This messages was printed from the Default priority queue...")
    return "Return value from the Default queue task 💚"


@shared_task(name="core.sample_low_priority_task", queue="low_priority")
def sample_low_priority_task():
    logger.info("This messages was printed from the Low Priority queue...")
    return "Return value from the Low Priority queue task 💜"


@shared_task(name="core.sample_high_priority_task", queue="high_priority")
def sample_high_priority_task():
    logger.info("This messages was printed from the High Priority queue...")
    return "Return value from the High Priority queue task 💛"


@shared_task(name="core.sample_scheduled_task", queue="low_priority")
def sample_scheduled_task():
    logger.info("Running scheduled task...")
    return "Return value from scheduled task ⏰"
