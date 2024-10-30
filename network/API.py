import os
from openai import OpenAI
from ..site.payload_sanitizer import PayloadSanitizer
from ..config import Config

##TODO: Make this async
class ChatGPT():
    '''
    Fetches AI generated resume summary
    '''
    def __init__(self):
        self.resume_data = PayloadSanitizer.convert_session_to_payload()
        self.client = OpenAI(api_key=Config.OPEN_AI_API_KEY)

    def get_resume_summary(self):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You will be provided with user submitted resume data in JSON format (e.g. job, education, skills, attributes, etc.), and your task is to write a user summary given the data in the POV of the user without embelishing anything. Write it as though its an acutal well-written resume summary. Not in JSON format."},
                {"role": "user", "content": f"Can you write me a professional resume summary given this data: {self.resume_data}"}
            ]
        )
        return response
