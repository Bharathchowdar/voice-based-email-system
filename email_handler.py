import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = 587


class EmailHandler:
    def __init__(self):
        self.email = EMAIL
        self.password = PASSWORD
        self._inbox_cache = []

    def _connect_imap(self):
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(self.email, self.password)
        return mail

    def fetch_inbox(self, limit: int = 10):
        """Fetch latest emails from inbox."""
        try:
            mail = self._connect_imap()
            mail.select("inbox")
            _, data = mail.search(None, "ALL")
            mail_ids = data[0].split()
            latest_ids = mail_ids[-limit:][::-1]

            emails = []
            for mail_id in latest_ids:
                _, msg_data = mail.fetch(mail_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                body = ""
                attachments = []

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode(errors='ignore')
                        elif content_type.startswith("image/"):
                            attachments.append({
                                'type': content_type,
                                'data': part.get_payload(decode=True)
                            })
                else:
                    body = msg.get_payload(decode=True).decode(errors='ignore')

                emails.append({
                    'id': mail_id.decode(),
                    'from': msg.get('From', ''),
                    'subject': msg.get('Subject', '(No Subject)'),
                    'date': msg.get('Date', ''),
                    'body': body.strip(),
                    'attachments': attachments
                })

            self._inbox_cache = emails
            mail.logout()
            return emails

        except Exception as e:
            print(f"[IMAP Error]: {e}")
            return []

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email via SMTP."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"[SMTP Error]: {e}")
            return False

    def delete_email(self, email_id: int) -> bool:
        """Delete an email by index from cached inbox."""
        try:
            if email_id >= len(self._inbox_cache):
                return False
            mail_id = self._inbox_cache[email_id]['id']
            mail = self._connect_imap()
            mail.select("inbox")
            mail.store(mail_id, '+FLAGS', '\\Deleted')
            mail.expunge()
            mail.logout()
            self._inbox_cache.pop(email_id)
            return True
        except Exception as e:
            print(f"[Delete Error]: {e}")
            return False
