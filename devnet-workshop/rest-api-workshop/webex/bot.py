import os
import sys

import requests
from dotenv import load_dotenv
from flask import Flask, request
from requests_toolbelt.multipart.encoder import MultipartEncoder

# put your token in a file `.env`
# BOT_TOKEN=<your token>
load_dotenv()

access_token = os.getenv("BOT_TOKEN")
base_url = "https://webexapis.com"

if access_token is None:
    print("Missing access token")
    sys.exit(1)

headers = {
    "Authorization": "Bearer {}".format(access_token),
    "Content-Type": "application/json",
}

app = Flask(__name__)

# Dynamic webhook creation
# Ngrok runs a local REST API
# the bot can use the api to get the random generated url
# and create a webhook or updating an existing one


def get_public_url() -> str:
    res = requests.get("http://localhost:4040/api/tunnels")
    res.raise_for_status()
    tunnels = res.json()
    return tunnels["tunnels"][0]["public_url"]


# update webhook


def create_webhook(public_url: str) -> None:
    url = base_url + "/v1/webhooks"
    body = {
        "name": "webex-bot",
        "targetUrl": public_url + "/webhook",
        "resource": "messages",
        "event": "created",
    }
    res = requests.post(url, headers=headers, json=body)

    if res.status_code != 200:
        print("error creating webhook continuing anyways")
        print(res.json())


print("connecting to ngrok local api...")
ngrok_url = get_public_url()
print("found ngrok public url", ngrok_url)

print("attempting to update webhook", sys.argv[1])
create_webhook(ngrok_url)
print("updated webhook successfully")


def get_room_details(id: str) -> dict:
    url = base_url + "/v1/rooms/" + id
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


def get_self_details() -> dict:
    url = base_url + "/v1/people/me"
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


def get_message_details(id: str) -> dict:
    url = base_url + "/v1/messages/" + id
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


def get_catfact() -> str:
    """Get a cat fact from catfact.ninja and return it as a string.

    Functions for Soundhound, Google, IBM Watson, or other APIs can be added
    to create the desired functionality into this bot.

    """
    response = requests.get("https://catfact.ninja/fact")
    response.raise_for_status()
    json_data = response.json()
    return json_data["fact"]


def get_image():
    url = "https://cataas.com/cat"

    res = requests.get(url)

    res.raise_for_status()

    return res.content


def send_message(text: str, room_id: str) -> None:
    url = base_url + "/v1/messages"
    res = requests.post(url, headers=headers, json={"text": text, "roomId": room_id})

    res.raise_for_status()

    print(res.json())


def send_image(content, room_id: str) -> None:
    m = MultipartEncoder(
        {
            "roomId": room_id,
            "text": "Here is your picture",
            "files": ("cat.png", content, "image/png"),
        }
    )

    r = requests.post(
        "https://webexapis.com/v1/messages",
        data=m,
        headers={
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": m.content_type,
        },
    )

    r.raise_for_status()

    print(r.json())


def execute_cmd(cmd: str, room_id: str) -> str:

    if cmd.lower().startswith("/cat"):
        fact = get_catfact()
        send_message(fact, room_id)
    elif cmd.lower().startswith("/image"):
        image = get_image()
        send_image(image, room_id)
    else:
        return "Sorry, I didn't understand"


@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.json

    print("\n")
    print("WEBHOOK POST RECEIVED:")
    print(json_data)
    print("\n")

    # This is a VERY IMPORTANT loop prevention control step.
    # If you respond to all messages...  You will respond to the messages
    # that the bot posts and thereby create a loop condition.
    me = get_self_details()
    if json_data["data"]["personId"] == me["id"]:
        # Message was sent by me (bot); do not respond.
        return "OK"

    # get room
    room_id = json_data["data"]["roomId"]
    room = get_room_details(room_id)

    # get message
    message_id = json_data["data"]["id"]
    message = get_message_details(message_id)

    # print(room)
    # print(message)

    # parse message
    execute_cmd(message["text"], room_id)

    return "OK"
