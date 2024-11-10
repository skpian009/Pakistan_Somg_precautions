import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import plotly.express as px
from datetime import datetime
from transformers import pipeline

import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import streamlit as st




# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# Load Google Service Account credentials from environment variables
creds_dict = {
    "type": os.getenv("GOOGLE_TYPE"),
    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("GOOGLE_UNIVERSE_DOMAIN")
}

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Pakistan Smog Data").sheet1  # Open your Google Sheet


# creds = ServiceAccountCredentials.from_json_keyfile_name('smog-441311-19de64d3f26c.json', scope)
# client = gspread.authorize(creds)
# sheet = client.open("Pakistan Smog Data").sheet1  # Open your Google Sheet

# Define and check column headers
headers = ["Timestamp", "Gender", "Age Range", "City", "Province", "Health Status", "User Name", "Suggestion"]
if not sheet.row_values(1):  # If the first row is empty, add headers
    sheet.insert_row(headers, 1)

# Initialize session state for tracking submission counts
if "submission_data" not in st.session_state:
    st.session_state["submission_data"] = {"Male": 0, "Female": 0, "Other": 0}

# Load Hugging Face's pre-trained model for health-related advice
# We will use a text generation model such as GPT-2, fine-tuned for health advice
# You can use a model like "DialoGPT" for conversational AI, or any other fine-tuned model for medical or health advice
health_advice_model = pipeline("text-generation", model="microsoft/BioGPT")  # Replace with your preferred model

# Function to generate health advice based on user input
def get_health_advice(age_range, health_status):
    # Generate health advice based on age range and health status
    input_text = f"Provide health advice for a {age_range} with the following health issues: {', '.join(health_status)}"
    advice = health_advice_model(input_text, max_length=150, num_return_sequences=1)
    return advice[0]["generated_text"]

# Streamlit App UI
st.title("Smog Awareness and Precaution App")
st.write("Learn about smog precautions and how you can contribute to reducing smog!")

# User Input: Personal Information
st.subheader("Personal Information")
gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])

# Age range selection with clear labels
age_range = st.selectbox(
    "Select Age Range",
    ["0-1 (Newborn)", "2-12 (Child)", "13-19 (Teen)", "20-64 (Adult)", "65+ (Senior)"]
)

city = st.text_input("City")
province = st.text_input("Province")

# Health status selection
health_status = st.multiselect(
    "Select Current Health Status (select all that apply)",
    ["Illness", "Cough", "Fatigue", "Sore Throat", "Watery Eyes", "Headache", "Breathing Difficulty", "Chest Pain", "Runny Nose", "Sneezing"]
)

# Suggestion submission
user_name = st.text_input("Your Name")
suggestion = st.text_area("Your Suggestions for Improving Air Quality")

# Submit Button
if st.button("Submit"):
    # Append data to Google Sheets
    health_status_str = ", ".join(health_status)
    sheet.append_row([str(datetime.now()), gender, age_range, city, province, health_status_str, user_name, suggestion])
    
    # Increment the relevant counter in session state
    st.session_state["submission_data"][gender] += 1
    st.success("Thank you! Your response has been recorded and the graph is updated.")

    # Provide AI-generated health advice based on user input
    health_advice = get_health_advice(age_range, health_status)
    st.subheader("Health Precautions and Advice")
    st.write(health_advice)

# Display interactive, real-time graph using in-memory data
st.subheader("Health Issues due to Smog - Real-Time Data")

# Convert the in-memory counter data to a format usable by Plotly
graph_data = [{"Gender": key, "Illness Count": count} for key, count in st.session_state["submission_data"].items()]

# Create the Plotly graph
fig = px.bar(
    graph_data,
    x="Gender",
    y="Illness Count",
    color="Gender",
    title="Count of Reported Illnesses by Gender due to Smog"
)
fig.update_layout(xaxis_title="Gender", yaxis_title="Illness Count", title_x=0.5)

# Display the chart
st.plotly_chart(fig)
