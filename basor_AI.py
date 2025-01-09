import google.generativeai as genai
from dotenv import load_dotenv
import os
import discord

# Load environment variables
load_dotenv()

# Create an intents object
intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read message content

# Pass intents to the Client constructor
client = discord.Client(intents=intents)

# Get the API keys from environment variables
basor = os.getenv('BASOR_TOKEN')
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Configure Google Generative AI
genai.configure(api_key=gemini_api_key)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Respond to a custom command
    if message.content.startswith('!halo basor'):
        await message.channel.send('waalikumsalam, seperti informasi yg saya infokn saat kelas berlangsung, silahkan dipersiapan untuk progress projekny')
    
    # Respond to another custom command
    if message.content.startswith('!bye'):
        await message.channel.send('Untuk progress tidak perlu ke kelas, langsung k ruang dosen sesuai jadwal perkuliahan.')
    
    # Call Google AI API when a message starts with '!ask'
    if message.content.startswith('!ask'):
        # Extract the question from the message (after '!ask')
        question = message.content[len('!ask '):]

        # Generate a response from Google Generative AI
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(question)
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"Sorry, I couldn't generate a response. Error: {e}")

# Run the bot
client.run(token=basor)
