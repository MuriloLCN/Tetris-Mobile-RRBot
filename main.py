import aiohttp.client_exceptions
import discord
import asyncio

import calculators
import dailyreminder
import dataupdate
import infocmds
import rotation
import savingtetris
import bonuspinging
import rolegiving

import privatedata
import datahandling
import timer
import rolechanger

intent = discord.Intents().all()

fullAccessServers = privatedata.fullAccessServers
whitelist = privatedata.whitelist
myid = privatedata.myid
alarmbotid = privatedata.alarmbotid

data = datahandling.loadDict()


async def waitforme(timeSpan, message, serverData):
    await message.channel.send("Timer created to " + str(timeSpan) + " minutes from now")
    await asyncio.sleep(timeSpan * 60)
    await message.channel.send(serverData.currentRole + " Connect now")


client = discord.Client(intents=intent)




@client.event
async def on_ready():
    print('Bot conectado como {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="$? for help"))


@client.event
async def on_message(message):
    global data

    if str(message.channel.type) == 'private' and message.author != client.user and message.content.startswith('$'):
        # Commands need server data to be loaded, so cannot be used in DMs
        return

    if str(message.channel.type) == 'private' and message.author != client.user:
        # This serves as a placeholder for a future support system.
        usuario = await client.fetch_user(myid)
        dm = await usuario.create_dm()
        await dm.send(str(message.author) + ': ' + str(message.content))

    # Only loads data if the message is a command

    if not message.content.startswith('$'):
        if not message.author.id == alarmbotid:
            return

    # Loads data
    try:
        curId = message.guild.id
        serverData = datahandling.getserverdata(curId, data)
    except Exception as err:
        usuario = await client.fetch_user(myid)
        dm = await usuario.create_dm()
        await dm.send('Error: ' + str(err))
        return

    # Gets the AlarmBot message and updates pending alarm ID
    # JUST A PLACEHOLDER! NOT FINAL!!
    # This is not perfect because it depends on humans to create the alarms, and if they don't do them in order,
    # they'll get jumbled (this is because Alarmbot cannot read other bots' messages)
    if message.author.id == alarmbotid:
        if message.embeds:
            try:
                stringy = str(message.embeds[0].to_dict()['fields'][0]['name'])
                gotId = stringy.split(' ')[3]
                try:
                    ind = serverData.alarms.index('temp')
                    serverData.alarms[ind] = gotId
                    data = datahandling.writeserverdata(message.guild.id, serverData, data)
                except (IndexError, ValueError):
                    return
            except (IndexError, ValueError):
                return

    if message.author == client.user:
        return
        # Just want to keep this here in case I need to do something using it's own messages in the future

    # Common commands
    await timer.check(message, serverData)

    await infocmds.check(client, message)

    await dataupdate.check(message, serverData, data)

    await calculators.check(message, serverData)

    # Trusted server features
    if message.guild.id in fullAccessServers:

        await rotation.check(message, serverData, data)

        await savingtetris.check(message, serverData, data)

        await bonuspinging.check(message, serverData, data)

        await dailyreminder.check(client, message, serverData, data)

        await rolegiving.check(client, message, serverData, data)



@client.event
async def on_raw_reaction_add(payload):

    await rolechanger.check(client, payload, data)


try:
    client.run(MY_TOKEN)
except (aiohttp.client_exceptions.ClientConnectorError, Exception):
    print('Could not connect to Discord API')
    # Had to put this here because every time there was a connection error my token
    # was briefly visible on the hosting platform's log command, so this no longer happens

