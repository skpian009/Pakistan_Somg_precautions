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
if not sheet.row_values(1):  # If the first row is empty, add headers
    sheet.insert_row(headers, 1)

# Streamlit App
st.title("Smog Awareness and Precaution App")
st.markdown("## How You Can Help Reduce Smog\nReduce vehicle emissions, avoid burning waste, and opt for cleaner energy options to contribute to a healthier environment.")

# Step 2: User Selection
st.subheader("Personal Information")
gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
age_range = st.selectbox(
    "Select Age Range",
    ["0-1 (Newborn)", "2-12 (Child)", "13-19 (Teen)", "20-64 (Adult)", "65+ (Senior)"]
)
city = st.text_input("City")
province = st.text_input("Province")

# Step 3: Health Status
st.subheader("Current Health Status")
health_status = st.multiselect("Select any symptoms you are experiencing:", ["Illness", "Not Well", "Pain", "Sore Throat", "Watery Eyes", "Cough", "Shortness of Breath", "Fatigue", "Headache", "Congestion"])

# Health advice generation using Groq model
st.subheader("Health Advice")
if health_status:
    st.write("**Based on your health status:**")
    
    # Groq API setup
    api_key = os.environ.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/models"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    health_status_str = ", ".join(health_status)
    payload = {
        "prompt": f"Provide health advice for someone experiencing the following symptoms: {health_status_str}",
        "model": "llama-3.1-8b-instant",
        "max_tokens": 150
    }

    # Send the request to the Groq API
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        advice = response.json().get('choices')[0].get('text')
        st.write(advice)
    else:
        st.write("Error: Unable to retrieve advice. Please try again later.")
else:
    st.write("Stay safe! Wear masks, keep windows closed, and avoid outdoor activity if possible.")

# Step 4: Suggestions
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

# Step 6: Data Visualization
st.subheader("Health Impact Data")
age_groups = ["Newborn", "Child", "Teen", "Adult", "Senior"]
illness_data = [10, 20, 30, 40, 25]  # Sample data, adjust as per your collected data

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
