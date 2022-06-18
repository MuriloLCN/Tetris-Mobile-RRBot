import gc

import discord

import classes
import datahandling
import texts


async def getVisualizerText(serverData: classes.ServerData, client: discord.Client):
    """
    Returns a string with the names of everyone waiting in the entry and exit queues.

    :param serverData: Server data
    :param client: Client context
    """
    enteringText = 'Waiting to enter:\n'
    exitText = '\nWaiting to exit:\n'
    for name in serverData.cached.entryqueue:
        user = await client.fetch_user(name)
        enteringText += str(user) + '\n'
    for name in serverData.cached.exitqueue:
        user = await client.fetch_user(name)
        exitText += str(user) + '\n'

    return "```" + enteringText + exitText + "```"


async def updateVisualizers(serverData: classes.ServerData, client: discord.Client, originalMessage: discord.Message):
    """
    Updates all visualizers. Deletes it from memory if unable to.

    :param serverData: Server data
    :param client: Client context
    :param originalMessage: Original message context (used to get serverID)
    """
    text = await getVisualizerText(serverData, client)

    for item in serverData.rotationvisualizerids.keys():
        try:
            channel = await client.fetch_channel(item)
            message = await channel.fetch_message(serverData.rotationvisualizerids[item])
        except (KeyError, discord.errors.NotFound, Exception):
            serverData.rotationvisualizerids.pop(item)
            datahandling.writeserverdata(originalMessage.guild.id, serverData)
            return

        try:
            await message.edit(content=text)
        except (KeyError, Exception):
            serverData.rotationvisualizerids.pop(item)
            datahandling.writeserverdata(originalMessage.guild.id, serverData)


async def compareQueue(message: discord.Message, entering: bool, entryList: list, exitList: list, dataClass: classes.ServerData):
    """
    Compares two queues to see if there are matching interests

    :param message: The message context
    :param entering: Whether the player is entering or leaving
    :param entryList: List of players that are waiting to enter
    :param exitList: List of players that are waiting to leave
    :param dataClass: Server data
    """
    user = str(message.author.id)

    if entering:
        comparative = exitList.copy()

    else:
        comparative = entryList.copy()

    if len(comparative) > 0:
        await message.channel.send(
            "It's a match! <@" + str(user) + "> and <@" + str(comparative[0]) + "> can switch!"
        )
        if entering:
            dataClass.cached.entryqueue.remove(user)
            dataClass.cached.exitqueue.pop(0)
        else:
            dataClass.cached.exitqueue.remove(user)
            dataClass.cached.entryqueue.pop(0)

    datahandling.writeserverdata(message.guild.id, dataClass)


async def addVisualizer(message: discord.Message, serverData: classes.ServerData, client: discord.Client):
    """
    Adds a visulizer to make the queues used for rotation visible so it's better for planning ahead.

    :param message: Message context
    :param serverData: Server data
    :param client: Client context
    """
    visualizertext = await getVisualizerText(serverData, client)

    newMessage = await message.channel.send(visualizertext)

    appendable = {newMessage.channel.id: newMessage.id}

    serverData.rotationvisualizerids.update(appendable)

    await updateVisualizers(serverData, client, message)

    datahandling.writeserverdata(message.guild.id, serverData)


async def enter(message: discord.Message, serverData: classes.ServerData, client: discord.Client):
    """
    Joins the entry queue

    Discord command:
    $enter

    :param message: Message context
    :param serverData: Server data
    :param client: Client context
    """
    name = message.author.id

    if str(name) in serverData.cached.entryqueue:
        serverData.cached.entryqueue.remove(str(name))
        datahandling.writeserverdata(message.guild.id, serverData)
        await message.add_reaction('\U00002B55')

    else:
        serverData.cached.entryqueue.append(str(name))
        datahandling.writeserverdata(message.guild.id, serverData)
        await message.add_reaction('\U0001F44D')

        await compareQueue(message, True, serverData.cached.entryqueue, serverData.cached.exitqueue, serverData)

    await updateVisualizers(serverData, client, message)
    del name, serverData, message
    gc.collect()


async def leave(message: discord.Message, serverData: classes.ServerData, client: discord.Client):
    """
    Joins the exit queue

    Discord command:
    $leave

    :param message: Message context
    :param serverData: Server data
    :param client: Client context
    """
    name = message.author.id

    if str(name) in serverData.cached.exitqueue:
        serverData.cached.exitqueue.remove(str(name))
        datahandling.writeserverdata(message.guild.id, serverData)
        await message.add_reaction('\U00002B55')

    else:
        serverData.cached.exitqueue.append(str(name))
        datahandling.writeserverdata(message.guild.id, serverData)
        await message.add_reaction('\U0001F44D')
        await compareQueue(message, False, serverData.cached.entryqueue, serverData.cached.exitqueue, serverData)

    await updateVisualizers(serverData, client, message)
    del name, serverData, message
    gc.collect()


async def freeSpot(message: discord.Message, client: discord.Client):
    """
    Mentions the next person in the entry queue that there is a free spot

    Discord command:
    $freespot

    :param message: Message context
    :param client: Client context
    """
    serverData = datahandling.loadData(str(message.guild.id))

    if len(serverData.cached.entryqueue) > 0:
        name = str(serverData.cached.entryqueue[0])
        await message.channel.send("There's an open spot, <@" + name + ">, you can enter")
        serverData.cached.entryqueue.pop(0)
        await updateVisualizers(serverData, client, message)
        datahandling.writeserverdata(message.guild.id, serverData)

    else:
        await message.channel.send("The entry queue is empty")


async def check(message, serverData, client):
    """
    Main check command

    Discord commands:
    $rotation
    $enter
    $leave
    $freespot

    :param message: Message context
    :param serverData: Server data
    :param client: Client context
    """
    # Help command
    if message.content.startswith('$rotation'):
        await message.channel.send(texts.rotation)
        return

    if message.content.startswith('$enter'):
        await enter(message, serverData, client)

    if message.content.startswith('$leave'):
        await leave(message, serverData, client)

    if message.content.startswith('$freespot'):
        await freeSpot(message, client)

    if message.content.startswith('$addvisualizer'):
        await addVisualizer(message, serverData, client)
