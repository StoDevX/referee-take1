"""Sends an email"""

import smtplib
from io import StringIO
from email.mime.text import MIMEText

TO_ADDR = 'hawkrives@gmail.com'

def send(msg):
    with smtplib.SMTP_SSL('smtp.gmail.com') as smtp:
        smtp.login(username, password)
        smtp.sendmail('rives@stolaf.edu', TO_ADDR, msg)
    print('mail sent')

def make_email():
    text = 'Test message'
    with StringIO(text) as fp:
        msg = MIMEText(fp.read())
    msg['To'] = TO_ADDR
    msg['From'] = 'rives@stolaf.edu'
    msg['Subject'] = 'A subject'
    return msg

def send_email():
    msg = make_email()
    print(msg)
    send(msg)
