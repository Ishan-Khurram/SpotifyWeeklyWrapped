import google.generativeai as genai
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Gemini:

    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_response(self, prompt):
        response = self.model.generate_content(prompt)
        return response

    def send_email(self, subject, body, sender_email, receiver_email, password):
        # Create a multipart message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "html"))

        # Create SMTP session for sending the mail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Enable security
            server.login(sender_email, password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)

    def extract_response_dict(self, response):
        return {
            "candidates": [{
                "content": {
                    "parts": [{"text": response.text}],
                    "role": "model"
                }
            }]}

    def generate_and_extract(self, prompt):
        response = self.generate_response(prompt)
        return self.extract_response_dict(response)
