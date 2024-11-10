import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import os

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

# Define and check column headers
headers = ["Timestamp", "Gender", "Age Range", "City", "Province", "Health Status", "User Name", "Suggestion"]
if not sheet.row_values(1):
    sheet.insert_row(headers, 1)

# Streamlit App setup
st.title("Smog Awareness and Precaution App")
st.markdown("## How You Can Help Reduce Smog\nReduce vehicle emissions, avoid burning waste, and opt for cleaner energy options to contribute to a healthier environment.")

# Personal Information Input
st.subheader("Personal Information")
gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
age_range = st.selectbox("Select Age Range", ["0-1 (Newborn)", "2-12 (Child)", "13-19 (Teen)", "20-64 (Adult)", "65+ (Senior)"])
city = st.text_input("City")
province = st.text_input("Province")

# Health Status Input
st.subheader("Current Health Status")
health_status = st.multiselect("Select any symptoms you are experiencing:", ["Illness", "Not Well", "Pain", "Sore Throat", "Watery Eyes", "Cough", "Shortness of Breath", "Fatigue", "Headache", "Congestion"])

# Health Advice with Groq LLM
st.subheader("Health Advice")

def get_health_advice(symptoms):
    api_key = os.getenv("GROQ_API_KEY")  # Ensure GROQ_API_KEY is set in environment variables
    url = "https://api.groq.com/openai/v1/models/llama-3.1-8b-instant/completions"
    
    # Define payload
    payload = {
        "prompt": f"Provide health advice for symptoms: {', '.join(symptoms)}",
        "max_tokens": 50,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        advice = response.json().get("choices")[0].get("text")
        return advice
    else:
        return "Error retrieving health advice. Please try again."

if health_status:
    advice = get_health_advice(health_status)
    st.write(f"**Based on your health status:** {advice}")
else:
    st.write("Stay safe! Wear masks, keep windows closed, and avoid outdoor activity if possible.")

# Suggestions Section
st.subheader("Share Your Suggestions")
user_name = st.text_input("Your Name")
suggestion = st.text_area("Share any suggestions or experiences to help improve air quality:")

if st.button("Submit Suggestion"):
    if user_name and suggestion:
        health_status_str = ", ".join(health_status)
        sheet.append_row([str(datetime.now()), gender, age_range, city, province, health_status_str, user_name, suggestion])
        st.success("Thank you for your contribution!")
    else:
        st.error("Please fill out your name and suggestion.")

# Data Visualization Section
st.subheader("Health Impact Data")
age_groups = ["Newborn", "Child", "Teen", "Adult", "Senior"]
illness_data = [10, 20, 30, 40, 25]  # Sample data, replace with actual data

fig, ax = plt.subplots()
ax.bar(age_groups, illness_data, color=['blue', 'green', 'orange', 'red', 'purple'])
ax.set_xlabel("Age Group")
ax.set_ylabel("Number of People Ill")
ax.set_title("Health Impact by Age Group Due to Smog")
st.pyplot(fig)

# Store user data in Google Sheets
if gender and age_range and health_status:
    sheet.append_row([str(datetime.now()), gender, age_range, city, province, health_status])

st.write("Data is stored and can be accessed for analysis [here](<Google Sheet link>)")
