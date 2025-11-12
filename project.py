import google.genai
import time
import PIL
import sys
import streamlit
from google.genai import types
client = google.client()
max_char=10000
aimodels=google.genai.models("gemini-2.5-flash")
imagemodels=google.genai.models("gemini-2.5-flash-image")
mathmodels=google.genai.models("gemini-2.5-flash")
def generative_teaching_ai():
    prompt_teach_input=streamlit.chat_input("Enter a prompt")
    response=client.models.generate.text(
        model=aimodels,
        prompt=prompt_teach_input,
        config=types.GenerateContentConfig()
    )
