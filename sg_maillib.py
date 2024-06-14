# -*- coding: utf-8 -*-
"""Send email via smtp_host."""
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import string
import random

from dotenv import load_dotenv


load_dotenv()


class SG_mail:
    """Class for e-mail """

    def send_email(self, subject, to_addr, body_text):

        smtp_host = os.getenv('SMPT_HOST')
        login = os.getenv('LOGIN')
        password = os.getenv('MAIL_PASSWORD')

        msg = MIMEText(body_text, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = login
        msg['To'] = to_addr


        s = smtplib.SMTP_SSL(smtp_host)
        s.set_debuglevel(1)
        try:
            s.login(login, password)
            s.sendmail(login, to_addr, msg.as_string())
        finally:
            print(msg)
            s.quit()

    def generate_unique_id(self, length):
        characters = string.ascii_letters + string.digits
        unique_id = ''.join(random.choice(characters) for _ in range(length))
        return unique_id.lower()


#m=SG_mail()
#m.send_email("Profitomer.ru - Регистрация v0.2t","admin@shilgen.ru", "Код активации ")
