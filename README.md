# MarketWatch API integration with Discord.py
A python discord bot that uses the MarketWatch API wrapper for interacting with the games section of MarketWatch.

# Features
* `/price` - Allow users to get the current price of a stock and a graph of that stocks highest prices for the past 5.
* `/leaderboard` - Allows users to get a leaderboard of the top 20 players in the MarketWatch.com game.
* Allows users to be ping when NYSE and NASDAQ opens and closes.
* Periodically sends the current leaderboard of the MarketWatch.com game.

# Setup
### To setup the bot properly, make sure to specify:
* `TOKEN = ""` - put in your discord bot token, you can get yours here: https://discord.com/developers/applications.
* `marketwatch = MarketWatch("email", "password")` - put in your Marketwatch.com information to log into your Marketwatch.com account.
* `game_name = ""` - put in the Marketwatch.com game that the bot will watch and get all it's data from.
* `console = ` - discord console channel id, where the bot sends all the errors and sends a message when it turns on.
* `leaderboard = ` - discord leaderboard channel id, where the current leaderboard is sent periodically.
* `server_id = ` - the main discord server where all the channels are.
* `NYSE` - discord channel id where your "open" and "close" roles are pinged when NYSE and NASDAQ opens and closes.
* `open_role = ` discord role id which is pinged when NYSE and NASDAQ opens.
* `close_role = ` discord role id which is pinged when NYSE and NASDAQ closes.
* `OWNER = ` - put in your discord user id here.

# Files and miscellaneous
* `stock_names_sort.py` - queries the yahoo finance database for it's company stock name, for example: "Apple" --> "AAPL".
* `main.py` - defines the discord bot, the roles and channels it uses, handles the front and backend.
* `sine_wave.jpg` - an example of the output file when you search for the price with `/price`
### Libraries used:
* `discord.py` - Discord bot.
* `datetime` - time handiling.
* `pytz` - Timezones.
* `asyncio` - discord bot reconnection loop.
* `time` - discord bot reconnection loop timeout.
* `marketwatch` - Marketwatch api wrapper you can download here: https://github.com/kevindong/MarketWatch_API.
* `datetime` - defines when the @task.loop() runs.
* `matplotlib.pyplot` - Matplotlib for ploting stock prices on a graph.
* `yfinanc` - Yahoo finance for getting market data.
* `requests` - allows you to query the yahoo finance database.
You can find more info on the MarketWatch API wrapper here: https://github.com/kevindong/MarketWatch_API.
