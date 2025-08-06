import boto3
import requests
from datetime import datetime, timezone

# Email addresses
TO_EMAIL = "kavangowda69@gmail.com"
FROM_EMAIL = "kavangowda69@gmail.com"

# Free weather API (optional)
CITY = "Bangalore"
WEATHER_API_KEY = "9cbaa3c7e20511787ebeb4453a0879e5"  # Replace with your OpenWeatherMap API key (free)
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"

def lambda_handler(event, context):
    # Fetch AWS cost estimate
    ce = boto3.client('ce', region_name='us-east-1')
    today = datetime.now(timezone.utc).date()
    billing = ce.get_cost_and_usage(
        TimePeriod={'Start': str(today), 'End': str(today)},
        Granularity='DAILY',
        Metrics=['UnblendedCost']
    )
    cost = billing['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']

    # Fetch weather
    try:
        weather_data = requests.get(WEATHER_URL).json()
        weather = f"{weather_data['weather'][0]['description']} at {weather_data['main']['temp']}°C"
    except:
        weather = "Could not fetch weather"

    # Count log events from CloudWatch (example: Lambda logs)
    logs = boto3.client('logs')
    try:
        streams = logs.describe_log_streams(
            logGroupName='/aws/lambda/DailyReportSender',
            orderBy='LastEventTime',
            descending=True,
            limit=5
        )
        latest_stream = streams['logStreams'][0]
        log_count = latest_stream.get('storedBytes', 0)
    except:
        log_count = "N/A"

    # Compose email
    subject = "🌤️ Daily AWS Report – Billing, Logs & Weather"
    body = f"""
    Daily Cloud Report:

    📦 AWS Cost Today: ${cost}
    📈 Log Event Bytes (latest stream): {log_count}
    🌤️ Weather in {CITY}: {weather}

    This is an automated daily report from your AWS Lambda.
    """

    # Send email via SES
    ses = boto3.client('ses')
    ses.send_email(
        Source=FROM_EMAIL,
        Destination={'ToAddresses': [TO_EMAIL]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )

    return {"status": "success"}
