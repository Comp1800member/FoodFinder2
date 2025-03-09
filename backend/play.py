import discord
from discord.ext import commands, tasks
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("foodfinder_key.json")  # <-- Update this path
firebase_admin.initialize_app(cred)
db = firestore.client()

TOKEN = ""

# Initialize the bot with necessary intents
intents = discord.Intents.default()
intents.guild_scheduled_events = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(minutes=1)
async def remove_expired_events():
    curr_time = datetime.datetime.now(datetime.timezone.utc)
    print(f"Checking for expired events at {curr_time}...")

    events_ref = db.collection("events")
    expired_events = events_ref.where("end_time", "<", curr_time).stream()

    for event in expired_events:
        print(f"Event deleted: {event.id} @ {curr_time}")
        event.reference.delete()

# Function to store event information
def store_event(event):
    event_data = {
        "id": event.id,
        "guild_id": event.guild.id,
        "name": event.name,
        "description": event.description,
        "start_time": event.start_time.isoformat(),
        "end_time": event.end_time.isoformat(),
        "location": event.location,
        "creator": str(event.creator),
        "url": event.url
    }
    db.collection("events").document(str(event.id)).set(event_data)
    print(f"Event '{event.name}' has been stored in Firestore.")

async def fetch_all_events_for_guild(guild):
    events = guild.scheduled_events
    for event in events:
        store_event(event)

# Event listener for new events
@bot.event
async def on_scheduled_event_create(event):
    print(f"New event detected: {event.name}")
    store_event(event)

@bot.event
async def on_scheduled_event_update(before, after):
    db.collection("events").document(str(before.id)).delete()
    store_event(after)

@bot.event
async def on_scheduled_event_delete(event):
    db.collection("events").document(str(event.id)).delete()

# Run the bot
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    for guild in bot.guilds:
        print(f"Fetching events for guild: {guild.name}")
        await fetch_all_events_for_guild(guild)
    remove_expired_events.start()

bot.run(TOKEN)
