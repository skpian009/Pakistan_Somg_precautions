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
    "private_key"="""-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCU1PFrscMPPonR\ncyUQL30Qe2xj274E5NjZrif5hnEnQFDBCmaN/dTTeXEl8v/CBSP48lBfkDqSc/Ml\nCFaCrAnaIApGoGDtvfzjVINJ2b8VK1M2rSXYpSfjuVu6N9ag4Wm3BkudAo0yKyq8\n188P0LBgzBnWjkdq86VhaGB7FtNix0H92M2dpn6lTaAGOxdmZJx33GTZNAnYE7wG\nMrvi7v+Evo8mGBrwY8gYeLvJ1JIlTRHVUJKcik+4DqSD41c9+t1nQ21GjqxHg54g\naqLXQAtj1WqB9nFgs5QT3Mbmtf/AibAYseWjeCYFNvWR6E6UQdTMDoWayDgl0hbw\nMPttmme9AgMBAAECggEAHyE2GOA+zCS4x2Al56+DIWwrZOycn2HtcIRylIi4CK11\nZpciEb9+oTf0wGsF70NLfaHTSVW9xo2tlPicPas1yVOryo93jqqPJ05xQoRiqQ8d\nkeFf+eM7h3Bo/Pd6cz6Ksc9FiAL1XQG15/dctjJgffKa0euDCR4KoKfoDD7fOnjg\nyaHKzHV8jFmAhL0UggkJJY5ZPYz1Q7oXseXNqVoHWKmrXsqZ6PeSmPMyY/tgBbZO\njv48+mlG9agRyDW4qTslwwTNweF63RGBGNKuB54gpdJ0WsaKI7FOwA0DC5QYwwWK\nY1AGSvklBTUEs+TLJF6hNfBkiyylGJ71Bp55WHlGIQKBgQDHwVaToBqolvo004qP\ndLgcuBR3H/XrF5IRSXgnTe7uk5qw2auou4KVEs93sdLTuEmhW+P/EH/H4fzoYg9e\n0AKMEjexQgP4CZI6kyu3ugbiTE+7+z94LU/KiVlY39gtROm/isi9mZVJump8H4nw\ndsVP2syOHoMqHQ+LKzkPKsvLHQKBgQC+vPeTY+zPFDsm/YcZbxMkJgB0OhdNPvrp\nAaRGp8QBq81W06Kf9d5fmHlCPdarJ9s4nC7jBwdrOyxv+2Jg8sHAo+D8T0IhhDeF\nmbwMJnzz2UnjfGAH6twLg+Dw9HHvugTTpuespP9MgdD0HAlFkVll/bUq0/ZGttpC\n3i9lCDvNIQKBgHSN+1ZoNSXp8lSgmljaYhNf1ZEstPFX74Lmu5UzhBbxSXGnkOID\nh040i5nryHiBL3VXiNFrbyPSWR+/F/japqHUf2qOeoJgE1LaTMgHY7znih7Fm2Mk\nDUrAmcGh2yGO9FUvRbJbyyAaBcgnHvWQV9EgefrzEtWf31H1BnYzInaBAoGAIEyr\nuB/hyCdq5O1l5V6z5RkyVnxH2eLiZnbKtNRQEuBfA2cPUPs3zwRo9Fi4c39qVinM\nntFf5j69BbGSNUymltKplNBvKHHVXSBtgbk6y6huJMG5GV4iKSkJ/IPIj4n2q0jG\nTqwaN4B8O/pLb6ZvdyABf+EpAUyRpWUurXM5fUECgYEAtuM4vRRQCP0/DIArZk/h\nLpZYDbaAMYjIphtVp9lk0is5FQEUuqviDYw88qpyJL5WD428wZ3j3qKqwB+0aVUB\nziQyb0YEAFY80TP+/hpVPKr6iWbkhQi1YiKFbfTsBIZx7mxSKLa5bY46QUdMNiRd\ntQcZWeiqwDrMQt+FX24QP0U=\n-----END PRIVATE KEY-----\n
 """,
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
