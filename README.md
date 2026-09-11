# Austin Weather Alerts
A Python script that monitors weather conditions for Austin, TX, and sends an email alert when certain thresholds are met.

checks for,
- Severe weather alerts via the National Weather Service API
- Extreme heat via Open-Meteo
- High chance of rain via Open-Meteo
- Poor air quality via Open-Meteo Air Quality API

The script checks all four sources every hour. If any condition is triggered, it sends a summary email via Gmail.

## Setup
1. Install: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env`
3. Fill in your Discord bot token and channel ID in `.env`:
   - Get a bot token from https://discord.com/developers/applications
   - Get your channel ID by enabling Developer Mode in Discord, then
     right-clicking the target channel → Copy Channel ID
4. Run the bot

## APIs used
- [National Weather Service API](https://www.weather.gov/documentation/services-web-api)
- [Open-Meteo](https://open-meteo.com/)
