from logging import getLogger
import smtplib
from email.message import EmailMessage

from api.schemas import ShowUser
from settings import settings

LOGGER = getLogger(__name__)


def get_email_template(user: ShowUser) -> EmailMessage:
    """Producing email_template to user"""
    # LOGGER.info(f"get_email_template for {user.dict()=}")
    email = EmailMessage()
    email["Subject"] = "Registration confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = user.email
    email.set_content(
        f"<h1>Registration confirmation</h1>"
        f"<div>"
        f"<p>Username: {user.username}</p><br />"
        f"<p>Email: {user.email}</p><br />"
        f"<p>FIO: {user.config['fio']}</p><br />"
        f"<p>Birthdate: {user.config['birthday']}</p><br />"
        f"<p>TAGS: {user.config['tags']}</p><br />"
        f"</div>",
        subtype="html",
    )
    return email


async def send_email(user: ShowUser) -> None:
    """Sending email to user"""
    # LOGGER.info(f"send_email for {user.dict()=}")
    email = get_email_template(user)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
