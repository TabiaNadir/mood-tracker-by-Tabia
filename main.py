import streamlit as st
import pandas as pd
import datetime
import csv
import os

MOOD_FILE = "mood_log.csv"

def load_mood_data():
    if not os.path.exists(MOOD_FILE):
        return pd.DataFrame(columns=["Date", "Mood"])  
    data = pd.read_csv(MOOD_FILE)
    if data.shape[1] == 2:
        data.columns = ["Date", "Mood"]
    return data

def save_mood_data(date, mood):
    file_exists = os.path.exists(MOOD_FILE)
    with open(MOOD_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists or os.stat(MOOD_FILE).st_size == 0:
            writer.writerow(["Date", "Mood"])
        writer.writerow([date, mood])

st.title("Mood Tracker")

today = datetime.date.today()

st.subheader("How are you feeling today?")

mood = st.selectbox("Select your mood", ["Happy", "Sad", "Angry", "Neutral"])

if st.button("Log Mood"):
    save_mood_data(today, mood)
    st.success("Mood Logged Successfully!")

data = load_mood_data()

if not data.empty:
    st.subheader("Mood Trends Over Time")

    data["Date"] = pd.to_datetime(data["Date"])

    # Fix: Normalize mood values (remove spaces, capitalize)
    data["Mood"] = data["Mood"].str.strip().str.capitalize()

    mood_counts = data["Mood"].value_counts()

    st.bar_chart(mood_counts)

    st.write("Built with by [Tabia Nadir](https://github.com/TabiaNadir)")
