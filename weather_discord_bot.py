import requests
import datetime
import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv


load_dotenv()
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])
intents = discord.Intents.default()
client = discord.Client(intents=intents)


WEATHER_CODES = { # om weather codes
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}
last_forecast_date = None  # checks if already sent


async def send_discord_message(content):
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:  # not cached yet
        channel = await client.fetch_channel(CHANNEL_ID)
    await channel.send(content)


async def check_weather():

    # national weather service alerts for extreme weather
    nws_url = 'https://api.weather.gov/alerts/active?point=30.2672,-97.7431'  # api
    nws_headers = {"User-Agent": "extreme weather alerts (email_here)"}  # nws headers
    nws_response = requests.get(nws_url, headers=nws_headers)  # get

    # open mateo alerts for chance of rain and extreme heat
    om_url = 'https://api.open-meteo.com/v1/forecast?latitude=30.2672&longitude=-97.7431&current=temperature_2m,precipitation_probability&temperature_unit=fahrenheit'
    om_response = requests.get(om_url)  # get

    # open mateo alerts for air quality
    aq_url = 'https://air-quality-api.open-meteo.com/v1/air-quality?latitude=30.2672&longitude=-97.7431&current=us_aqi'
    aq_response = requests.get(aq_url)

    alerts = []  # collect alerts
    if nws_response.status_code == 200:  # nws operational
        nws_data = nws_response.json()
        features = nws_data['features']  # return extreme weather
        if len(features) == 0:
            pass
        else:
            for feature in features:
                alerts.append(feature['properties']['event'])
    else:
        print(f'get failed + {nws_response.status_code}')


    if om_response.status_code == 200:  # om operational
        om_data = om_response.json()
        temperature = om_data['current']['temperature_2m']
        rain_chance = om_data['current']['precipitation_probability']
        if rain_chance > 50:  # return heat and rain risk
            alerts.append(f'🌧️🌧️🌧️ {rain_chance}% CHANCE OF RAIN 🌧️🌧️🌧️')
        else:
            pass
        if temperature > 95:
            alerts.append(f'☀️☀️☀️ EXTREME TEMPS OF {temperature} DEGREES!!! ☀️☀️☀️')
        else:
            pass
    else:
        print(f'get failed + {om_response.status_code}')


    if aq_response.status_code == 200:  # aq operational
        aq_data = aq_response.json()
        air_quality = aq_data['current']['us_aqi']
        if air_quality > 75:  # return air quality
            alerts.append(f'⚠️⚠️⚠️ DANGEROUS AIR QUALITY INDEX OF {air_quality}!! ⚠️⚠️⚠️')
        else:
            pass
    else:
        print(f'get failed + {aq_response.status_code}')

    if alerts:
        body = '\n'.join(alerts)
        await send_discord_message(f'🚨🚨🚨 **WEATHER ALERT** 🚨🚨🚨\n{body}')
    else:
        print('no alerts')


async def get_forecast(): # daily forecast
    fc_url = (
        'https://api.open-meteo.com/v1/forecast'
        '?latitude=30.2672&longitude=-97.7431'
        '&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode,sunrise,sunset'
        '&temperature_unit=fahrenheit'
        '&timezone=America%2FChicago'
    )
    response = requests.get(fc_url)

    data = response.json()
    daily = data['daily']

    high = daily['temperature_2m_max'][0] # vars
    low = daily['temperature_2m_min'][0]
    rain_chance = daily['precipitation_probability_max'][0]
    code = daily['weathercode'][0]
    sunrise = daily['sunrise'][0].split('T')[1]  # strip date
    sunset = daily['sunset'][0].split('T')[1]
    condition = WEATHER_CODES.get(code, f'Unknown ({code})')

    body = ( # format
        f"Today's forecast for Austin:\n"
        f"Condition: {condition}\n"
        f"High: {high}°F | Low: {low}°F\n"
        f"Chance of rain: {rain_chance}%\n"
        f"Sunrise: {sunrise} | Sunset: {sunset}"
    )

    await send_discord_message(body)


@tasks.loop(hours=1) # sends out forecast
async def weather_loop():
    global last_forecast_date

    await check_weather()

    now = datetime.datetime.now() # sends it only once around 7am
    if now.hour >= 7 and last_forecast_date != now.date():
        await get_forecast()
        last_forecast_date = now.date()


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    if not weather_loop.is_running():
        weather_loop.start()


if __name__ == '__main__':
    client.run(DISCORD_TOKEN)