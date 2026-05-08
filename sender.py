import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

def send_email(to_email, body, config):
    msg = EmailMessage()
    msg["From"] = config.EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = "Software Developer – Profile Submission"

    msg.set_content(body)

    with open(config.RESUME_PATH, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=Path(config.RESUME_PATH).name,
        )

    context = ssl.create_default_context()

    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(config.EMAIL_ADDRESS, config.EMAIL_APP_PASSWORD)
        server.send_message(msg)
