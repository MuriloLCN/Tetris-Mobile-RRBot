import discord.errors

import classes
import datahandling
import privatedata
import gc


async def setRoleCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Changes the role that's mentioned when a timer runs out

    Discord command:
    $setrole (@newrole)

    :param message: Message context
    :param serverData: Server data
    """

    if not message.author.guild_permissions.administrator and message.author.id not in privatedata.whitelist:
        await message.channel.send("You do not have permission to use this command")
        return

    try:
        temp_role = message.content.split('@')[1]

    except IndexError:
        await message.channel.send("Oops, incorrect syntax. Correct usage: \"$setrole @role\"")
        return

    # Fun fact, when mentioning users and custom roles you need to say '<@their_id>' but when you are mentioning
    # everyone/here you just say '@everyone'/'@here'.

    if temp_role != 'everyone' and temp_role != 'here':
        temp_role = '<@' + temp_role

    # There's no need to check if they have permission to tag everyone/here because
    # if they don't, they won't even be able to send the command in chat anyway
    else:
        temp_role = '@' + temp_role

    await message.channel.send("Switched role to: " + temp_role)
    serverData.proprieties.currentrole = temp_role
    datahandling.writeserverdata(message.guild.id, serverData)

    del temp_role, serverData, message
    gc.collect()


async def setNewLimitCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Changes the time limit of how long a timer can be

    Discord command:
    $setnewlimit (new limit in minutes)

    :param message: Message context
    :param serverData: Server data
    """
    if not message.author.guild_permissions.administrator or message.author.id not in privatedata.whitelist:
        await message.channel.send("You do not have permission to use this command")
        return

    novoLimite = str(message.content).split(' ')[1]

    try:
        novoLimite = float(novoLimite)

    except ValueError:
        await message.channel.send('Invalid time limit, use "$?" for help')
        return

    if float(novoLimite) < 0:
        await message.channel.send('Time limit cannot be negative')
        return

    if float(novoLimite) == 0:
        await message.channel.send('Time limit cannot be zero')
        return

    serverData.proprieties.currentlimit = float(novoLimite)
    datahandling.writeserverdata(message.guild.id, serverData)
    await message.channel.send('Time limit changed to ' + str(novoLimite) + ' minutes maximum')

    del novoLimite, serverData, message
    gc.collect()


async def setReferencePPSCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Changes the reference PPS values to be used in calculations for the server

    Discord command:
    $setreferencepps (new reference PPS values)

    :param message: Message context
    :param serverData: Server data
    """
    try:
        value = str(message.content).split(' ')[1]
    except IndexError:
        await message.channel.send("Invalid syntax, use '$setreferencepps <PPS>' where <PPS> is an integer")
        return
    try:
        value = float(value)
    except ValueError:
        await message.channel.send("Invalid PPS value")
        return
    serverData.proprieties.referencepps = value
    datahandling.writeserverdata(message.guild.id, serverData)
    await message.add_reaction('\U0001F44D')

    del value, serverData, message
    gc.collect()


async def printServerDataCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Prints all data stored for the server

    Discord command:
    $printserverdata

    :param message: Message context
    :param serverData: Server data
    """
    if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
        await message.channel.send("You don't have permission to use this command")
        return

    try:
        await message.channel.send('Server data: ' + str(vars(serverData)))
        await message.channel.send('Cached: ' + str(vars(serverData.cached)))
        await message.channel.send('Proprieties: ' + str(vars(serverData.proprieties)))
        await message.channel.send('Ref. Param.: ' + str(vars(serverData.proprieties.referenceparameters)))
    except discord.errors.HTTPException:
        await message.channel.send('Stored data too large to be sent in one message')
    return


async def resetServerDataCMD(message: discord.Message):
    """
    Resets current server's data to a virgin state

    Discord command:
    $resetserverdata

    :param message: Message context
    """
    if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
        await message.channel.send("You don't have permission to use this command")
        return

    serverData = classes.ServerData()
    datahandling.writeserverdata(message.guild.id, serverData)
    await message.add_reaction('\U0001F44D')


