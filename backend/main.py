import uvicorn
from discord.ext import commands, tasks
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import discord
import asyncio
from datetime import datetime, timezone, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from api import perplex
from prophet import Prophet
import matplotlib.pyplot as plt
from openai import OpenAI
import os


prompt_string = ""

# Initialize Firebase
cred = credentials.Certificate("foodfinder_key.json")  # <-- Update this path
firebase_admin.initialize_app(cred)
db = firestore.client()

TOKEN = "MTMwMzYyNzcyNTY3MTQ5Nzc5MA.G7SAMN.M9y1g5sqgNDpy6oeKZU5z15Lymj60mp7F2BGMM"


# Initialize the bot with necessary intents
intents = discord.Intents.default()
intents.guild_scheduled_events = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- FastAPI Setup ---
app = FastAPI(debug=True)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Event(BaseModel):
    id: int
    guild_id: int
    name: str
    description: str
    start_time: str
    end_time: str
    location: str
    creator: str
    url: str

class Events(BaseModel):
    events: List[Event]


# @tasks.loop(minutes=1)
# async def remove_expired_events():
#     curr_time = datetime.datetime.now(datetime.timezone.utc)
#     print(f"Checking for expired events at {curr_time}...")
#
#     events_ref = db.collection("events")
#     expired_events = events_ref.where("end_time", "<", curr_time).stream()
#
#     for event in expired_events:
#         print(f"Event deleted: {event.id} @ {curr_time}")
#         await event.reference.delete()

# Function to store event information
def store_event(event):

    print(f"Event '{event.name}' has been stored in Firestore.")
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

async def fetch_all_events_for_guild(guild):
    events = guild.scheduled_events
    for event in events:
        prompt = (f"Here is the event: {event} {event.description}. There will be free food "
              f"at this event!. Based on the message return a STRING, responding with 'Y' "
              f"if the message contains or implies that "
              f"there is free food or 'N' if otherwise. "
              f"ONLY RETURN A STRING WITH 'Y' or 'N', DO NOT GIVE ANY REASONING OR INFO WHEN RESPONDING")
        response = perplex.get_ai_response(prompt=prompt)
        response_content = response.choices[0].message.content.strip()  # Access and clean the content

        if response_content == 'Y':
            store_event(event)

@bot.event
async def on_scheduled_event_update(before, after):
    db.collection("events").document(str(before.id)).delete()
    store_event(after)

@bot.event
async def on_scheduled_event_delete(event):
    db.collection("events").document(str(event.id)).delete()

"""

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        ),
    },
    {
        "role": "user",
        "content": (
            "How many stars are in the universe?"
        ),
    },
]

client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="sonar-pro",
    messages=messages,
)
"""

@bot.event
async def on_scheduled_event_create(event):
    print(f"New event detected: {event.name}")
    print(f"The event: {event} {event.description}")
    prompt = (f"Here is the event: {event} {event.description}. There will be free food "
              f"at this event!. Based on the message return a STRING, responding with 'Y' "
              f"if the message contains or implies that "
              f"there is free food or 'N' if otherwise. "
              f"ONLY RETURN A STRING WITH 'Y' or 'N', DO NOT GIVE ANY REASONING OR INFO WHEN RESPONDING")
    print(prompt)
    response = perplex.get_ai_response(prompt=prompt)
    response_content = response.choices[0].message.content.strip()  # Access and clean the content
    print(f"Response content: {response_content}")  # Check the actual content

    if response_content == 'Y':
        store_event(event)

@bot.event
async def on_message(message):
    print("received message")
    prompt = (f"Here is the message: {message.content}. Based on the message "
              f"return a json object with the following keys: "
              f"event, name, description, start_time, end_time, "
              f"location, creator/event host/club name, "
              f"guild/server name, "
              f"if theres a url then add url. For the event key, "
              f"respond with a string "
              f"containing whether the message is about an event "
              f"(if the message appears to sound like a planned public or social gathering with free food, "
              f"then only put either 'Y' for yes or 'N' for no). "
              f"If you cant find information for what the value most likely is then leave it "
              f"as 'n/a' as the value in the json object. Please try to answer with the most likely "
              f"approximate answer instead of relying on 'n/a. "
              f"ONLY GIVE JSON OBJECT, DO NOT GIVE ANY REASONING OR INFO WHEN RESPONDING")


    print(f"{prompt}")
    response = perplex.get_ai_response(prompt=prompt)
    print(f"response received {response}")
    df = pd.read_json(response)
    print(df[0])
    if df[0] == 'Y':
        print("message was an event")
        new_event = discord.ScheduledEvent(
            name=df[1], # event_name
            description=df[2], # event_description,
            start_time=df[3], # start_time,
            end_time=df[4], # end_time,
            location=df[5], # location,
            creator=df[6], # message.author,
            guild=df[7], # message.guild,
            url=df[8], # "http://example.com/"  # Set this dynamically if needed
        )

        # Store the new event in Firestore
        store_event(new_event)

        # Send a confirmation message
        await message.channel.send(f"New event '{df[1]}' created!")

    # Make sure to process commands
    await bot.process_commands(message)


