# Austin Weather Alerts
A Discord bot that monitors weather conditions for Austin, TX, and sends alerts when certain thresholds are met, and a daily forecast in the morning.

checks for,
- Severe weather alerts via the National Weather Service API
- Extreme heat via Open-Meteo
- High chance of rain via Open-Meteo
- Poor air quality via Open-Meteo Air Quality API

The script checks all four sources every hour. If any condition is triggered, it sends an alert.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env`
3. Fill in your Discord bot token and channel ID in `.env`:
   - Get a bot token from https://discord.com/developers/applications
   - Get your channel ID by enabling Developer Mode in Discord, then
     right-clicking the target channel → Copy Channel ID
4. Run the bot: `python weather_discord_bot.py`

## APIs used
- [National Weather Service API](https://www.weather.gov/documentation/services-web-api)
- [Open-Meteo](https://open-meteo.com/)
