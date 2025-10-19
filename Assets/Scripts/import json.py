import json
import datetime
import random


eatingOut = [
    {
        "name": "Whackdonalds",
        "price": "random.choice(range(6,10.51,0.5))",
        "tag": "EO",
    },
    {
        "name": "Subway",
        "price": "random.choice(range(6,10.51,0.5))",
        "tag": "EO",
    },
    {
        "name": "KFC",
        "price": "random.choice(range(6,10.51,0.5))",
        "tag": "EO",
    },
    {
        "name": "Useless Amazon thing",
        "price": "random.choice(range(10,100,0.01))",
        "tag": "OS",
    },
    {
        "name": "Steam Game",
        "price": "random.choice(range(10,50,5))",
        "tag": "EO",
    },
]

def eatingOut():
    thing = random.choice(badDecisions)
    thing["price"] = exec(thing["price"])
users = {
    "user1": [],
    "user2": [],
    "user3": []
}


def main():
    today = datetime.datetime.now()
    prev = today - datetime.timedelta(days=200)
    days = [day for ]
    file = open("something.json", "w")
    json.dump(users, file,indent=4)