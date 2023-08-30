import asyncio
import discord
import telethon
import yaml

from discord.ext import commands
from telethon import TelegramClient, events

with open('config.yml', 'rb') as x:
    config = yaml.safe_load(x)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def forward_to_discord(event):
    message = event.message
    if message.chat_id == config["input_group_id"]:
        discord_channel = bot.get_channel(config["discord_channel"])
        discord_message = f"**{message.sender.first_name}:** {message.text}"
        await discord_channel.send(discord_message)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

async def main():
    async with TelegramClient("test1", config["api"], config["hash"]) as client:
        client.add_event_handler(forward_to_discord, events.NewMessage)

        print("bot started")
        await client.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(bot.start(config["discord_token"]))
    loop.run_forever()
