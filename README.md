<h1 align='center'>
  Dollar-Cost Averaging Strategy with lemon.markets API 🍋 
</h1>

This is a public [lemon.markets](https://lemon.markets) repository that outlines a dollar-cost averaging (DCA) strategy using our API. To get a general understanding of the API, please refer to our [documentation](https://docs.lemon.markets). 

## Instructions for Use

This script can be used as a starting point to implement your own dollar-cost averaging strategy and to set up Telegram notifications. If implemented as is, the script will trade one share of the Xtrackers MSCI World Swap ETF 1C weekly. 

A walk-through of this script can be found in this blog-post: /todo

### Environment Variables

You'll notice that the script uses several environment variables. Please define the following in an .env file or within your IDE:

* `TOKEN_KEY` - Your lemon.markets access token
* `CLIENT_ID` - Your client ID
* `CLIENT_SECRET` - Your client secret
* `MIC` - Market Idenitfier Code of chosen Trading Venue
* `BASE_URL` - The base URL of our paper money API
* `AUTH_URL` - The authentication URL of our API
* `SPACE_UUID` - UUID of your space

### Telegram Bot

In this repository, we're using [send-telegram](https://pypi.org/project/telegram-send/) to send messages using Telegram. Install Telegram on your smartphone and message `/newbot` to @BotFather to get started. BotFather will give you a token, which can be used to interact with your bot. 

send-telegram can be installed in your terminal using pip as follows:
```
pip install telegram-send
```
It can be configured with:
```
telegram-send --configure 
```
You will be prompted to fill in the token you received, at which point you will receive a password. Upon sending this password to your bot using the Telegram app, your script will be configured with your bot. Full installation instructions for send-telegram can be found [here](https://pypi.org/project/telegram-send/#installation).

You can now use send-telegram with the command:
```
telegram_send.send(messages=["Hello!"])
```

## Interested in contributing?

This (and all lemon.markets open source projects) is work in progress. If you are interested in contributing to this repository, simply create a PR and/or contact us at [support@lemon.markets](mailto:support@lemon.markets).

Looking forward to building lemon.markets with you 🍋
