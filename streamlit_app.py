import streamlit as st
import pandas as pd

from openai import OpenAI
from pathlib import Path
from datetime import datetime
import numpy as np

# Initialize OpenAI client with API key from secrets
client = OpenAI(api_key=st.secrets["open_ai"]["API_Key"])

st.title('The Bissellator')
bissell= str(Path(__file__).parent/"bissell2009_extracted.txt")

# Upload dataset
lost_object=st.text_input("Specify a lost item","a shitty old sock")
with open(bissell, "r", encoding="utf-8") as f:
    bissell_text = f.read()

# Button to start generating text
if st.button('Click to Bissellate'):

    prompt = (
        f"In the style of academic writing found in the text in {bissell_text}  "
        f"write a descriptive and florid paragraph about:\n\n"
        f"{lost_object}\n\n"
                )

        # Call the OpenAI API
    response = client.chat.completions.with_raw_response.create(model="gpt-4o-mini", messages=[{"role": "system", "content": "You are a human geographer"},{"role": "user", "content": prompt}])
    completion=response.parse()
    #print(completion.choices[0].message)
    st.write("Bissellwords:")
    st.markdown(completion.choices[0].message.content)
else:
    st.write("Don't be scared.")
import os
import requests
from bs4 import BeautifulSoup

def fetch_and_save_first_image(query: str, outfile: str):
    url = "https://www.google.com/search"
    params = {"q": query, "tbm": "isch"}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    # Skip the first <img> (logo), grab the next real one
    img_tags = soup.find_all("img")
    for img in img_tags:
        src = img.get("src")
        if src and src.startswith("http"):
            img_url = src
            break
    else:
        raise RuntimeError("No valid image found")

    img_data = requests.get(img_url).content
    os.makedirs(os.path.dirname(outfile) or ".", exist_ok=True)
    with open(outfile, "wb") as f:
        f.write(img_data)
    print(f"Saved first image to {outfile}")


 fetch_and_save_first_image(lost_object, "first_image.jpg")
 st.image("first_image.jpg")
    