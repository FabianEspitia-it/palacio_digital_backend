import imaplib
import email
import re
import os

from email.header import decode_header


def get_code_email(user_email: str) -> str:

    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"), port=993)

    mail.login(os.getenv("DISNEY_EMAIL"), os.getenv("DISNEY_PASSWORD"))

    mail.select("inbox")

    status, messages = mail.search(
        None, f'(FROM "{user_email}")')

    if status == "OK":

        message_ids: list[str] = messages[0].split()

        if message_ids != []:

            status, message = mail.fetch(message_ids[-1], "(RFC822)")

            for response in message:

                if isinstance(response, tuple):

                    email_message = email.message_from_bytes(response[1])

                    subject, encoding = decode_header(
                        email_message["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(
                            encoding if encoding else "utf-8")

                    new_subject: str = subject.replace(" ", "").replace(
                        "FW:", "").replace("RV:", "").replace("هدایت:", "")

                    if ("Tu código de acceso único para Disney+".replace(" ", "") in new_subject) or ("Your one-time passcode for Disney+".replace(" ", "") in new_subject) or ("Votre code d'accès à usage unique pour Disney+".replace(" ", "") in new_subject) or ("Jednorazowy kod dostępu do Disney+".replace(" ", "") in new_subject) or ("Il tuo codice d'accesso temporaneo per Disney+".replace(" ", "") in new_subject) or ("Din engångskod till Disney+".replace(" ", "")) or ("Seu código de acesso único para o Disney+".replace(" ", "") in new_subject):

                        if email_message.is_multipart():
                            for part in email_message.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode(
                                        "utf-8", errors="ignore")
                        else:
                            body = email_message.get_payload(
                                decode=True).decode("utf-8", errors="ignore")

                        code = re.findall(r'(\d{6})(?:\s|\n|$)', body)

                        if code:
                            print(f"Código: {code[-1]}")
                            return code[-1]

        else:
            status, messages = mail.search(
                None, '(HEADER From "Disney+")')

            counter: int = 0

            if status == "OK":

                message_ids: list[str] = messages[0].split()

                for msg_id in message_ids[::-1]:

                    status, message = mail.fetch(msg_id, "(RFC822)")

                    if status == "OK":

                        for response in message:

                            if isinstance(response, tuple):

                                email_message = email.message_from_bytes(
                                    response[1])

                                to_email: str = email_message.get("To").lower(
                                ).strip().replace("<", "").replace(">", "")

                                if to_email != user_email.lower().strip():
                                    counter += 1

                                    if counter == 10:
                                        return None
                                    continue

                                subject, encoding = decode_header(
                                    email_message["Subject"])[0]
                                if isinstance(subject, bytes):
                                    subject = subject.decode(
                                        encoding if encoding else "utf-8")

                                new_subject: str = subject.replace(" ", "").replace(
                                    "FW:", "").replace("RV:", "").replace("هدایت:", "")

                                if ("Tu código de acceso único para Disney+".replace(" ", "") in new_subject) or ("Your one-time passcode for Disney+".replace(" ", "") in new_subject) or ("Votre code d'accès à usage unique pour Disney+".replace(" ", "") in new_subject) or ("Jednorazowy kod dostępu do Disney+".replace(" ", "") in new_subject) or ("Il tuo codice d'accesso temporaneo per Disney+".replace(" ", "") in new_subject) or ("Din engångskod till Disney+".replace(" ", "")) or ("Seu código de acesso único para o Disney+".replace(" ", "") in new_subject):

                                    if email_message.is_multipart():
                                        for part in email_message.walk():
                                            if part.get_content_type() == "text/plain":
                                                body = part.get_payload(decode=True).decode(
                                                    "utf-8", errors="ignore")
                                    else:
                                        body = email_message.get_payload(
                                            decode=True).decode("utf-8", errors="ignore")

                                    code = re.findall(
                                        r'(\d{6})(?:\s|\n|$)', body)

                                    if code:
                                        print(f"Código: {code[-1]}")
                                        return code[-1]

    mail.close()