async def clearCacheCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Clears the .cached attr of the ServerData

    Discord command:
    $clearcache

    :param message: Message context
    :param serverData: Server data
    """
    if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
        await message.channel.send("You don't have permission to use this command")
        return

    serverData.cached = classes.Cache()

    datahandling.writeserverdata(message.guild.id, serverData)
    await message.add_reaction('\U0001F44D')
    await message.channel.send("Cleared cache for rotation, dailies, tetrises, etc")

    return


async def updateReferenceValuesCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Updates the reference player values to be used in calculations for the server

    Discord command:
    $updatereferencevalues (day)/(month)/(year) (quick play highscore) (marathon highscore) (lines cleared) (tetrises)
    (all clears) (t-spins) (challenges) (login streak) (back-to-backs)

    :param message: Message context
    :param serverData: Server data
    """
    if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
        await message.channel.send("You don't have permission to use this command")
        return

    try:
        stringy = str(message.content).split(' ', 1)
        referenceString = stringy[1]
        # So many parameters...
        splitty = referenceString.split(' ')
        year = int(splitty[0].split('/')[2])
        month = int(splitty[0].split('/')[1])
        day = int(splitty[0].split('/')[0])
        qphs = int(splitty[1])
        mths = int(splitty[2])
        lines = int(splitty[3])
        tet = int(splitty[4])
        allc = int(splitty[5])
        tsd = int(splitty[6])
        chl = int(splitty[7])
        strk = int(splitty[8])
        btb = int(splitty[9])

        serverData.proprieties.referenceparameters = classes.Parameters(
            year, month, day, qphs, mths, lines, tet, allc, tsd, chl, strk, btb
        )

        datahandling.writeserverdata(message.guild.id, serverData)
        await message.add_reaction('\U0001F44D')
    except (IndexError, Exception):
        await message.channel.send("Incorrect syntax, correct usage: \n"
                                   "$updatereferencevalues <day>/<month>/<year> <quickplay hscore>"
                                   " <marathon hscore>"
                                   " <lines> <tetrises> <allclears> <tspins> <challenges> <streak> <b2bs>")
        return

    del stringy, referenceString, splitty, year, month, day, qphs, mths, lines, tet, allc, tsd, chl, strk, btb
    del serverData, message
    gc.collect()


async def forgetChangerMessagesCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Forgets all changer messages, so they'll no longer work

    Discord command:
    $forgetchangermessages

    :param message: Message context
    :param serverData: Server data
    """
    if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
        await message.channel.send("You don't have permission to use this command")
        return

    serverData.rolechangerids = []
    await message.add_reaction('\U0001F44D')
    datahandling.writeserverdata(message.guild.id, serverData)


async def appendChangerIDCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Adds a message ID to the 'changer messages' stored ids, so any user message can be used to switch roles, as long
    as it's formatted in the same way. This way those messages can be dynamically edited on-the-go

    Discord command:
    $appendchangerid (message id)

    :param message: Message context
    :param serverData: Server data
    """
    if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
        await message.channel.send("You don't have permission to use this command")
        return

    try:
        value = str(message.content).split(' ')[1]  # Yes, they are stored as str and not string for reasons
        # past me should know...
    except (IndexError, ValueError):
        await message.channel.send("Invalid command, correct usage:\n$addchangerid <messageID>")
        return

    serverData.rolechangerids.append(value)
    await message.add_reaction('\U0001F44D')
    datahandling.writeserverdata(message.guild.id, serverData)
    del value, serverData, message
    gc.collect()


async def storePointCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Stores a data point

    Discord command:
    $storepoint (point name) (day)/(month)/(year) (quick play highscore) (marathon highscore) (lines cleared) (tetrises)
    (all clears) (t-spins) (challenges) (login streak) (back-to-backs)

    :param message: Message context
    :param serverData: Server data
    """
    # Reused code from $addpoint in graphs.py
    try:
        texts = str(message.content).split(' ')
        username = texts[1].lower()
        date = texts[2]
        quickplayhs = int(texts[3])
        marathonhs = int(texts[4])
        linec = int(texts[5])
        tetrises = int(texts[6])
        allclears = int(texts[7])
        tspins = int(texts[8])
        challenges = int(texts[9])
        streak = int(texts[10])
        btbs = int(texts[11])
        try:
            day = int(date.split('/')[0])
            month = int(date.split('/')[1])
            year = int(date.split('/')[2])
        except IndexError:
            await message.channel.send("One or more of your date parameters were missing")
            return
        except ValueError:
            await message.channel.send("One or more of your date values were invalid")
            return
        except Exception as e:
            print("Error: {}".format(str(e)))
            return
    except IndexError:
        await message.channel.send("One or more of your parameters were missing\n"
                                   "Correct usage: "
                                   "$storepoint username d/m/y qphs mths lines tetris allc tspins "
                                   "chall strk b2b")
        return
    except ValueError:
        await message.channel.send("One or more of your values were invalid")
        return
    except Exception as e:
        print("Error: {}".format(str(e)))
        return

    try:
        param = classes.Parameters(year, month, day, quickplayhs, marathonhs, linec, tetrises, allclears, tspins,
                                   challenges, streak, btbs)
    except ValueError:
        await message.channel.send("Invalid date format")
        return

    serverData.storedpoints.update({username: param})
    await message.add_reaction('\U0001F44D')
    datahandling.writeserverdata(message.guild.id, serverData)
    del texts, username, date, quickplayhs, marathonhs, linec, tetrises, allclears, tspins, challenges, streak, btbs
    del serverData, message
    gc.collect()


async def deletePointCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Deletes a specific point

    Discord command:
    $deletepoint (point name)

    :param message: Message context
    :param serverData: Server data
    """
    try:
        name = str(message.content).split(' ')[1]
        name = name.lower()
    except (IndexError, Exception):
        await message.channel.send("Invalid command, correct usage:\n$deletepoint <pointname>")
        return

    try:
        serverData.storedpoints.pop(name)
    except (AttributeError, Exception):
        await message.channel.send("Point with name {} not found, to see list of stored points use "
                                   "$listpoints".format(name))
        return

    await message.add_reaction('\U0001F44D')
    datahandling.writeserverdata(message.guild.id, serverData)
    del name, serverData, message
    gc.collect()


