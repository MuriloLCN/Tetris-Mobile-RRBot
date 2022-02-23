import re

import discord

import datahandling
import privatedata
import classes


def switch_role(new_role, serverID, dataClass, data):
    dataClass.currentRole = new_role
    datahandling.writeserverdata(serverID, dataClass, data)


def switch_limit(new_time, serverID, dataClass, data):
    dataClass.currentLimit = new_time
    datahandling.writeserverdata(serverID, dataClass, data)


async def check(message, serverData, data):

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

        if message.content.startswith('$printserverdata'):
            if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
                await message.channel.send("You don't have permission to use this command")
                return

            await message.channel.send('Server data: ' + str(vars(serverData)))
            await message.channel.send('Cached: ' + str(vars(serverData.cached)))
            await message.channel.send('Proprieties: ' + str(vars(serverData.proprieties)))
            await message.channel.send('Ref. Param.: ' + str(vars(serverData.proprieties.referenceparameters)))
            return

        if message.content.startswith('$resetserverdata'):
            if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
                await message.channel.send("You don't have permission to use this command")
                return

            serverData = classes.ServerData()
            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U0001F44D')

        if message.content.startswith('$clearcache'):
            if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
                await message.channel.send("You don't have permission to use this command")
                return

            serverData.cached = classes.Cache()

            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U0001F44D')
            await message.channel.send("Cleared cache for rotation, dailies, tetrises, etc")

            return

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

                serverData.proprieties.referenceparameters = classes.Parameters(
                    year, month, day, qphs, mths, lines, tet, allc, tsd, chl, strk
                )

                datahandling.writeserverdata(message.guild.id, serverData, data)
                await message.add_reaction('\U0001F44D')
            except (IndexError, Exception):
                await message.channel.send("Incorrect syntax, correct usage: \n"
                                           "$updatereferencevalues <day>/<month>/<year> <quickplay hscore>"
                                           " <marathon hscore>"
                                           " <lines> <tetrises> <allclears> <tspins> <challenges> <streak>")
                return

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
