from google import genai
import time
from PIL import Image
from io import BytesIO
import sys
import streamlit
from google.genai import types
client = genai.Client(api_key="AIzaSyDCw5v7LPZ9ZbzPt1nwz6hQo98e8n0Tt7Q")
max_char=10000
max_outtokens=10000
max_intokens=100000
def generative_teaching_ai():
    prompt_teach_input=input("Enter a prompt: ")
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_teach_input,
        config=types.GenerateContent Config(temperature=0.1,max_output_tokens=max_outtokens)
    )
    print(response.text)
  
def generative_math_ai():
    while True:
        prompt_teach_input=input("Enter a math question: ")
        mathresponse=client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Explain with detail"+prompt_teach_input,
            config=types.GenerateContentConfig(temperature=0.1,max_output_tokens=max_outtokens)
    )
        print(mathresponse.text)

choose=input("Enter which model do you want to use:\n1.Ai teaching assistant\n2.Math Ai\n")
if choose=="1":
    generative_teaching_ai()
elif choose=="2":
    generative_math_ai()
else:
    print("please chooes one or 2")