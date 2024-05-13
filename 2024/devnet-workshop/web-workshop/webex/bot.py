from flask import Flask, request
from dotenv import load_dotenv

import requests
import os
import sys

load_dotenv()

access_token = os.getenv("BOT_TOKEN")
base_url = 'https://webexapis.com'

if access_token is None:
    print("Missing access token")
    sys.exit(1)

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

app = Flask(__name__)


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


def send_message(text: str, room_id: str) -> None:
    url = base_url + "/v1/messages/"
    res = requests.post(url, headers=headers, json={
                        "text": text, "roomId": room_id})

    res.raise_for_status()

    print(res.json())


def execute_cmd(cmd: str) -> str:
    if cmd.lower().startswith("/cat"):
        return get_catfact()
    else:
        raise Exception("unknonw command")


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
    response = execute_cmd(message["text"])

    # send response to user
    send_message(response, room_id)

    return "OK"
