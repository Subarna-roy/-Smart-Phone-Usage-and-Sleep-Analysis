import os
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. LOAD DATASET
DATA_FOLDER = "data"
csv_files = [f for f in os.listdir(DATA_FOLDER) if f.lower().endswith(".csv")]

if not csv_files:
    print("No CSV file found!")
    print("Put your dataset CSV inside the 'data' folder.")
    raise SystemExit

df = pd.read_csv(os.path.join(DATA_FOLDER, csv_files[0]))

print("=" * 50)
print("SMART PHONE USAGE & SLEEP ANALYSIS")
print("=" * 50)
print("\nDataset Shape:", df.shape)
print("\nFirst 5 Records:")
print(df.head())

# 2. CHECK REQUIRED COLUMNS
required = [
    "phone_usage_hours",
    "sleep_hours",
    "social_media_hours",
    "youtube_hours",
    "gaming_hours"
]

missing = [c for c in required if c not in df.columns]
if missing:
    print("\nMissing columns:", missing)
    raise SystemExit

# 3. BASIC ANALYSIS
avg_phone = np.mean(df["phone_usage_hours"])
avg_sleep = np.mean(df["sleep_hours"])

print("\n--- BASIC RESULT ---")
print("Average Phone Usage:", round(avg_phone, 2), "hours")
print("Average Sleep:", round(avg_sleep, 2), "hours")

# 4. MOST USED DIGITAL ACTIVITY
activity = {
    "Social Media": df["social_media_hours"].mean(),
    "YouTube": df["youtube_hours"].mean(),
    "Gaming": df["gaming_hours"].mean()
}
most_used = max(activity, key=activity.get)

print("\n--- DIGITAL ACTIVITY ---")
for name, value in activity.items():
    print(name + ":", round(value, 2), "hours")
print("Most Used Activity:", most_used)

# 5. PIE CHART - DIGITAL ACTIVITY
plt.figure(figsize=(6, 6))
plt.pie(activity.values(), labels=activity.keys(), autopct="%1.1f%%", startangle=90)
plt.title("Digital Activity Usage")
plt.tight_layout()
plt.show()

# 6. PHONE USAGE LEVELS
low = (df["phone_usage_hours"] < 3).sum()
moderate = ((df["phone_usage_hours"] >= 3) & (df["phone_usage_hours"] < 6)).sum()
high = (df["phone_usage_hours"] >= 6).sum()

usage = {"Low": low, "Moderate": moderate, "High": high}

print("\n--- PHONE USAGE LEVELS ---")
print("Low:", low)
print("Moderate:", moderate)
print("High:", high)

# 7. PIE CHART - PHONE USAGE
plt.figure(figsize=(6, 6))
plt.pie(usage.values(), labels=usage.keys(), autopct="%1.1f%%", startangle=90)
plt.title("Phone Usage Levels")
plt.tight_layout()
plt.show()

# 8. SCATTER PLOT - PHONE USAGE VS SLEEP
plt.figure(figsize=(7, 5))
sns.scatterplot(data=df, x="phone_usage_hours", y="sleep_hours")
plt.title("Phone Usage vs Sleep")
plt.xlabel("Phone Usage (Hours)")
plt.ylabel("Sleep (Hours)")
plt.tight_layout()
plt.show()

# 9. NIGHT MODE RECOMMENDATION
current_hour = datetime.now().hour

print("\n" + "=" * 50)
print("NIGHT MODE")
print("=" * 50)

if current_hour >= 23:
    print("Night Mode: ON")
    print("Recommended Activity to Limit:", most_used)
    print("Emergency Calls: Allowed")
    print("Emergency Messages: Allowed")
else:
    print("Night Mode: OFF")
    print("Normal Usage")

# 10. FINAL RESULT
print("\n" + "=" * 50)
print("FINAL RESULT")
print("=" * 50)
print("Average Phone Usage:", round(avg_phone, 2), "hours")
print("Average Sleep:", round(avg_sleep, 2), "hours")
print("Most Used Activity:", most_used)
print("\nProject completed successfully.")
