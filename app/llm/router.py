import os
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

# Clients
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class LLMRouter:

    def gemini(self, prompt: str):

        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text


    def groq(self, prompt: str):

        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
            )

            return completion.choices[0].message.content

        except:
            # fallback if Groq fails
            return self.gemini(prompt)


router = LLMRouter()