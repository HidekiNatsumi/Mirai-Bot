import random

import discord
from discord import member
from discord.ext import tasks
from discord.ext.commands import bot

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=discord.Intents.all())

intents = discord.Intents.all()

token = 'token'
my_server = 00000000000000000 #add your server id


@client.event
async def on_ready():
    for server in client.guilds:
        serverId = server.id
        if server.id != my_server:#makes this bot leave everyserver except (my_server) on_ready
            await client.get_guild(serverId).leave()
            print('we left ', server)

    await client.change_presence(activity=discord.Game(name="Visual Studio Code")) #sets activity on
    print(f'We have logged in as {client.user}')

    for member in client.get_all_members():
        # print(member)
        if member.activity is not None:
            for activity in member.activities:
                if activity.name == 'League of Legends':
                    print(member.name, 'is a no lifer since he is playing', activity.name)

                if activity.name == 'Spotify':
                    print(member.name, 'is playing', activity.title, 'by', activity.artist)
                    await client.get_channel(1007571199024431126).send(
                        f"{member.name} is playing {activity.title} by {activity.artist}")


@client.event
async def on_member_join(member, server):       #On member join it will display a member joined the server message and also a dm
    await client.get_channel(1007571199024431126).send(f"{member.name} has joined")
    await member.send(f'Welcome to the server')


@client.event
async def on_member_remove(member, server):         #on member leave it will display member has left the server
    await client.get_channel(1007571199024431126).send(f"{member.name} has left")


@client.event
async def on_server_join(server):
    serverId = server.id
   # print('left the server ', server)
    if server != my_server:
        await client.get_guild(serverId).leave()
        print('we left ', server)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!roll'):     #gets a random number used to roll a die
        await message.channel.send(random.randint(1, 6))

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
        
    if message.content.startswith('!spotify'):
        #checks if the member who sent the message is listening to a spotify song
        for member in client.get_all_members():
            # print(member)
            if member == message.author:
                if member.activity is not None:
                    for activity in member.activities:
                        if activity.name == 'Spotify':
                            channel = message.channel
                            await client.get_channel(channel.id).send(
                                f"{member.name} is playing {activity.title} by {activity.artist}")
    if message.author == client.user:
        return


@client.event
async def on_presence_update(member,activity):
    print(member.activity)


client.run(token)
