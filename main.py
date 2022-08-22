import os
import random
import smtplib
import datetime as dt


def get_today():
    now = dt.datetime.now()
    return now


def get_quote():
    with open('quotes.txt') as f:
        quotes_list = f.readlines()
    quote = random.choice(quotes_list)
    return quote


def send_email(content):
    EMAIL = os.getenv('email')
    PASSWORD = os.getenv('email_password')
    mailTo = os.getenv('emailTo')
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=120) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=mailTo, msg=content)


now = get_today()
if now.weekday() == 0:
    quote = get_quote()
    content = f'Subject: Monday Blue? Monday Motivation\n\n{quote}'
    print(content)
    send_email(content)
else:
    print('Normal day')


