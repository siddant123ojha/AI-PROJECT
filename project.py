import google.genai
import time
import PIL
import sys
import streamlit


max_char=10000

def run_ai_teaching_assistant():
    streamlit.chat_input("Enter a prompt: ",key=teach_apikey, max_chars=max_char, accept_file=False)
    streamlit.rerun()

run_ai_teaching_assistant()