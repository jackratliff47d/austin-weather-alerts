import requests
import time
import smtplib
from email.message import EmailMessage


def send_email(subject, body): # email alerts
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'email_here'
    msg['To'] = 'email_here'
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('email_here', 'app_password_here')
        smtp.send_message(msg)



def check_weather():

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
        send_email('🚨🚨🚨 WEATHER ALERT 🚨🚨🚨', body)
    else:
        print('No alerts this check.')


while True: # checks for alerts every hour
    check_weather()
    time.sleep(3600)


