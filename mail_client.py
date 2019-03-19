import ssl, smtplib
from email.message import EmailMessage
import textwrap

SMTP = "" # Change to SMTP provider of your choice.
SENDER_EMAIL = "" # Change this to your (sender) email.
PASSWORD = ""

class SMTPServer:
    def __init__(self):
        context = ssl.create_default_context()
        self.smtp_server = smtplib.SMTP(SMTP, port=587)
        self.smtp_server.starttls(context=context) # Encrypt connection using TLS.
        print("Logging into server as: " + SENDER_EMAIL)
        self.smtp_server.login(SENDER_EMAIL, PASSWORD)
        print("Logged in!")
    
    def send_grade(self, headers, num):
        msg = EmailMessage()
        content = textwrap.dedent("""\
                                  Hello {0},\n
                                  {1} Grade: {2}
                                  Feedback: {3}\n
                                  """.format(headers["First_Name"], num,
                                             headers[num],
                                             headers[num + "_Feedback"]))
        msg.set_content(content)

        msg['Subject'] = "[CSEE 3827] " + num + " Grade"
        msg['From'] = "CSEE 3827"
        msg['To'] = headers["Email"]
        self.smtp_server.send_message(msg)
    
    # TODO: Sending MIME messages and support for other email content.
    # TODO: Add space for sending a universal message to everyone about common mistakes.
