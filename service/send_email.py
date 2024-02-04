import json
import os
import smtplib
import sys
from email.message import EmailMessage
from typing import List

from api.schemas import ShowUser
from settings import settings


def get_email_template(user: ShowUser) -> EmailMessage:
    email = EmailMessage()
    email["Subject"] = "Registration confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = user.email
    data_conf = user.config
    data = json.loads(data_conf)
    a=1
    email.set_content(
        f"<h1>Registration confirmation</h1>"
            f"<div>"
            f"<p>Username: {user.username}</p><br />"
            f"<p>Email: {user.email}</p><br />"
            f"<p>FIO: {json.loads(user.config)[0]['fio']}</p><br />"
            f"<p>Birthdate: {json.loads(user.config)[0]['birthday']}</p><br />"
            f"<p>TAGS: {json.loads(user.config)[0]['tags']}</p><br />"
            f"</div>",
        subtype="html",
    )
    return email


async def send_email(user: ShowUser) -> None:
    user_email = user.email
    email = get_email_template(user)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
