import google.genai
import time
import PIL
import sys
from secrets import image_apikey
from secrets import math_apikey
from secrets import teach_apikey
import streamlit
image_key=google.genai.Client(image_apikey)
math_apikey=google.genai.Client(math_apikey)
teach_apikey=google.genai.Client(teach_apikey)

max_char=10000

def generative_teaching_ai():
    google.genai.models("gemini-2.5-flash")
    
def run_ai_teaching_assistant():
    streamlit.title("📖Ai teaching assistant")
    streamlit.container(border=True, width="stretch",height="content")
    streamlit.chat_input("Enter your message", max_char=max_char,accept_file=False)
    streamlit.button("Send")
    
run_ai_teaching_assistant()