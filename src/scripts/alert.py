import smtplib


def send_alert(programme, school):
    sender = 'academicprobation2023@gmail.com'
    receiver = ['2023@gmail.com', '@gmail.com']
    password = ''
    subject = f'GPA below or equal to default GPA'
    body = (f'Programme: {programme}\n'
            f'School: {school}')

    message = f"""From: {sender}
To: {receiver}
Subject: {subject}

{body}
"""

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
        server.quit()
        print(f'\033[32mAlert sent to {receiver}\033[0m')
    except Exception as e:
        print(f'\033[91mError sending alert: {e}\033[0m')
