# Smart Phone Usage & Sleep Analysis

## What the project does
- Calculates average phone usage and sleep.
- Finds the most-used activity: Social Media, YouTube or Gaming.
- Shows a digital-activity pie chart.
- Groups phone usage into Low, Moderate and High.
- Shows a phone-usage pie chart.
- Shows Phone Usage vs Sleep using a scatter plot.
- Gives a Night Mode recommendation after 11 PM.

## Dataset
Put your CSV file inside the `data` folder.

Required columns:
- phone_usage_hours
- sleep_hours
- social_media_hours
- youtube_hours
- gaming_hours

The program automatically reads the first CSV file in `data`.

## Run in VS Code

1. Open this project folder in VS Code.
2. Put your dataset CSV in `data`.
3. Open Terminal.
4. Run:

```bash
pip install -r requirements.txt
python main.py
```

## Note
The dataset has no actual clock-time column. Therefore, Night Mode is a proposed recommendation feature. It does not actually block apps.
