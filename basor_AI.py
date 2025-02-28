import google.generativeai as genai
from dotenv import load_dotenv
import os
import discord


load_dotenv()


intents = discord.Intents.default()
intents.message_content = True  

# Pass intents to the Client constructor
client = discord.Client(intents=intents)


basor = os.getenv('BASOR_TOKEN')
gemini_api_key = os.getenv('GEMINI_API_KEY')


genai.configure(api_key=gemini_api_key)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

   
    if message.content.startswith('!halo basor'):
        await message.channel.send('waalikumsalam, saya basor AI')
    
    
    if message.content.startswith('!bye'):
        await message.channel.send('Untuk progress tidak perlu ke kelas, langsung k ruang dosen sesuai jadwal perkuliahan.')
    
   
    if message.content.startswith('!ask'):
        
        question = message.content[len('!ask '):]

     
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(question)
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"Sorry, I couldn't generate a response. Error: {e}")


client.run(token=basor)