import json
import requests


def to_red():
    secrets = open("home/pi/shared_files/secrets.json")
    secrets = json.load(secrets)
    token = secrets["API_KEY_PI_2"]
    label_id = secrets["Lamp2"]

    headers = {"Authorization": "Bearer %s" % token, }

    payload = {
        "states": [
            {
                "selector": f"id:{label_id}",
                "power": "on",
                "color": "red",
                "brightness": 0.2,
                "duration": 3600,
            }
        ]
    }

    response = requests.put('https://api.lifx.com/v1/lights/states',
                            data=json.dumps(payload), headers=headers)
