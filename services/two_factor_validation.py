import smtplib
from email.message import EmailMessage
import random

def send_email(recipient, subject, body, sender='email.sender.t2024@gmail.com', sender_password='pqji lvha ckvo fehu', smtp_server='smtp.gmail.com', smtp_port=587) -> bool:
    """
    Sends a standard email from a sender to a recipient.

    :param sender: The email address of the sender.
    :param recipient: The email address of the recipient.
    :param subject: The subject of the email.
    :param body: The body of the email.
    :param sender_password: The password for the sender's email.
    :param smtp_server: The SMTP server to be used (default is smtp.gmail.com).
    :param smtp_port: The port of the SMTP server (default is 587).
    """
    # Creates an EmailMessage instance
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Connects to the SMTP server and sends the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Initiates TLS
            server.login(sender, sender_password)  # Login
            server.send_message(msg)  # Sends the message
            print("E-mail sent successfully!")
            return True
    except Exception as e:
        print(f"Error sending e-mail: {e}")
        return False

def generate_secret_code():
    """
    Generates a 6-digit secret authentication code.
    
    Returns:
        str: A 6-digit code.
    """
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return code

# Exemplo de uso
'''secret_code = generate_secret_code()
message_body = f'Insira este código de 6 dígitos para confirmar que é você.\n{secret_code}\nSe você não solicitou este código nas configurações, ignore esta mensagem'

send_email('recipient_email@example.com', 
           'Assunto do E-mail', 
           secret_code)'''