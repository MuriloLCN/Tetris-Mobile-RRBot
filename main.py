import gc

import aiohttp.client_exceptions
import discord
import asyncio

import bonuspinging
import calculators
import classes
import dailyreminder
import datahandling
import dataupdate
import graphs
import helpcommand
import infocmds
import privatedata
import rolechanger
import rolegiving
import rotation
import savingtetris
import timer
import matchmaking
import performancetests
import clock

intent = discord.Intents().all()

blacklist = privatedata.blacklist
myid = privatedata.myid
alarmbotid = privatedata.alarmbotid
token = privatedata.token
devtoken = privatedata.devtoken  # Token used for extensive testing

matches = classes.Match()

client = discord.Client(intents=intent)


@client.event
async def on_ready():
    """
    Event handler for initialization of the bot
    """
    print('Bot connected as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="$? for help"))
    await clock.clockLoop(client)


@client.event
async def on_message(message):
    """
    Event handler for Discord messages

    :param message: Message context
    """
    global matches

    if str(message.channel.type) == 'private' and message.author != client.user and message.content.startswith('$'):
        # Commands need server data to be loaded, so cannot be used in DMs
        return

    if str(message.channel.type) == 'private' and message.author != client.user:
        # This serves as a placeholder for a future support system.
        usuario = await client.fetch_user(myid)
        dm = await usuario.create_dm()
        await dm.send(str(message.author) + ': ' + str(message.content))
        del usuario, dm
        return

    # Only moves forward if the message is relevant to the bot
    if not message.content.startswith('$'):
        if not message.author.id == alarmbotid:
            return

    # Loads data
    data = datahandling.loadDict()

    for key in data.keys():
        data[key] = classes.updateObject(data[key])

    try:
        curId = message.guild.id
        serverData = datahandling.getserverdata(curId, data)
    except Exception as err:
        usuario = await client.fetch_user(myid)
        dm = await usuario.create_dm()
        await dm.send('Error: ' + str(err))
        return

    # Gets the AlarmBot message and updates pending alarm ID
    if message.author.id == alarmbotid:
        if message.embeds:
            try:
                stringy = str(message.embeds[0].to_dict()['fields'][0]['name'])
                gotId = stringy.split(' ')[3]
                for entry in serverData.alarms.keys():
                    if serverData.alarms[entry][0] == 'temp':
                        serverData.alarms[entry][0] = gotId
                        break
                datahandling.writeserverdata(message.guild.id, serverData, data)
                del stringy, gotId
                return
            except (IndexError, ValueError):
                return

    if message.author == client.user:
        return
        # Just want to keep this here in case I need to do something using it's own messages in the future

    # Common commands
    await helpcommand.check(message, serverData, data)

    await timer.check(message, serverData)

    await infocmds.check(client, message)

    await dataupdate.check(message, serverData, data)

    await calculators.check(message, serverData)

    await matchmaking.check(message, matches, client)

    await rolegiving.check(client, message, serverData, data)

    # Usually it's better to turn this into a guard clause but keeping it indented helps to see which one's which
    if message.guild.id in privatedata.fullAccessServers:

        await rotation.check(message, serverData, data, client)

        await savingtetris.check(message, serverData, data)

        await bonuspinging.check(message, serverData, data)

        await dailyreminder.check(client, message, serverData, data)

        #await graphs.check(message, serverData, data)
        # Keeping this here until memory leak gets better
        asyncio.get_event_loop().create_task(graphs.check(message, serverData, data))

        await performancetests.check(message, serverData, data, client, matches)

        await clock.check(message)

    del curId, data, key, message, serverData
    gc.collect()


@client.event
async def on_raw_reaction_add(payload):
    """
    Event handler for reaction addition on Discord messages
    :param payload: Payload context
    """
    data = datahandling.loadDict()

    for key in data.keys():
        data[key] = classes.updateObject(data[key])

    await rolechanger.check(client, payload, data)

    await helpcommand.reaction_check(client, payload, data)

    del data, key, payload
    gc.collect()

try:
    client.run(token)
except (aiohttp.client_exceptions.ClientConnectorError, Exception):
    print('Could not connect to Discord API')
    # Had to put this here because every time there was a connection error my token
    # was briefly visible on the hosting platform's log command, so this no longer happens
