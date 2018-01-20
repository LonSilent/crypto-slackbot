from __future__ import print_function, division
import os
import time
import re
from slackclient import SlackClient
import json
from collections import defaultdict
from api import collect_data

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
COMMAND = "bot "
ENABLE_MAICOIN = False

def parse_bot_commands(slack_events):
    for event in slack_events:
        # print(event)
        if event["type"] == "message" and not "subtype" in event:
            message = event['text'].lower()
            channel = event['channel']
            # check and pass symbol
            if message.startswith(COMMAND):
                return message.split(' ')[-1], channel
    return None, None

def handle_command(symbol, channel):
    response = collect_data(symbol, enable_maicoin=ENABLE_MAICOIN)

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
    )

if __name__ == "__main__":

    if slack_client.rtm_connect(with_team_state=False):
        print("Bot connected and running!")
        bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            symbol, channel = parse_bot_commands(slack_client.rtm_read())
            if symbol:
                handle_command(symbol, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")