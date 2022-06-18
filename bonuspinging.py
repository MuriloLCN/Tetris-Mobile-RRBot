import gc

import discord

import classes
import datahandling
import texts

import clock


async def fullBonusPingCMD(message: discord.Message):
    """
    Sends the help text for the bonus pinging mechanic

    Discord command:
    $fullbonusping

    :param message: Message context
    """
    await message.channel.send(texts.fullbonusping)


async def dailiesDoneCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Does the necessary checks when a player has done their daily tasks
    Adds/Removes them from serverData.cached.donedailies
    Silences/Desilences their daily alarm, if they have one

    Discord command:
    $dailiesdone

    :param message: Message context
    :param serverData: Server data
    """
    name = str(message.author.id)

    if name in serverData.cached.donedailies:
        serverData.cached.donedailies.remove(name)
        await message.add_reaction('\U00002B55')

        # Reactivate the alarm (old)
        if str(name) in serverData.alarms.keys():
            if serverData.alarms[str(name)][1]:
                serverData.alarms[str(name)][1] = False

        # Reactivate the alarm (new)
        alarms = clock.loadAlarms()
        if int(message.author.id) in alarms.keys():
            try:
                alarms[int(message.author.id)][4] = False
                clock.writeUpdatedAlarms(alarms)
            except IndexError:
                pass

    else:
        serverData.cached.donedailies.append(name)

        await message.add_reaction('\U0001F44D')

        # Deactivate the alarm (old)
        if str(name) in serverData.alarms.keys():
            if not serverData.alarms[str(name)][1]:
                serverData.alarms[str(name)][1] = True

        # Deactivate the alarm (new)
        alarms = clock.loadAlarms()
        if int(message.author.id) in alarms.keys():
            try:
                alarms[int(message.author.id)][4] = True
                clock.writeUpdatedAlarms(alarms)
            except IndexError:
                pass

    datahandling.writeserverdata(message.guild.id, serverData)

    del name, serverData, message
    gc.collect()


async def gotFullBonusCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Signals every player that has done their daily tasks that the team has achieved full bonus

    :param message: Message context
    :param serverData: Server data
    """
    myString = ''

    for name in serverData.cached.donedailies:
        myString += "<@" + str(name) + ">, "

    await message.channel.send("Team now has full bonus, let's get that bread! " + myString)
    serverData.cached.donedailies.clear()

    datahandling.writeserverdata(message.guild.id, serverData)
    del myString, serverData, message
    gc.collect()
    return


async def check(message: discord.Message, serverData: classes.ServerData):
    """
    Main check function

    Discord commands:
    $fullbonusping
    $dailiesdone
    $gotfullbonus

    :param message: Message context
    :param serverData: Server data
    """
    # Help command
    if message.content.startswith('$fullbonusping'):
        await fullBonusPingCMD(message)

    # Add/Remove name from list
    if message.content.startswith('$dailiesdone'):
        await dailiesDoneCMD(message, serverData)

    # Pinging command
    if message.content.startswith('$gotfullbonus'):
        await gotFullBonusCMD(message, serverData)
