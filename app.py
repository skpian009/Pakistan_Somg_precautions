import os
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from datetime import datetime

# Set up credentials using environment variables
credentials = {
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
}

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets", 
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]

# Replace 'credentials' with the appropriate dictionary format or JSON string as required
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)
sheet = client.open("Pakistan Smog Data").sheet1  # Your Google Sheet name

# Streamlit App UI
st.title("Smog Awareness and Precaution App")
st.markdown("## How You Can Help Reduce Smog\nReduce vehicle emissions, avoid burning waste, and opt for cleaner energy options to contribute to a healthier environment.")

# User Information Input
st.subheader("Personal Information")
gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
age_range = st.selectbox("Select Age Range", ["0-1 (Newborn)", "2-12 (Child)", "13-19 (Teen)", "20-64 (Adult)", "65+ (Senior)"])
city = st.text_input("City")
province = st.text_input("Province")

# Health Status and Health Advice
st.subheader("Current Health Status")
health_status = st.multiselect("Select any symptoms you are experiencing:", ["Illness", "Not Well", "Pain", "Sore Throat", "Watery Eyes", "Cough", "Shortness of Breath", "Fatigue", "Headache", "Congestion"])

# Health advice display
st.subheader("Health Advice")
if health_status:
    st.write("**Based on your health status:**")
    st.write("- Stay indoors as much as possible.")
    st.write("- Wear a mask if you need to go outside.")
    st.write("- Use air purifiers if available and drink warm fluids.")
    if "Severe" in health_status:
        st.write("Visit a healthcare provider if symptoms worsen.")
else:
    st.write("Stay safe! Wear masks, keep windows closed, and avoid outdoor activity if possible.")

# User Suggestions
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

# Health Impact Data Visualization
st.subheader("Health Impact Data")
age_groups = ["Newborn", "Child", "Teen", "Adult", "Senior"]
illness_data = [10, 20, 30, 40, 25]  # Replace with actual data as needed

fig, ax = plt.subplots()
ax.bar(age_groups, illness_data, color=['blue', 'green', 'orange', 'red', 'purple'])
ax.set_xlabel("Age Group")
ax.set_ylabel("Number of People Ill")
ax.set_title("Health Impact by Age Group Due to Smog")
st.pyplot(fig)
