#from __future__ import absolute_path, unicode_literals
from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from django.core.mail import send_mail

from celery_progress.backend import ProgressRecorder

import time
import requests
from urllib import request
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import lxml


@shared_task(bind=True)
def count_words(self, url):
    progress_recorder = ProgressRecorder(self)

    print(f"Counting words at {url}")

    start = time.time()

    r = request.urlopen(url)

    soup = BeautifulSoup(r.read().decode(), "lxml")

    paragraphs = " ".join([p.text for p in soup.find_all("p")])

    word_count = dict()

    
    for i in paragraphs.split():
        if not i in word_count:
            word_count[i] = 1
        else:
            word_count[i] += 1

    end = time.time()

    time_elapsed = end - start

    for i in range(10):
        time.sleep(2)
        progress_recorder.set_progress(i + 1, 10, f'On iteration {i}')
#    print(word_count)
    print(f"Total words: {len(word_count)}")
    print(f"Time elapsed: {time_elapsed} ms")

    message = f" Was the word count. Python function was done in: {time_elapsed} and URL: {url}"


    return len(word_count), message


@shared_task
def send_async_email(email_data):
    """Background task to send an email with Django-Mail."""
    send_mail(email_data['subject'],
              email_data['body'],
              'cca1337@gmail.com',
              [email_data['to']],
              fail_silently=False,
             )
  
    return None    
 
@shared_task(bind=True)
def get_weather_api(self, mesto):
    progress_recorder = ProgressRecorder(self)
    units = "metric"
    lang = "sk"
    mesto = mesto.lower()
    APIKEY = "ddac9aef54ea6f2bd618a5bab65c4bad"
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={mesto}&appid={APIKEY}&units={units}&lang={lang}"
    request = requests.get(URL)
    data = request.json()

    city = data["name"]

    latitude = data["coord"]["lat"]
    longitude = data["coord"]["lon"]
    aktualne = data["weather"][0]["description"]

    sunrise = data["sys"]["sunrise"]
    sunrise = int(sunrise)
    sunrise = datetime.utcfromtimestamp(sunrise) + timedelta(hours=1)
    sunrise = sunrise.strftime('%H:%M:%S')

    sunset = data["sys"]["sunset"]
    sunset = int(sunset)
    sunset1 = datetime.utcfromtimestamp(sunset) + timedelta(hours=1)
    sunset = datetime.utcfromtimestamp(sunset) + timedelta(hours=1)
    sunset = sunset.strftime('%H:%M:%S')

    temp = data["main"]["temp"]
    temp_max = data["main"]["temp_max"]
    temp_mix = data["main"]["temp_min"]
    feels_like = data["main"]["feels_like"]

    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    
    
    for i in range(10):
        time.sleep(2)
        progress_recorder.set_progress(i + 1, 10, f'On iteration {i}')
        

    if datetime.now() > sunset1:
        pocasie = (
                f"Mesto: {city} sa nachadza {latitude} zemepisnej sirky a {longitude} zemepisnej dlzky. Momentalne je {aktualne}"
                f"\nTeplota je {temp}°C. Pocitovo je {feels_like}°C. Max bude {temp_max}°C a min bude {temp_mix}°C"
                f"\nVlhkost je {humidity} % a rychlost vetra je {wind_speed}m/s."
                f"\nVychod slnka bude {sunrise} a zapad slnka bol {sunset}")
    else:
        pocasie = (
            f"Mesto: {city} sa nachadza {latitude} zemepisnej sirky a {longitude} zemepisnej dlzky. Momentalne je {aktualne}"
            f"\nTeplota je {temp}°C. Pocitovo je {feels_like}°C. Max bude {temp_max}°C a min bude {temp_mix}°C"
            f"\nVlhkost je {humidity} % a rychlost vetra je {wind_speed}m/s."
            f"\nVychod slnka bol {sunrise} a zapad slnka bude {sunset}")

    return pocasie
   
