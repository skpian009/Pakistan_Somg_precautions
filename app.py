import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from a .env file
load_dotenv()

# Access the API key from environment variables
api_key = os.getenv("GROQ_API_KEY")

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
health_status = st.multiselect("Select any symptoms you are experiencing:", 
                               ["Illness", "Not Well", "Pain", "Sore Throat", "Watery Eyes", "Cough", 
                                "Shortness of Breath", "Fatigue", "Headache", "Congestion"])

# Function to get health advice from the LLM via Groq API
def get_health_advice(health_status):
    client = Groq(api_key=api_key)
    
    # Create a Groq chat completion request
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Provide health advice based on the following health status: {health_status}.",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content.strip()

# Streamlit UI for Health Advice
st.subheader("Health Advice")

if health_status:
    st.write("**Based on your health status:**")
    advice = get_health_advice(", ".join(health_status))  # Joining list into a comma-separated string
    st.write(advice)
else:
    st.write("Stay safe! Wear masks, keep windows closed, and avoid outdoor activity if possible.")

# Step 4: Suggestions
st.subheader("Share Your Suggestions")
user_name = st.text_input("Your Name")
suggestion = st.text_area("Share any suggestions or experiences to help improve air quality:")

if st.button("Submit Suggestion"):
    if user_name and suggestion:
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
