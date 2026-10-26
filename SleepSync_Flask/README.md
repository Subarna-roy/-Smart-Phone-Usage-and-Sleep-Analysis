# SleepSync — Flask Edition

SleepSync is a student data-analysis project that explores phone usage, digital activities and sleep patterns. The frontend uses **Flask, HTML and CSS**; the charts are generated with Matplotlib and Seaborn.

## Features
- Average phone usage and sleep summary cards
- Most-used activity (Social Media, YouTube, Gaming)
- Digital activity pie chart
- Low / Moderate / High phone usage pie chart
- Phone usage vs sleep scatter plot
- Night Mode recommendation after 11 PM
- CSV upload through the website

## Required CSV columns
- `phone_usage_hours`
- `sleep_hours`
- `social_media_hours`
- `youtube_hours`
- `gaming_hours`

## Run in VS Code
1. Extract and open this `SleepSync_Flask` folder in VS Code.
2. Open the terminal in this folder.
3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Start the Flask website:

```bash
python app.py
```

5. Open this address in your browser: `http://127.0.0.1:5000`
6. Upload your CSV dataset.

## Important limitation
The dataset does not contain actual time-of-day phone usage. Night Mode is a proposed recommendation based on the computer's current time and does not block applications. The scatter plot shows patterns, not proof of causation.
