import discord
from discord.ext import commands, tasks
import json
import sqlite3
import datetime

conn = sqlite3.connect('food.db')
cursor = conn.cursor()

# Create table for storing events if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    guild_id TEXT,
    name TEXT,
    description TEXT,
    start_time TEXT,
    end_time TEXT,
    location TEXT,
    creator TEXT,
    url TEXT
)
''')
conn.commit()
configs = 'config.json'

TOKEN = ""

#updates token to token in config file, probably shouldn't push to github but I'll leave it for now.
with open(configs, 'r') as file:
    config = json.load(file)
    TOKEN = config['DISCORD_BOT_TOKEN']

# Initialize the bot with necessary intents
intents = discord.Intents.default()
intents.guild_scheduled_events = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Path to store event details
EVENTS_FILE = "events.json"

# Load existing events if they exist
try:
    with open(EVENTS_FILE, "r") as file:
        stored_events = json.load(file)
except FileNotFoundError:
    stored_events = {}

@tasks.loop(minutes=1)
async def remove_expired_events():
    curr_time = datetime.datetime.now(datetime.timezone.utc)
    print(f"Checking for expired events at {curr_time}...")
    curr_time_formatted = curr_time.strftime('%Y-%m-%d %H:%M:%S.%f+00:00')
    print(curr_time_formatted)

    cursor.execute('''SELECT * FROM events WHERE end_time < ?''', (curr_time_formatted,))
    events_to_delete = cursor.fetchall()

    # Print or log the events that will be deleted
    for event in events_to_delete:
        print(f"Event deleted: {event} @ {curr_time}")

    cursor.execute('''
    DELETE FROM events WHERE end_time < ?
    ''', (curr_time_formatted,))
    conn.commit()

# Function to store event information
def store_event(event):
    cursor.execute('''
    INSERT OR REPLACE INTO events (id, guild_id, name, description, start_time, end_time, location, creator, url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        event.id, event.guild.id, event.name, event.description,
        str(event.start_time), str(event.end_time), event.location,
        str(event.creator), event.url
    ))
    conn.commit()
    print(f"Event '{event.name}' has been stored in the database.")

async def fetch_all_events_for_guild(guild):
    events = guild.scheduled_events
    for event in events:
        store_event(event)

# Event listener for new events
@bot.event
async def on_scheduled_event_create(event):
    print(f"New event detected: {event.name}")
    print("Event attributes:", dir(event))
    try:
        print(f"Event Start time: {event.start_time}")
    except Exception as e:
        print(e)
    store_event(event)

@bot.event
async def on_scheduled_event_update(before, after):
    cursor.execute('DELETE FROM events WHERE id = ?', (before.id,))
    store_event(after)

@bot.event
async def on_scheduled_event_delete(event):
    cursor.execute('DELETE FROM events WHERE id = ?', (event.id,))


# Run the bot
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    for guild in bot.guilds:
        print(f"Fetching events for guild: {guild.name}")
        await fetch_all_events_for_guild(guild)
    remove_expired_events.start()

bot.run(TOKEN)