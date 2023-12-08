#app id : 1180120052050182155
#puKey:1cd58d12f4a8bcec59f4328cce215a71aeee6d8c8bb80e79c35ea205ee4db247
import discord
import os
from openai import OpenAI


file = input("Enter 1, 2, or 3 for loading the chat:\n ")
match(file):
    case "1":
      file = "chat1.txt"
    case "2":
      file = "chat2.txt"
    case "3": 
      file = "chat3.txt"
    case _:
      print("Invalid choice.")
      exit()
with open(file, "r") as f:
  chat = f.read() 

openai_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_key)
token = os.getenv("SECRET_KEY")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        try:
          chat += f"{message.author}: {message.content}\n"
          print(f'Message from {message.author}: {message.content}')
          if self.user != message.author:
             if self.user in message.mentions:
                print(chat)
                channel = message.channel
                response = openai_client.completions.create(
                   model="text-davinci-003",
                   prompt=f"{chat}\nAarohiGPT: ",
                   temperature=1,
                   max_tokens=256,
                   top_p=1,
                   frequency_penalty=0,
                   presence_penalty=0
               )
                messageToSend = response.choices[0].text
                await channel.send(messageToSend)
        except Exception as e:
         print(e)
         chat = ""
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
if token is not None:
  client.run(token)
else:
  print("No token found")