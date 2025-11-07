"""
Streamlit app for Calorie Scout (calorie-scout-genai).

Usage:
    streamlit run app.py
"""

import streamlit as st
from PIL import Image
from calorie_scout.openai_client import OpenAIVisionClient
from calorie_scout.config import OPENAI_API_KEY
import io
import json

st.set_page_config(page_title="Calorie Scout", layout="centered")

st.title("Calorie Scout — GenAI Food Nutrition Estimator")
st.markdown(
    "Upload a photo of a meal, and the GenAI model will suggest detected food items and estimate calories. "
    "The model will also provide a brief description of the food, it's typical ingredients, nutritional profile, and the advantages and disadvantages of consuming this food."
)

# Sidebar settings
st.sidebar.header("Settings")
model_choice = st.sidebar.text_input("OpenAI model", value="gpt-4o")
api_key_input = st.sidebar.text_input("OpenAI API key (or set OPENAI_API_KEY env)", type="password")

# pick API key
api_key = api_key_input.strip() or OPENAI_API_KEY
if not api_key:
    st.sidebar.warning("No OpenAI key found. Set OPENAI_API_KEY in environment or enter it here.")
    st.stop()

client = OpenAIVisionClient(api_key=api_key, model=model_choice)

uploaded_file = st.file_uploader("Upload a food image", type=["jpg","jpeg","png"])

if uploaded_file:
    # Display image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded image", use_container_width=True)
    st.write("Sending to OpenAI for detection...")

    # Build a food recognition prompt
    food_recognition_prompt = """
    Context: I'm analyzing a food image for a calorie tracking application.
    Imstruction: Please identify the food in this image.
    Input: [The image i am about to share]
    Output: Provide the name of the food, a brief description of what you see, and if possible , mention it's typical ingredients or nutritional profile and the advantages and disadvantages of consuming this food.

    "total_calories": float
    
    If data is missing, make a reasonable estimate based on common serving sizes.
    """

    openai_description = client.query_image(
        image=image,
        prompt=food_recognition_prompt,
        max_tokens=800
    )
    
    st.markdown(openai_description)