import gc

import discord

import classes
import datahandling
import texts


async def savedTetris(message: discord.Message, serverData: classes.ServerData, data: dict):
    """
    Marks that user as having Tetris line clears stored in a marathon game

    Discord command:
    $savedtetris

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """
    name = str(message.author.id)

    if name in serverData.cached.savedtetrises:
        serverData.cached.savedtetrises.remove(name)
        datahandling.writeserverdata(message.guild.id, serverData, data)
        await message.add_reaction('\U00002B55')

    else:
        serverData.cached.savedtetrises.append(name)
        datahandling.writeserverdata(message.guild.id, serverData, data)
        await message.add_reaction('\U0001F44D')

    del name, serverData, data, message
    gc.collect()
    return


async def tetrisTask(message: discord.Message, serverData: classes.ServerData, data: dict):
    """
    Pings all users that have stored Tetris line clears so that they can block out and add their points to the task

    Discord command:
    $tetristask

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """
    myString = ''

    while len(serverData.cached.savedtetrises) != 0:
        for name in serverData.cached.savedtetrises:
            myString += "<@" + str(name) + ">, "
            serverData.cached.savedtetrises.remove(name)

    datahandling.writeserverdata(message.guild.id, serverData, data)

    await message.channel.send("Tetris task is live! " + myString)
    del myString, serverData, data, message
    gc.collect()
    return


async def check(message: discord.Message, serverData: classes.ServerData, data: dict):
    """
    Main check function

    Discord commands:
    $savedtetris
    $tetristask
    $infotetris

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """
    if message.content.startswith('$savedtetris'):
        await savedTetris(message, serverData, data)

    if message.content.startswith('$tetristask'):
        await tetrisTask(message, serverData, data)

    # Help command
    if message.content.startswith('$infotetris'):
        await message.channel.send(texts.infotetris)
        return
