import boto3
import requests
from datetime import datetime, timedelta, timezone


TO_EMAIL = "kavangowda69@gmail.com"
FROM_EMAIL = "kavangowda69@gmail.com"  # Fixed double '@' typo


CITY = "Bangalore"
WEATHER_API_KEY = "9cbaa3c7e20511787ebeb4453a0879e5"
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"

def lambda_handler(event, context):
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=1)

    try:
        ce = boto3.client('ce', region_name='us-east-1')
        billing = ce.get_cost_and_usage(
            TimePeriod={'Start': str(start), 'End': str(end)},
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )
        cost = billing['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
    except Exception as e:
        cost = f"Error fetching cost: {str(e)}"

    try:
        weather_data = requests.get(WEATHER_URL, timeout=5).json()
        weather = f"{weather_data['weather'][0]['description'].title()} at {weather_data['main']['temp']}°C"
    except:
        weather = "Could not fetch weather"

    try:
        logs = boto3.client('logs')
        streams = logs.describe_log_streams(
            logGroupName='/aws/lambda/DailyReportSender',
            orderBy='LastEventTime',
            descending=True,
            limit=1
        )
        latest_stream = streams['logStreams'][0]
        log_count = latest_stream.get('storedBytes', '0')
    except:
        log_count = "N/A"

    subject = "🌤️ Daily AWS Report – Billing, Logs & Weather"
    body = f"""
👋 Hello Kavan,

📅 Report Date: {start} to {end}

📦 AWS Cost: ${cost}
📈 Log Event Bytes (latest stream): {log_count}
🌤️ Weather in {CITY}: {weather}

✅ This is your automated daily cloud report.

– Lambda Bot ☁️
"""

    try:
        ses = boto3.client('ses', region_name='us-east-1')
        ses.send_email(
            Source=FROM_EMAIL,
            Destination={'ToAddresses': [TO_EMAIL]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        return {"status": "Email sent successfully!"}
    except Exception as e:
        return {"status": f"Email failed: {str(e)}"}
