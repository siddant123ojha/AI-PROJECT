import google.genai
import time
import PIL
import sys
import streamlit

image_apikey = "AIzaSyBGOh41L0O11ySl2u6MfCqQnqxIkbYVSVw"
math_apikey = "AIzaSyDcR4OiRTIDWYNOJBReoovm4RsJKSs_6qY"
teach_apikey="AIzaSyDCw5v7LPZ9ZbzPt1nwz6hQo98e8n0Tt7Q"
max_char=10000

def run_ai_teaching_assistant():
    streamlit.chat_input("Enter a prompt: ",key=teach_apikey, max_chars=max_char, accept_file=False)
    streamlit.rerun()

run_ai_teaching_assistant()