import aiohttp.client_exceptions
import discord

import bonuspinging
import calculators
import classes
import dailyreminder
import datahandling
import dataupdate
import graphs
import infocmds
import privatedata
import rolechanger
import rolegiving
import rotation
import savingtetris
import timer
import matchmaking

intent = discord.Intents().all()

blacklist = privatedata.blacklist
myid = privatedata.myid
alarmbotid = privatedata.alarmbotid
token = privatedata.token
devtoken = privatedata.devtoken  # Token used for extensive testing

data = datahandling.loadDict()

matches = classes.Match()

client = discord.Client(intents=intent)

for key in data.keys():
    data[key] = classes.updateObject(data[key])


@client.event
async def on_ready():
    print('Bot connected as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="$? for help"))


@client.event
async def on_message(message):
    global data
    global matches

    if str(message.channel.type) == 'private' and message.author != client.user and message.content.startswith('$'):
        # Commands need server data to be loaded, so cannot be used in DMs
        return

    if str(message.channel.type) == 'private' and message.author != client.user:
        # This serves as a placeholder for a future support system.
        usuario = await client.fetch_user(myid)
        dm = await usuario.create_dm()
        await dm.send(str(message.author) + ': ' + str(message.content))

    # Only moves forward if the message is relevant to the bot
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
                for entry in serverData.alarms.keys():
                    if serverData.alarms[entry][0] == 'temp':
                        serverData.alarms[entry][0] = gotId
                        break
                datahandling.writeserverdata(message.guild.id, serverData, data)
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

    await matchmaking.check(message, matches, client)

    # Usually it's better to turn this into a guard clause but keeping it indented helps me to see which one's which
    if message.guild.id in privatedata.fullAccessServers:

        await rotation.check(message, serverData, data)

        await savingtetris.check(message, serverData, data)

        await bonuspinging.check(message, serverData, data)

        await dailyreminder.check(client, message, serverData, data)

        await rolegiving.check(client, message, serverData, data)

        await graphs.check(message, serverData, data)


@client.event
async def on_raw_reaction_add(payload):

    await rolechanger.check(client, payload, data)


try:
    client.run(token)
except (aiohttp.client_exceptions.ClientConnectorError, Exception):
    print('Could not connect to Discord API')
    # Had to put this here because every time there was a connection error my token
    # was briefly visible on the hosting platform's log command, so this no longer happens
