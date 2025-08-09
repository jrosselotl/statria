import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_project import UserProject

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


def send_email_with_pdf(recipients: list[str], subject: str, body: str, pdf_file: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(recipients)
    msg.set_content(body)

    with open(pdf_file, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(pdf_file)
        )

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)


def get_admin_emails(db: Session, project_id: int) -> list[str]:
    admin_users = (
        db.query(User)
        .join(UserProject, User.id == UserProject.user_id)
        .filter(UserProject.project_id == project_id)
        .filter(User.role.in_(["admin", "project"]))
        .all()
    )

    emails = [u.email for u in admin_users if u.email and "@" in u.email]

    if "jrosselot@alancx.com" not in emails:
        emails.append("jrosselot@alancx.com")

    return emails