# Run the bot
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    for guild in bot.guilds:
        print(f"Fetching events for guild: {guild.name}")
        await fetch_all_events_for_guild(guild)
    # remove_expired_events.start()




# --- FastAPI Routes ---
@app.get("/events", response_model=Events)
def get_events():
    events_ref = db.collection("events").stream()
    events_list = [
        Event(
            id=event.id,
            guild_id=event.to_dict().get("guild_id", "N/A"),
            name=event.to_dict().get("name", "Unnamed Event"),
            description=event.to_dict().get("description", ""),
            start_time=event.to_dict().get("start_time", ""),
            end_time=event.to_dict().get("end_time", ""),
            location=event.to_dict().get("location", "Unknown"),
            creator=event.to_dict().get("creator", "Unknown"),
            url=event.to_dict().get("url", ""),
        )
        for event in events_ref
    ]

    return Events(events=events_list)

def predict_future():
#replace this with actual data
    events_ref = db.collection("events").stream()
    events_data = [
        Event(
            id=event.id,
            guild_id=event.to_dict().get("guild_id", "N/A"),
            name=event.to_dict().get("name", "Unnamed Event"),
            description=event.to_dict().get("description", ""),
            start_time=event.to_dict().get("start_time", ""),
            end_time=event.to_dict().get("end_time", ""),
            location=event.to_dict().get("location", "Unknown"),
            creator=event.to_dict().get("creator", "Unknown"),
            url=event.to_dict().get("url", ""),
        )
        for event in events_ref
    ]

    df = pd.DataFrame(events_data)
    df['ds'] = pd.to_datetime(df['start_time'])
    df['y'] = 1  # Each event counts as one occurrence

    df = df.groupby('ds').sum().reset_index()

    model = Prophet()
    model.fit(df)

    # DataFrame for future dates (e.g., next 30 days)
    future = model.make_future_dataframe(periods=30)

    forecast = model.predict(future)

    fig = model.plot(forecast)
    plt.title("Predicted Free Food Events")
    plt.xlabel("Date")
    plt.ylabel("Number of Events")
    plt.show()
@app.get("/upcoming-events", response_model=Events)
def get_upcoming_events():
    events_ref = db.collection("events").stream()

    # Get current UTC time
    now = datetime.now(timezone.utc)
    two_days_later = now + timedelta(days=2)

    events_list = []
    for event in events_ref:
        event_data = event.to_dict()

        # Extract start_time and convert it to datetime
        start_time_str = event_data.get("start_time", "")
        try:
            start_time = datetime.fromisoformat(start_time_str)
        except ValueError:
            continue  # Skip events with invalid date format

        # Filter: Only include events within the next 2 days
        if now <= start_time <= two_days_later:
            events_list.append(
                Event(
                    id=event.id,
                    guild_id=event_data.get("guild_id", "N/A"),
                    name=event_data.get("name", "Unnamed Event"),
                    description=event_data.get("description", ""),
                    start_time=start_time_str,
                    end_time=event_data.get("end_time", ""),
                    location=event_data.get("location", "Unknown"),
                    creator=event_data.get("creator", "Unknown"),
                    url=event_data.get("url", ""),
                )
            )
    return Events(events=events_list)
@app.get("/")
def say_hello():
    return {"hello": "world"}

async def main():
    # Start FastAPI server in a separate task
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)

    # Run FastAPI and Discord bot concurrently
    await asyncio.gather(
        server.serve(),
        bot.start(TOKEN)
    )

if __name__ == "__main__":
    #predict_future()
    asyncio.run(main())
