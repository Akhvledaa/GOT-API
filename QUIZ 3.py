import os
import requests
import json
import sqlite3
import win11toast
# os.system("pip install <module name you have not installed>")

key = '887aaff89bee4fd742287bfd4afa2483'
units = 'metric'
city = input("Enter the city name: ")
url = 'https://api.openweathermap.org/data/2.5/weather?'

params = {
    'q': city,
    'appid': key,
    'units': units
}
response = requests.get(url, params)
data = response.text
data_json = response.json()

print(f"Status code {response.status_code}")

with open('file.json', 'w+') as file:
    json.dump(data_json, file, indent=4)

weather = data_json['weather'][0]['description']
weather_temp = data_json['main']['temp']


def weather_info():
    print(f"Current weather in {city}: {weather}")
    print(f"Current temp: {weather_temp}")


weather_info()

# Create database connection
conn = sqlite3.connect('weather.sqlite')
cur = conn.cursor()

# Create table
cur.execute("""
    create table if not exists weather(
        id integer primary key autoincrement,
        city varchar(20),
        weather varchar(20),
        temp integer
    )
""")

# Insert data into table
columns = (city, weather, weather_temp)
cur.executemany("insert into weather (city, weather, temp) values (?, ?, ?)", (columns, ))

# Commit changes and close connection
conn.commit()
conn.close()

# Notification
info = f'It is {weather_temp} degrees in {city}'
win11toast.toast(f"Weather", info, dialogue=info, duration='short', buttons=['Open app', 'Dismiss'])
