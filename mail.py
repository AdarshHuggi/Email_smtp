import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
from dotenv import load_dotenv

import os
from log import logger
# Load environment variables
load_dotenv()

class EmailAlert:
    def __init__(self):
        # Securely fetch environment variables
        self.host = os.getenv("EMAIL_HOST")
        self.port = int(os.getenv("PORT"))
        self.username = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        
        
    
    
    def send_email(self, to_email, subject, message_body):

        print(self.host,self.port,self.username,self.password)
        """
        Sends an email using SMTP with SSL encryption.
        
        Args:
            to_email (str): Recipient email address.
            subject (str): Subject of the email.
            message_body (str): Body content of the email.
        
        Returns:
            None
        """
        try:
            # Set up the message
            message = MIMEMultipart()
            message["From"] = self.username
            message["To"] = to_email
            message["Subject"] = subject

            # Attach the message body
            message.attach(MIMEText(message_body, "plain"))

            # Secure SSL context
            context = ssl.create_default_context()
      

            # Connect to the server and send email
            with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
                server.login(self.username, self.password)
                server.sendmail(self.username, to_email, message.as_string())

            print("Email sent successfully")
            logger.info(f"Email sent successfully to {to_email}")

        except Exception as e:
            logger.error(f"Error occurred: {e}")
            print(f"Error occurred: {e}")





to_email="aaa.r.huggi@gmail.com"
subject="Test Email from Gmail"
message_body="""
Hi.

This is the Test Email to check the python script

Please ignore this email

Thanks 
Python app

"""



if __name__ == "__main__":
    
    email_alert = EmailAlert()
    email_alert.send_email(to_email,subject,message_body)







