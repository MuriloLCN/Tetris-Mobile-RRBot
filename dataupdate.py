import re

import classes
import datahandling
import privatedata


# It used to help keeping them in separate functions in the older versions of the code when everything was messy, I'm
# keeping them like this to serve as a personal reminder to not make things messy again.
def switch_role(new_role, serverID, dataClass, data):
    dataClass.currentRole = new_role
    datahandling.writeserverdata(serverID, dataClass, data)


def switch_limit(new_time, serverID, dataClass, data):
    dataClass.currentLimit = new_time
    datahandling.writeserverdata(serverID, dataClass, data)


async def check(message, serverData, data):

    # Changes 'currentrole', which is what is mentioned when the timer runs out
    if message.content.startswith('$setrole'):
        if message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist:
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
            switch_role(temp_role, message.guild.id, serverData, data)
        else:
            await message.channel.send("You do not have permission to use this command")
        return

    # Changes 'currentlimit', which is how long one can make a timer
    # TODO: Change all regex parsings to a normal parse like the other commands. This command is old.
    if message.content.startswith('$setnewlimit'):
        if message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist:

            novoLimite = re.sub('[^\d\.]', '', message.content)

            validTime = True

            try:
                novoLimite = float(novoLimite)

            except ValueError:
                await message.channel.send('Invalid time limit, use "$?" for help')
                validTime = False
                novoLimite = 15

            if float(novoLimite) < 0:
                await message.channel.send('Time limit cannot be negative')
                validTime = False

            if float(novoLimite) == 0:
                await message.channel.send('Time limit cannot be zero')
                validTime = False

            if validTime:
                switch_limit(float(novoLimite), message.guild.id, serverData, data)
                await message.channel.send('Time limit changed to ' + str(novoLimite) + ' minutes maximum')

        else:
            await message.channel.send("You do not have permission to use this command")
        return

    if message.guild.id in privatedata.fullAccessServers:
        # Changes 'referencepps', used in calculations
        if message.content.startswith('$setreferencepps'):
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
            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U0001F44D')
            return

        # Changes 'botchannel', which is the channel used for Alarbot as well in order to avoid spam
        if message.content.startswith('$setbotchannel'):

            if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
                await message.channel.send("You don't have permission to use this command")
                return

            try:
                channel = str(message.content).split('#')[1]
                channel = channel[:-1]
                serverData.proprieties.botchannel = channel
                await message.add_reaction('\U0001F44D')
                datahandling.writeserverdata(message.guild.id, serverData, data)
                return
            except (IndexError, ValueError):
                await message.channel.send("Invalid syntax, use '$setbotchannel #channel' as in '$setbotchannel #general'")
                return

        # Changes 'reminderchannel', which is where the bot will send the daily tasks reminders
        if message.content.startswith('$setreminderchannel'):

            if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
                await message.channel.send("You don't have permission to use this command")
                return

            try:
                channel = str(message.content).split('#')[1]
                channel = channel[:-1]
                serverData.proprieties.reminderchannel = channel
                await message.add_reaction('\U0001F44D')
                datahandling.writeserverdata(message.guild.id, serverData, data)
                return
            except (IndexError, ValueError):
                await message.channel.send(
                    "Invalid syntax, use '$setreminderchannel #channel' as in '$setreminderchannel #general'")
                return

        # Prints stored data for that server
        if message.content.startswith('$printserverdata'):
            if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
                await message.channel.send("You don't have permission to use this command")
                return

            await message.channel.send('Server data: ' + str(vars(serverData)))
            await message.channel.send('Cached: ' + str(vars(serverData.cached)))
            await message.channel.send('Proprieties: ' + str(vars(serverData.proprieties)))
            await message.channel.send('Ref. Param.: ' + str(vars(serverData.proprieties.referenceparameters)))
            return

        # Resets all server data to default
        if message.content.startswith('$resetserverdata'):
            if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
                await message.channel.send("You don't have permission to use this command")
                return

            serverData = classes.ServerData()
            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U0001F44D')

        # Clears everything from the serverData.cached
        if message.content.startswith('$clearcache'):
            if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
                await message.channel.send("You don't have permission to use this command")
                return

            serverData.cached = classes.Cache()

            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U0001F44D')
            await message.channel.send("Cleared cache for rotation, dailies, tetrises, etc")

            return

        # Changes the reference values used for the calculations. Has a lot of parameters.
        if message.content.startswith('$updatereferencevalues'):
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

                datahandling.writeserverdata(message.guild.id, serverData, data)
                await message.add_reaction('\U0001F44D')
            except (IndexError, Exception):
                await message.channel.send("Incorrect syntax, correct usage: \n"
                                           "$updatereferencevalues <day>/<month>/<year> <quickplay hscore>"
                                           " <marathon hscore>"
                                           " <lines> <tetrises> <allclears> <tspins> <challenges> <streak> <b2bs>")
                return

        # Clears the serverData.rolechangerids, which stores the IDs of the messages on which upon a reaction being
        # added would trigger a check to try and give a role to the user
        if message.content.startswith('$forgetchangermessages'):
            # I wanted to make it delete them as well but I realized that then the command would need to be run
            # in the channel in which the messages are in, and most people would end up deleting them manually anyway.
            # Either that or even more API calls...
            if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
                await message.channel.send("You don't have permission to use this command")
                return

            serverData.rolechangerids = []
            await message.add_reaction('\U0001F44D')
            datahandling.writeserverdata(message.guild.id, serverData, data)

        # Adds an ID to the serverData.rolechangerids, useful for recycling messages and unecessary pings
        if message.content.startswith('$appendchangerid'):
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
            datahandling.writeserverdata(message.guild.id, serverData, data)

        # Stores a point containing {name: Parameters} which can be later retrieved in order to easily be used on graphs
        # Has lots of parametes.
        if message.content.startswith('$storepoint'):
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
            datahandling.writeserverdata(message.guild.id, serverData, data)

        # Deletes a stored point
        if message.content.startswith('$deletepoint'):
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
            datahandling.writeserverdata(message.guild.id, serverData, data)

        # Clears all stored points
        if message.content.startswith('$clearpoints'):
            serverData.storedpoints = dict()
            await message.add_reaction('\U0001F44D')
            datahandling.writeserverdata(message.guild.id, serverData, data)

        # Lists all stored points
        if message.content.startswith('$listpoints'):
            text = "List of stored points:\n"
            appendabletext = ''

            for key in serverData.storedpoints.keys():
                appendabletext = appendabletext + str(key) + '\n'

            await message.channel.send(text + appendabletext)
            return

        # Prints data stored for a given point
        if message.content.startswith('$printpoint'):
            try:
                name = str(message.content).split(' ')[1]
                name = name.lower()
            except (IndexError, Exception):
                await message.channel.send("Invalid command, correct usage:\n$printpoint <pointname>")
                return

            try:
                point = serverData.storedpoints[name]
            except (AttributeError, Exception) as e:
                await message.channel.send("Point with named {} not found, to see list of stored points use "
                                           "$listpoints".format(name))
                return

            await message.channel.send(str(vars(point)))
            return
