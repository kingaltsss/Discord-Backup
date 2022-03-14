import discord
from discord.ext import commands
import asyncio
import httpx
import json


config = json.load(open("config.json"))
bot = commands.Bot(command_prefix=config['prefix'], self_bot=True)


@bot.command(name="backupfriends")
async def backupfriends(ctx):
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://discord.com/api/v9/users/@me/relationships", headers={"Authorization": config['token']})

    with open("./friends.txt", "a") as friendsfile:
        for user in resp.json():
            if user['type'] == 1:   
                try:
                    friendsfile.write(f"{user['user']['username']}#{user['user']['discriminator']}\n")
                except:
                    friendsfile.write(f"{user['user']['username'].encode()}#{user['user']['discriminator']}\n")
    await ctx.send(f"Saved all friends.")


@bot.command(name="backupservers")
async def backupservers(ctx):
    count = 0
    with open("servers.txt", "a") as serversfile:
        for guild in bot.guilds:
            count += 1
            channels = await guild.fetch_channels()
            channel = discord.utils.get(channels, type=discord.ChannelType.text)
            if discord.Permissions(channel.permissions_for(channel.guild.me).value).create_instant_invite:
                invite = await channel.create_invite()
                serversfile.write(f"{invite.url}\n")
                print(f"{invite.url}, guild number {count}/{len(bot.guilds)}")
                await asyncio.sleep(2)


@bot.command(name="joinservers")
async def joinservers(ctx):
    servers = open("servers.txt").readlines()
    for server in servers:
        if server != "":
            try:
                await bot.join_guild(server.strip())
                print(f"Joined {server.strip()}")
                await asyncio.sleep(2)
            except:
                print("Failed to join server. Invite invalid?")


bot.run(config['token'])