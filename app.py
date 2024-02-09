### Food Healthiness App

from dotenv import load_dotenv
load_dotenv() ## Load the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Default Prompt

default_prompt="""

    1. Identify the food items from the image and calculate the total calories. Provide details for each food item in the following format:

        - Food Item 1: [Calories]
        - Food Item 2: [Calories]
        ...
        -----------------------------------

    2. Assess the overall healthiness of the food based on its nutritional composition.

    3. Analyze the percentage distribution of essential nutrients such as carbohydrates, fats, fibers, sugar, and other vital components required in our diet.

"""

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(image, prompt=None):
    if prompt is None:
        prompt = default_prompt
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, image[0]])
    return response.text




def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##Initialize our streamlit app

st.set_page_config(page_title="Food Healthiness App")

st.header("Food Healthiness App")

input_prompt = st.text_input("Input Prompt (Optional): ",key="input")
uploaded_file = st.file_uploader("Choose an image:", type=["jpg", "jpeg", "png"])
image=""  

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Generate Analysis")


## If submit button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_repsonse(image_data)
    st.subheader("Analysis Results:")
    st.write(response)


