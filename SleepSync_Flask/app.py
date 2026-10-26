from datetime import datetime
from io import BytesIO
import base64
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from flask import Flask, render_template, request

app = Flask(__name__)
REQUIRED_COLUMNS = [
    "phone_usage_hours",
    "sleep_hours",
    "social_media_hours",
    "youtube_hours",
    "gaming_hours",
]


def fig_to_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=120)
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close(fig)
    return encoded


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("dataset")
        if not uploaded_file or uploaded_file.filename == "":
            error = "Please choose a CSV dataset."
        else:
            try:
                df = pd.read_csv(uploaded_file)
                missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
                if missing:
                    error = "Missing required columns: " + ", ".join(missing)
                else:
                    for col in REQUIRED_COLUMNS:
                        df[col] = pd.to_numeric(df[col], errors="coerce")
                    df = df.dropna(subset=REQUIRED_COLUMNS)

                    if df.empty:
                        error = "No valid rows were found in the required columns."
                    else:
                        avg_phone = float(np.mean(df["phone_usage_hours"]))
                        avg_sleep = float(np.mean(df["sleep_hours"]))
                        activity = {
                            "Social Media": float(df["social_media_hours"].mean()),
                            "YouTube": float(df["youtube_hours"].mean()),
                            "Gaming": float(df["gaming_hours"].mean()),
                        }
                        most_used = max(activity, key=activity.get)

                        usage_levels = {
                            "Low (<3 hours)": int((df["phone_usage_hours"] < 3).sum()),
                            "Moderate (3–<6 hours)": int(
                                ((df["phone_usage_hours"] >= 3) &
                                 (df["phone_usage_hours"] < 6)).sum()
                            ),
                            "High (6+ hours)": int((df["phone_usage_hours"] >= 6).sum()),
                        }

                        fig, ax = plt.subplots(figsize=(5, 4))
                        ax.pie(activity.values(), labels=activity.keys(),
                               autopct="%1.1f%%", startangle=90)
                        ax.set_title("Digital Activity Usage")
                        activity_chart = fig_to_base64(fig)

                        fig, ax = plt.subplots(figsize=(5, 4))
                        ax.pie(usage_levels.values(), labels=usage_levels.keys(),
                               autopct="%1.1f%%", startangle=90)
                        ax.set_title("Phone Usage Levels")
                        usage_chart = fig_to_base64(fig)

                        fig, ax = plt.subplots(figsize=(8, 4.5))
                        sns.scatterplot(data=df, x="phone_usage_hours",
                                        y="sleep_hours", ax=ax)
                        ax.set_title("Phone Usage vs Sleep")
                        ax.set_xlabel("Phone Usage (Hours)")
                        ax.set_ylabel("Sleep (Hours)")
                        sleep_chart = fig_to_base64(fig)

                        night_mode = datetime.now().hour >= 23
                        result = {
                            "rows": len(df),
                            "avg_phone": f"{avg_phone:.2f}",
                            "avg_sleep": f"{avg_sleep:.2f}",
                            "most_used": most_used,
                            "activity_chart": activity_chart,
                            "usage_chart": usage_chart,
                            "sleep_chart": sleep_chart,
                            "night_mode": night_mode,
                            "activity": activity,
                            "usage_levels": usage_levels,
                        }
            except Exception as exc:
                error = f"Could not read the dataset: {exc}"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
