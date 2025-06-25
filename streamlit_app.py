import streamlit as st
import pandas as pd

from openai import OpenAI
from pathlib import Path
from datetime import datetime
import numpy as np

# Initialize OpenAI client with API key from secrets
client = OpenAI(api_key=st.secrets["open_ai"]["API_Key"])

st.title('The Bissellator')
bissell= str(Path(__file__).parent.parent/ "Data/bissell2009_extracted.txt")

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
