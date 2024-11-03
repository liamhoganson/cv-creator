import os
from openai import OpenAI
from ..config import Config

class ChatGPT():
    '''
    Fetches AI generated resume summary
    '''
    def __init__(self, resume_data: dict):
        self.resume_data = resume_data
        self.client = OpenAI(api_key=Config.OPEN_AI_API_KEY)

    async def get_resume_summary(self):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": Config.PROMPT_ONE},
                {"role": "user", "content": f"Can you write me a professional resume summary given this data: {self.resume_data}"}
            ]
        )
        return response.choices[0].message.content

    async def edit_resume_attributes(self):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": Config.PROMPT_TWO},
                {"role": "user", "content": f"Can you transform this resume data: {self.resume_data}"}
            ]
        )
        return response.choices[0].message.content
