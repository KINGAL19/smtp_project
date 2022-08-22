import os
import random
import smtplib
import datetime as dt
import pandas as pd


def find_match_data(now, match_list):
    df = pd.read_csv('birthdays.csv')
    df_dict_list = df.to_dict(orient='records')
    for dict in df_dict_list:
        month = dict['month']
        day = dict['day']
        if now.month == month:
            if now.day == day:
                match_list.append(dict)


def write_letter(match_list, REPLACE_HOLDER):
    for match_dict in match_list:
        num = random.randint(1, 3)
        with open(f'letter_templates/letter_{num}.txt') as f:
            content = f.read()
            new_content = content.replace(REPLACE_HOLDER, match_dict['name'])
            match_dict['content'] = new_content


def send_email(match_dict):
    EMAIL = os.getenv('email')
    PASSWORD = os.getenv('email_password')
    mailTo = match_dict['email']
    content = f"Subject: Happy birthday! {match_dict['name']}\n\n{match_dict['content']}"
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=mailTo, msg=content)

def main():
    now = dt.datetime.now()
    REPLACE_HOLDER = '[NAME]'
    match_list = []

    find_match_data(now, match_list)
    write_letter(match_list, REPLACE_HOLDER)
    print(match_list)
    for match_dict in match_list:
        send_email(match_dict)


if __name__ == "__main__":
    main()
