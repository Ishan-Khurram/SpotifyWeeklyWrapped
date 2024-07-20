import google.generativeai as genai
import os


class Gemini:

    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_response(self, prompt):
        response = self.model.generate_content(prompt)
        return response
