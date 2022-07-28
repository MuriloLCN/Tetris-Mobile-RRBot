import gc

import aiohttp.client_exceptions
import discord
import asyncio

import bonuspinging
import calculators
import classes
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

    if str(message.channel.type) == 'private':
        # Commands need server data to be loaded, so cannot be used in DMs
        return

    # Only moves forward if the message is relevant to the bot
    if not message.content.startswith('$'):
        return

    # Loads data
    try:
        curId = message.guild.id
        serverData = datahandling.loadData(str(curId))
    except Exception as err:
        usuario = await client.fetch_user(myid)
        dm = await usuario.create_dm()
        await dm.send('Error: ' + str(err))
        return

    if message.author == client.user:
        return
        # Just want to keep this here in case I need to do something using it's own messages in the future

    # Common commands
    await helpcommand.check(message, serverData)

    await timer.check(message, serverData)

    await infocmds.check(client, message)

    await dataupdate.check(message, serverData)

    await calculators.check(message, serverData)

    await rolegiving.check(client, message, serverData)

    if curId in blacklist:
        return

    await rotation.check(message, serverData, client)

    await savingtetris.check(message, serverData)

    await bonuspinging.check(message, serverData)

    # await graphs.check(message, serverData, data)
    # Keeping this here until I fix completely the memory leak from the radar chart
    asyncio.get_event_loop().create_task(graphs.check(message, serverData))

    await clock.check(message)

    if message.guild.id in privatedata.fullAccessServers:

        await performancetests.check(message, serverData, client, matches)

    del curId, message, serverData
    gc.collect()


@client.event
async def on_raw_reaction_add(payload):
    """
    Event handler for reaction addition on Discord messages
    :param payload: Payload context
    """

    await rolechanger.check(client, payload)

    await helpcommand.reaction_check(client, payload)

    del payload
    gc.collect()

try:
    client.run(token)
except (aiohttp.client_exceptions.ClientConnectorError, Exception):
    print('Could not connect to Discord API')
    # Had to put this here because every time there was a connection error my token
    # was briefly visible on the hosting platform's log command, so this no longer happens
