# crypto-slackbot

A simple bot to get the price of cryptocurrencies, written with python. And it is compatible with python2.7 and python 3.x. 

<img src="https://i.imgur.com/9Re8rTR.png">

## Dependency

slackclient, requests

## Get Started

1. Create a Slack App to recieve an API token for your bot. You can follow this [tutorial](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html).

2. Modify your bash
```
export SLACK_BOT_TOKEN='your bot user OAuth access token here'
```

3. Install Packages
```
pip install slackclient
pip install requests
```

4. Start the bot

```
python bot.py
```

5. Invite your bot user to the channel you want to use.

6. Enjoy! Just type `bot btc`, `bot xrp` ... whatever. 

## Usage in slack

`bot [coin]`: Get the price of coin. And coin's name should be abbreviation. Example: `bot eth`, `bot xrp`, `bot ltc`.


