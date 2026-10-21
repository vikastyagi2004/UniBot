import os
from dotenv import load_dotenv
from groq import Groq
 
load_dotenv()  # reads GROQ_API_KEY from the .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "user", "content": "Say hello to the ai Odyssey class!"}
    ],
)
 
print(response.choices[0].message.content)
