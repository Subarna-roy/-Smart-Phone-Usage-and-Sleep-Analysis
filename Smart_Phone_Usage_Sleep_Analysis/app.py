import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(
    page_title="Smart Phone Usage & Sleep Analysis",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Smart Phone Usage & Sleep Analysis")
st.write("Analyze student phone usage, sleep patterns and digital activities.")

uploaded_file = st.file_uploader(
    "Upload your Student Productivity & Digital Distraction CSV",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload your CSV dataset to start the analysis.")
    st.stop()

df = pd.read_csv(uploaded_file)

required_columns = [
    "phone_usage_hours",
    "sleep_hours",
    "social_media_hours",
    "youtube_hours",
    "gaming_hours"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error("Missing columns: " + ", ".join(missing))
    st.stop()

st.success("Dataset uploaded successfully!")

with st.expander("View Dataset"):
    st.dataframe(df.head(20), use_container_width=True)

# Basic results
avg_phone = np.mean(df["phone_usage_hours"])
avg_sleep = np.mean(df["sleep_hours"])

activity = {
    "Social Media": df["social_media_hours"].mean(),
    "YouTube": df["youtube_hours"].mean(),
    "Gaming": df["gaming_hours"].mean()
}

most_used = max(activity, key=activity.get)

# Summary
st.subheader("📊 Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Phone Usage",
    f"{avg_phone:.2f} hrs"
)

col2.metric(
    "Average Sleep",
    f"{avg_sleep:.2f} hrs"
)

col3.metric(
    "Most Used Activity",
    most_used
)

# Charts
left, right = st.columns(2)

with left:
    st.subheader("📱 Digital Activity Usage")

    fig1, ax1 = plt.subplots(figsize=(5, 5))

    ax1.pie(
        activity.values(),
        labels=activity.keys(),
        autopct="%1.1f%%",
        startangle=90
    )

    ax1.set_title("Digital Activity Usage")
    st.pyplot(fig1)

with right:
    st.subheader("📊 Phone Usage Levels")

    low = (df["phone_usage_hours"] < 3).sum()

    moderate = (
        (df["phone_usage_hours"] >= 3) &
        (df["phone_usage_hours"] < 6)
    ).sum()

    high = (df["phone_usage_hours"] >= 6).sum()

    usage = {
        "Low": low,
        "Moderate": moderate,
        "High": high
    }

    fig2, ax2 = plt.subplots(figsize=(5, 5))

    ax2.pie(
        usage.values(),
        labels=usage.keys(),
        autopct="%1.1f%%",
        startangle=90
    )

    ax2.set_title("Phone Usage Levels")
    st.pyplot(fig2)

# Scatter plot
st.subheader("📱 Phone Usage vs 😴 Sleep")

fig3, ax3 = plt.subplots(figsize=(9, 5))

sns.scatterplot(
    data=df,
    x="phone_usage_hours",
    y="sleep_hours",
    ax=ax3
)

ax3.set_title("Phone Usage vs Sleep")
ax3.set_xlabel("Phone Usage (Hours)")
ax3.set_ylabel("Sleep (Hours)")

st.pyplot(fig3)

# Night mode
st.subheader("🌙 Night Mode Recommendation")

current_hour = datetime.now().hour

if current_hour >= 23:
    st.warning("🌙 Night Mode: ON")
    st.write(
        f"Recommended activity to limit: **{most_used}**"
    )
    st.write("☎️ Emergency Calls: Allowed")
    st.write("💬 Emergency Messages: Allowed")
else:
    st.success("☀️ Night Mode: OFF")
    st.write("Normal usage is currently allowed.")

st.info(
    "Note: Night Mode is a proposed recommendation feature. "
    "The dataset does not contain actual time-of-day usage data."
)
