# Austin Weather Alerts
A Python script that monitors weather conditions for Austin, TX, and sends an email alert when certain thresholds are met.

checks for,
- Severe weather alerts via the National Weather Service API
- Extreme heat via Open-Meteo
- High chance of rain via Open-Meteo
- Poor air quality via Open-Meteo Air Quality API

The script checks all four sources every hour. If any condition is triggered, it sends a summary email via Gmail.

## Setup
1. Install dependencies: `pip install requests`
2. Replace the placeholder values:
   - `email_here`: your Gmail address
   - `app_password_here`: with a Gmail App Password
3. Good to go

APIs used
- [National Weather Service API](https://www.weather.gov/documentation/services-web-api)
- [Open-Meteo](https://open-meteo.com/)
