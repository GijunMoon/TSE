import google.generativeai as genai

class GeminiAI:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # 사용하는 모델명은 상황에 따라 변경 가능

    def generate_story(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text