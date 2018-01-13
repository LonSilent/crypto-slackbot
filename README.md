# crypto-slackbot

A simple bot to get the price of cryptocurrencies, written with python. And it is compatible with python2.7 and python 3.x. 

## Dependency

slackclient, requests

## Get Started

1. Modify your bash
```
export SLACK_BOT_TOKEN='your bot user OAuth access token here'
```

2. Install Packages
```
pip install slackclient
pip install requests
```

3. Start the bot

```
python bot.py
```

4. Invite your bot user to the channel you want to use.

5. Enjoy! Just type `bot btc`, `bot xrp` ... whatever. 

## Usage in slack

`bot [coin]`: Get the price of coin. And coin's name should be abbreviation. Example: `bot eth`, `bot xrp`, `bot ltc`.


