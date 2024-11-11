import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv
from groq import Groq
import pandas as pd

# Load environment variables from a .env file
load_dotenv()

# Access the API key from environment variables
api_key = os.getenv("GROQ_API_KEY")

# File to store user data
DATA_FILE = 'user_data.csv'

# Function to save data
def save_data():
    if all([
        st.session_state.get("gender"),
        st.session_state.get("age_range"),
        st.session_state.get("province"),
        st.session_state.get("health_status")
    ]):
        new_data = {
            "timestamp": [datetime.now()],
            "gender": [st.session_state.gender],
            "age_range": [st.session_state.age_range],
            "province": [st.session_state.province],
            "symptoms": [", ".join(st.session_state.health_status)]
        }
        new_df = pd.DataFrame(new_data)

        # Append to CSV file, creating it if it doesn't exist
        if os.path.exists(DATA_FILE):
            new_df.to_csv(DATA_FILE, mode='a', header=False, index=False)
        else:
            new_df.to_csv(DATA_FILE, index=False)

# Streamlit App
st.title("Smog Awareness and Precaution App")
st.markdown("## How You Can Help Reduce Smog\nReduce vehicle emissions, avoid burning waste, and opt for cleaner energy options to contribute to a healthier environment.")

# Step 2: User Selection
st.subheader("Personal Information")

st.selectbox("Select Gender", ["Male", "Female", "Other"], key="gender", on_change=save_data)
st.selectbox("Select Age Range", ["0-1 (Newborn)", "2-12 (Child)", "13-19 (Teen)", "20-64 (Adult)", "65+ (Senior)"], key="age_range", on_change=save_data)
st.text_input("City", key="city", on_change=save_data)
st.text_input("Province", key="province", on_change=save_data)

# Step 3: Health Status
st.subheader("Current Health Status")
st.multiselect("Select any symptoms you are experiencing:", 
               ["Illness", "Not Well", "Pain", "Sore Throat", "Watery Eyes", "Cough", 
                "Shortness of Breath", "Fatigue", "Headache", "Congestion"], 
               key="health_status", on_change=save_data)

# Function to get health advice from the LLM via Groq API
def get_health_advice(health_status):
    client = Groq(api_key=api_key)
    
    # Create a Groq chat completion request
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"Provide health advice based on the following health status: {health_status}.",
        }],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content.strip()

# Streamlit UI for Health Advice
st.subheader("Health Advice")

if st.session_state.get("health_status"):
    st.write("**Based on your health status:**")
    advice = get_health_advice(", ".join(st.session_state.health_status))  # Joining list into a comma-separated string
    st.write(advice)
else:
    st.write("Stay safe! Wear masks, keep windows closed, and avoid outdoor activity if possible.")

# Step 6: Data Visualization based on Stored Data
st.subheader("Health Impact Data Based on All User Input")

if os.path.exists(DATA_FILE):
    # Load data
    df = pd.read_csv(DATA_FILE)
    
    # Count occurrences by age group
    age_group_counts = df.groupby('age_range').size()

    # Prepare data for the bar chart
    age_groups = ["0-1 (Newborn)", "2-12 (Child)", "13-19 (Teen)", "20-64 (Adult)", "65+ (Senior)"]
    illness_counts = [age_group_counts.get(age, 0) for age in age_groups]

    # Plot cumulative data
    fig, ax = plt.subplots()
    ax.bar(age_groups, illness_counts, color=['blue', 'green', 'orange', 'red', 'purple'])
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Number of Ill People")
    ax.set_title("Cumulative Health Impact by Age Group Due to Smog")
    st.pyplot(fig)
else:
    st.write("No data available yet.")




import pandas as pd
import streamlit as st
import os

# Access the secret code from GitHub Secrets (environment variable)
secret_code = os.getenv("DOWNLOAD_SECRET_CODE")

# Temporary debug output (remember to remove after confirming)
st.write("Debug Secret Code:", secret_code)

# Prompt the user for a secret code
user_input = st.text_input("Enter the secret code to download user data:", type="password")

if user_input == secret_code:
    st.success("Access granted")
    # Show download button if CSV file exists
    if os.path.exists("user_data.csv"):
        with open("user_data.csv", "rb") as file:
            st.download_button(
                label="Download User Data",
                data=file,
                file_name="user_data.csv",
                mime="text/csv"
            )
elif user_input:
    st.error("Access denied")

