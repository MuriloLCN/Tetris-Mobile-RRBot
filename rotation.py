import gc

import discord

import classes
import datahandling
import texts


async def compareQueue(message: discord.Message, entering: bool, entryList: list, exitList: list, dataClass: classes.ServerData, data: dict):
    """
    Compares two queues to see if there are matching interests

    :param message: The message context
    :param entering: Whether the player is entering or leaving
    :param entryList: List of players that are waiting to enter
    :param exitList: List of players that are waiting to leave
    :param dataClass: Server data
    :param data: Data dict
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

    datahandling.writeserverdata(message.guild.id, dataClass, data)


async def enter(message: discord.Message, serverData: classes.ServerData, data: dict):
    """
    Joins the entry queue

    Discord command:
    $enter

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """
    name = message.author.id

    if str(name) in serverData.cached.entryqueue:
        serverData.cached.entryqueue.remove(str(name))
        datahandling.writeserverdata(message.guild.id, serverData, data)
        await message.add_reaction('\U00002B55')

    else:
        serverData.cached.entryqueue.append(str(name))
        datahandling.writeserverdata(message.guild.id, serverData, data)
        await message.add_reaction('\U0001F44D')

        await compareQueue(message, True, serverData.cached.entryqueue, serverData.cached.exitqueue, serverData, data)

    del name, serverData, data, message
    gc.collect()


async def leave(message: discord.Message, serverData: classes.ServerData, data: dict):
    """
    Joins the exit queue

    Discord command:
    $leave

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """
    name = message.author.id

    if str(name) in serverData.cached.exitqueue:
        serverData.cached.exitqueue.remove(str(name))
        datahandling.writeserverdata(message.guild.id, serverData, data)
        await message.add_reaction('\U00002B55')

    else:
        serverData.cached.exitqueue.append(str(name))
        datahandling.writeserverdata(message.guild.id, serverData, data)
        await message.add_reaction('\U0001F44D')
        await compareQueue(message, False, serverData.cached.entryqueue, serverData.cached.exitqueue, serverData, data)

    del name, serverData, data, message
    gc.collect()


async def freeSpot(message: discord.Message, data: dict):
    """
    Mentions the next person in the entry queue that there is a free spot

    Discord command:
    $freespot

    :param message: Message context
    :param data: Loaded data
    """
    serverData = datahandling.getserverdata(message.guild.id, data)

    if len(serverData.cached.entryqueue) > 0:
        name = str(serverData.cached.entryqueue[0])
        await message.channel.send("There's an open spot, <@" + name + ">, you can enter")
        serverData.cached.entryqueue.pop(0)
        datahandling.writeserverdata(message.guild.id, serverData, data)

    else:
        await message.channel.send("The entry queue is empty")


async def check(message, serverData, data):
    """
    Main check command

    Discord commands:
    $rotation
    $enter
    $leave
    $freespot

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """
    # Help command
    if message.content.startswith('$rotation'):
        await message.channel.send(texts.rotation)
        return

    if message.content.startswith('$enter'):
        await enter(message, serverData, data)

    if message.content.startswith('$leave'):
        await leave(message, serverData, data)

    if message.content.startswith('$freespot'):
        await freeSpot(message, data)
