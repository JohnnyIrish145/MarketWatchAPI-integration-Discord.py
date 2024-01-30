import discord
from discord.ext import commands, tasks
from discord import Interaction
from datetime import datetime
import pytz # Timezones
import asyncio # For discord bot reconnect loop
import time
from marketwatch import MarketWatch # Marketwatch api you can download here: https://github.com/kevindong/MarketWatch_API
import stock_names_sort # stock_names_sort.py that queries the Yahoo finance database
from datetime import time as houring # For defining when the @task.loop() runs
game_name = "" # Marketwatch.com game name you want to know about
marketwatch = MarketWatch("email", "password") # Logs in to Marketwatch.com
import matplotlib.pyplot as plt # Matplotlib for ploting stock prices on a graph
import yfinance # Yahoo finance for getting market data

intents = discord.Intents.all()
client = discord.ext.commands.Bot(command_prefix="$", intents=intents, sync_commands=True)

TOKEN = "discord bot token"

OWNER = 727764636904194060 # owner/admin user id as int()
# Channels
console = # Console channel id
open_role = # Role id that pings when NYSE and NASDAQ opens
close_role = # Role id that pings when NYSE and NASDAQ closes
NYSE = # Channel id where open and close roles are pinged
leaderboard = # Channel id where leaderboards are periodiclly displayed
server_id = # The server id where your users get pinged and leaderboard shown
# Channels
colour_stripe = discord.Colour.gold() # Change to your desirable colour

def leader(): # Gets the current games top 20 leaderboard and formats it into a discord embed
    leaderboard = marketwatch.get_leaderboard(game_name) # Fetches the leaderboard from your game on Marketwatch.com 
    embed = discord.Embed(
        colour=discord.Colour.dark_teal(),
        title=f'Leaderboard for the "{game_name}" game',
        description = "" # Sets the description as an empty string to easliy add new elements with the loop
    )
    embed.set_footer(text="Made by Johnnyirish")
    num = 0 # Sets a varible to 0 to keep track and limit the discord embed message size
    for i in leaderboard: # for every person in the leaderboard
        num+=1 # Keeps track of current amount of players on the discord embed leaderboard message
        if num > 1 and num < 22:
            rank = i["rank"] # Gets the current players rank
            player = i["player"] # Gets the current players name
            portfolio_value = i["portfolio_value"] # Gets the players current networth
            transactions = i["transactions"] # Gets the number of transactions the player has made in the current game
            url = i["player_url"] # Gets the players Marketwatch.com portfolio page url
            embed.description += f'{rank}. [{player}]({url}) - {portfolio_value} with {transactions} transactions.\n'
        elif num == 20 or num > 20: # returns/stops adding people to the embed when it reaches top 20 players
            return embed

@client.event
async def on_ready(): # Executes when the bot starts up or reboots
    newYorkTz = pytz.timezone("America/New_York") # Sets current timezone to New York
    timeInNewYork = datetime.now(newYorkTz) # Gets the current time in New York
    current_time = timeInNewYork.strftime("%a:%H:%M:%S") # Formats the current time in New York
    print("-----") # Divider
    print(f"{client.user} is now running") # Prints to console that bot is running
    print("Time: ", current_time) # Prints the time when the bot starts up
    await client.tree.sync() # Syncs and updates all active /commands to discord
    embed = discord.Embed(
        colour=colour_stripe,
        description="Console",
        title=f"{client.user} is now running")
    await client.get_channel(console).send(embed=embed) # Sends a discord message to "console" channel when bot goes online or reboots
    
    opening.start() # Starts @task.loop()
    closing.start() # Starts @task.loop()

# Basic error handiling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound): # Ignores random ctx command errors
        return
    embed = discord.Embed(
            colour=discord.Colour.green(),
            title="An error occurred")
    await ctx.send(embed=embed) # Sends an error message
    await client.get_channel(console).send(error) # Sends error to error channel

#Sets timezone to New York 
utc = pytz.timezone("America/New_York")

time = houring(hour=9, minute=29, tzinfo=utc) # Opening time of NYSE and NASDAQ (If it doesn't work, try: "datetime.time(hour=9, minute=29, tzinfo=utc)")
time2 = houring(hour=15, minute=59, tzinfo=utc) # Closing time of NYSE and NASDAQ (If it doesn't work, try: "datetime.time(hour=15, minute=59, tzinfo=utc)")