async def clearPointsCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Clears all stored points

    Discord command:
    $clearpoints

    :param message: Message context
    :param serverData: Server data
    """
    serverData.storedpoints = dict()
    await message.add_reaction('\U0001F44D')
    datahandling.writeserverdata(message.guild.id, serverData)


async def listPointsCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Lists all stored points

    Discord command:
    $listpoints

    :param message: Message context
    :param serverData: Server data
    """
    text = "List of stored points:\n"
    appendabletext = ''

    for key in serverData.storedpoints.keys():
        appendabletext = appendabletext + str(key) + '\n'

    await message.channel.send(text + appendabletext)
    del text, appendabletext, serverData, message
    gc.collect()


async def printPointCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Prints the data for a given point

    Discord command:
    $printpoint (point name)

    :param message: Message context
    :param serverData: Server data
    """
    try:
        name = str(message.content).split(' ')[1]
        name = name.lower()
    except (IndexError, Exception):
        await message.channel.send("Invalid command, correct usage:\n$printpoint <pointname>")
        return

    try:
        point = serverData.storedpoints[name]
    except (AttributeError, Exception):
        await message.channel.send("Point with named {} not found, to see list of stored points use "
                                   "$listpoints".format(name))
        return

    await message.channel.send(str(vars(point)))
    del name, point, serverData, message
    gc.collect()


async def check(message, serverData):
    """
    Main check function

    Discord commands:
    $setrole
    $setnewlimit
    $setreferencepps
    $printserverdata
    $resetserverdata
    $clearcache
    $updatereferencevalues
    $forgetchangermessages
    $appendchangerid
    $storepoint
    $deletepoint
    $clearpoints
    $listpoints
    $printpoint

    :param message: Message context
    :param serverData: Server data
    """

    if message.content.startswith('$setrole'):
        await setRoleCMD(message, serverData)

    if message.content.startswith('$setnewlimit'):
        await setNewLimitCMD(message, serverData)

    if message.guild.id in privatedata.fullAccessServers:

        if message.content.startswith('$setreferencepps'):
            await setReferencePPSCMD(message, serverData)

        if message.content.startswith('$printserverdata'):
            await printServerDataCMD(message, serverData)

        if message.content.startswith('$resetserverdata'):
            await resetServerDataCMD(message)

        if message.content.startswith('$clearcache'):
            await clearCacheCMD(message, serverData)

        if message.content.startswith('$updatereferencevalues'):
            await updateReferenceValuesCMD(message, serverData)

        if message.content.startswith('$forgetchangermessages'):
            await forgetChangerMessagesCMD(message, serverData)

        if message.content.startswith('$appendchangerid'):
            await appendChangerIDCMD(message, serverData)

        if message.content.startswith('$storepoint'):
            await storePointCMD(message, serverData)

        if message.content.startswith('$deletepoint'):
            await deletePointCMD(message, serverData)

        if message.content.startswith('$clearpoints'):
            await clearPointsCMD(message, serverData)

        if message.content.startswith('$listpoints'):
            await listPointsCMD(message, serverData)

        if message.content.startswith('$printpoint'):
            await printPointCMD(message, serverData)
