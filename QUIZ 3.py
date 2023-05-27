import os
import requests
import json
import sqlite3
import win11toast
# os.system("pip install <module name you have not installed>")

url = 'https://www.anapioficeandfire.com/api/characters?'
name = input("Enter a character's name from Game of Thrones: ")

payload = {
    'name': name
}
r = requests.get(url, payload)
data = r.text
datajson = r.json()
# print(f"Status code {r.status_code}")

# Expecting an error
if not datajson:
    print("You have entered incorrect name, you must spell it correctly")
    exit()

with open('GOT.json', 'w+') as file:
    json.dump(datajson, file, indent=4)

CharName = datajson[0]['name']
Born = datajson[0]['born']
Aliases = ', '.join(datajson[0]['aliases'][:2])
Actor = datajson[0]['playedBy'][0]


def characters_info():
    print(f"Character's name: {CharName}")
    print(f"Born: {Born}")
    print(f"Aliases: {Aliases}")
    print(f"Actor: {Actor}")


characters_info()

# Create database connection
conn = sqlite3.connect('GOT.sqlite')
cur = conn.cursor()

# Create table
cur.execute("""
    create table if not exists GOT(
        id integer primary key autoincrement,
        name varchar(30),
        born varchar(30),
        aliases varchar(50),
        actor varchar(30)
    )
""")

# Insert data into the table
columns = (CharName, Born, Aliases, Actor)
cur.executemany("insert into GOT (name, born, aliases, actor) values (?, ?, ?, ?)", (columns, ))

conn.commit()
conn.close()

# Notification
info = f"Name: {CharName}\nBorn: {Born}\nActor: {Actor}"
win11toast.toast(f"Game of Thrones characters", info)