# Task for when NYSE and NASDAQ open
@tasks.loop(time=time) # Checks if the current time is equal to the opening time
async def opening():
    my_server = client.get_guild(server_id) # Gets the server by id
    role = my_server.get_role(open_role).mention # Gets open_role
    
    utc2 = pytz.timezone("America/New_York") # Sets timezone to New York 
    timeInNewYork = datetime.now(utc2)
    weekday = timeInNewYork.strftime("%w") # Gets a 0 - 6 number based on what day of the week it is in New York right now
    
    if int(weekday) != 6 and int(weekday) != 0: # Checks if day isin't Saturday or Sunday
        await client.get_channel(NYSE).send(f"{role} NYSE is about to open!") # Pings the open_role when NYSE and NASDAQ open in the "NYSE" channel
    
    await client.get_channel(leaderboard).send(embed=leader()) # Sends the leaderboard to the leaderboard channel everyday

# Task for when NYSE and NASDAQ close
@tasks.loop(time=time2) # Checks if the current time is equal to the closing time
async def closing():
    my_server = client.get_guild(server_id) # Gets the server by id
    role = my_server.get_role(close_role).mention # Gets close_role
    
    utc2 = pytz.timezone("America/New_York") # Sets timezone to New York 
    timeInNewYork = datetime.now(utc2)
    weekday = timeInNewYork.strftime("%w") # Gets a 0 - 6 number based on what day of the week it is in New York right now

    if int(weekday) != 6 and int(weekday) != 0: # Checks if day isin't Saturday or Sunday
        await client.get_channel(NYSE).send(f"{role} NYSE is about to close!") # Pings the close_role when NYSE and NASDAQ close in the "NYSE" channel
    
    await client.get_channel(leaderboard).send(embed=leader()) # Sends the leaderboard to the leaderboard channel everyday

# Allows users to get a leaderboard of the game with a /command
@client.tree.command(name = "leaderboard", description="Get the current leaderboard of the game")
async def leaderboard(interaction : discord.Interaction):
    
    await interaction.response.send_message(embed=leader()) # Fethces the top 20 players in a game and replies to the user as a discord embed

# Allow users to get the current price of a stock and a graph of that stocks highest prices for the past 5
@client.tree.command(name = "price", description="Get the current price of a stock")
async def price(interaction : discord.Interaction, stock_name: str):
    
    stock_name_search_result = stock_names_sort.sort(stock_name).upper() # Returns a company code from Yahoo finance, for example "Apple" --> "AAPL"
    
    if stock_name_search_result == "NOT FOUND": # Handles if the stock wans't found in Yahoo finance database
        embed = discord.Embed(
                colour=colour_stripe,
                title=f'Sorry, but we could not find "{stock_name}"')
        await interaction.response.send_message(embed=embed) # Replies to the user if stock_name wasn't found
    else:
        stock_info = yfinance.Ticker(stock_name_search_result) # Fethces data about the stock on Yahoo finance
        
        data = yfinance.download(stock_name_search_result, period="5d") # Downloads 5 days of data about that stock on Yahoo finance
        data2 = data['High'] # Gets all the highest prices of each day
        data2.plot() # Plots each price on a graph 
        plt.title(f"{stock_name_search_result} Highest Stock Prices over 5 days") # Sets a header/title of the graph
        plt.xlabel("Days") # Sets a x value title/label of the graph
        plt.ylabel("Price") # Sets a y value title/label of the graph

        plt.savefig("sine_wave.jpg") # Saves the graph as a .jpg file in the current directory as "sine_wave.jpg"
        plt.clf() # Clears all the graph data for future use
        file = discord.File("sine_wave.jpg", filename="sine_wave.jpg") # Adds a discord file to the message called 
        
        # Gets the current price of "stock_name"
        price = stock_info.info["currentPrice"]
        
        stock_url = stock_name_search_result.lower()
        url = f"https://www.marketwatch.com/investing/stock/{stock_url}" # Gets the Marketwatch.com url of that stock
        embed = discord.Embed(
        colour=colour_stripe,
        description=f"[{stock_name_search_result}]({url}) - ${price}") # Shows the current price of the stock with a hyperlink to that stocks Marketwatch.com page
        embed.set_image(url="attachment://sine_wave.jpg") # Sets the discord embed image to the graph .jpg image
        await interaction.response.send_message(file=file, embed=embed) # Replies to the user with all the infomation as a discord embed

# Reconnect loop for when the bot crashes
async def reconnect_loop():
    while True:
        await asyncio.sleep(1)
        if client.is_closed():
            print('Bot is disconnected, attempting to reconnect...')
            try:
                await client.start(TOKEN)
                print('Reconnect successful.')
                break
            except Exception as e:
                print(f'Reconnect failed, {e}, retrying in 5 seconds...')
                await asyncio.sleep(5)

async def main():
    try:
        await client.start(TOKEN)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal exception {e}, running reconnect loop.")
        await reconnect_loop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
