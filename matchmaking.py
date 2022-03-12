import discord.errors
from copy import deepcopy

import asyncio
import gc

import classes

# TODO List
'''
Add custom timer
Add custom player limit
Add premature start
Add more control over matchmaking
Etc
'''


async def updateMessage(message: discord.Message, matches: classes.Match, client: discord.Client):
    """
    Updates all messages for players that are awaiting in the matchmaking lobby when things change (player joined, left,
    etc)
    :param message: Message context
    :param matches: Match object
    :param client: Client context
    """
    for i in matches.players.keys():
        try:
            channel = await client.fetch_channel(matches.players[i][0])
            msg = await channel.fetch_message(matches.messageids[matches.players[i][0]])
            text = str(matches.getMessageContent())
            await msg.edit(content=text)
        except (discord.errors.NotFound, KeyError):
            newMsg = await message.channel.send(matches.getMessageContent())
            newdict = {message.channel.id: newMsg.id}
            matches.messageids.update(newdict)

    if len(matches.players.keys()) == 0:
        for i in matches.messageids.keys():
            try:
                channel = await client.fetch_channel(i)
                msg = await channel.fetch_message(matches.messageids[i])
                text = str(matches.getMessageContent())
                await msg.edit(content=text)
            except (discord.errors.NotFound, Exception):
                pass


async def startMatch(matches: classes.Match, client: discord.Client):
    """
    Starts the match countdown and pinging

    :param matches: Match object
    :param client: Client context
    """
    for key in matches.players.keys():
        try:
            channel = await client.fetch_channel(matches.players[key][0])
            await channel.send("Match is starting in 30s, be ready to join royale!")
        except (discord.errors.NotFound, KeyError, IndexError):
            pass

    tempMatches = deepcopy(matches)
    matches.reset()
    await asyncio.sleep(30)

    for key in tempMatches.players.keys():
        try:
            channel = await client.fetch_channel(tempMatches.players[key][0])

            tex = ''
            for userid in tempMatches.players.keys():
                tex = tex + ' <@' + str(userid) + '>'

            await channel.send("Join now!" + tex)
        except (discord.errors.NotFound, KeyError, IndexError):
            pass

    del tempMatches
    gc.collect()


async def check(message, matches, client):
    """
    Main check function

    :param message: Message context
    :param matches: Match object
    :param client: Client context
    """
    userdata = {message.author.id: [message.channel.id, str(message.author.name)]}

    if message.content.startswith('$matchmaking'):

        if message.author.id in matches.players.keys():
            matches.players.pop(message.author.id)
            await message.add_reaction('\U00002B55')
            await updateMessage(message, matches, client)

        else:
            matches.players.update(userdata)
            await message.add_reaction('\U0001F44D')
            await updateMessage(message, matches, client)

        if len(matches.players.keys()) >= matches.playerlimit:
            await startMatch(matches, client)
