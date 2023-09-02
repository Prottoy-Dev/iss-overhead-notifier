import requests
from datetime import datetime
import smtplib
import time
import os
from dotenv import load_dotenv
load_dotenv()

MY_LAT = os.getenv("MY_LAT")
MY_LONG = os.getenv("MY_LONG")

my_email = os.getenv("my_email")
my_pass = os.getenv("my_pass")


def overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now <= sunset or time_now >= sunset:
        return True


while True:
    time.sleep(60)
    if overhead() and night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(my_email, my_pass)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="example@gmail.com",
                msg="Subject:look up\n\n look up"
            )
