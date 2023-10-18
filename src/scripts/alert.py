import itertools
import logging
import smtplib
import threading
import time
from email.message import EmailMessage


def send_alert(name, email, school, programme, cumulative_gpa, gpa):
    sender = 'academicprobationsystem2023@gmail.com'
    password = 'eulp fsbb dore qhza'

    message = EmailMessage()
    message['Subject'] = 'Alert: You are on Academic Probation'
    message['From'] = f'{sender}'
    message['To'] = f'{sender}'
    message.set_content(f"""
        Email: {email}
        Programme: {programme}
        School: {school}

        Dear {name},
    
        We hope this message finds you well. This email is to inform you that your recent GPA [{cumulative_gpa}]
        has fallen below the required threshold [{gpa}] and you are now on academic probation.
    
        Academic probation is a serious matter. It is a signal that you may need to make significant changes to meet 
        the academic standards required to continue at our institution. However, it's important to remember that this 
        is not a permanent status, and many students have successfully returned to good standing after a period of 
        probation.
    
        Here are some steps you can take:
        
        1. Meet with your academic advisor: They can provide guidance on course selection, study strategies, 
        and connecting with campus resources. 
        
        2. Utilize campus resources: This includes tutoring centers, writing workshops, and counseling services. 
        
        3. Reflect on your habits: Consider if changes need to be made in your study habits, time management, 
        or course load.
        
        Remember, this is a time for action and improvement. It's important to take advantage of the resources 
        available to you and to communicate regularly with your advisor.
        
        Please do not hesitate to reach out if you have any questions or need further clarification about the 
        implications of being on academic probation.
        
        Best,
        Academic Probation System
        University of Technology, Jamaica
    """)

    done = [False]
    t = threading.Thread(target=animate, args=(done,))
    t.start()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(message)
        server.quit()

        done[0] = True
        t.join()  # Wait for the animation thread to finish

        print(f'\rAlert sent to {email}', flush=True)
        logging.info(f'Alert sent to {email}')
    except Exception as e:
        logging.error(f'Error sending alert: {e}')


def animate(done):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done[0]:
            break
        print('\rSending alert... ' + c, end='', flush=True)
        time.sleep(0.1)
