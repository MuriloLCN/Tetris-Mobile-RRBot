import discord.errors
import datahandling
import privatedata


async def check(client, message, serverData, data):
    # Adds an {role: reaction} pair to be used in the creation of a role changing message.
    # When the user reacts with a reaction, the adequate role is given
    if message.content.startswith('$addoption'):
        if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
            await message.channel.send("You don't have permission to use this command")
            return

        try:
            reaction = str(message.content).split('&')[1]
            reaction = ''.join(reaction.split())
            try:
                role = str(message.content).split('&')[2] + '&' + str(message.content).split('&')[3]
            except IndexError:
                role = str(message.content).split('&')[2]

            newData = {role: reaction}

            serverData.cached.rolepairs.update(newData)

            try:
                await message.add_reaction(reaction)
            except discord.errors.HTTPException:
                await message.channel.send("Invalid emoji")
                return

            await message.add_reaction('👍')

            datahandling.writeserverdata(message.guild.id, serverData, data)

        except (IndexError, ValueError):
            await message.channel.send("Incorrect syntax, use '$addrole &<reaction> &<role/option text>'")
            return

    # Adds a changer message to a specific channel so users can alternate roles.
    # Also clears the options added in the cache
    if message.content.startswith('$addchanger'):
        if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
            await message.channel.send("You don't have permission to use this command")
            return

        try:
            content = str(message.content)
            channelId = int(message.content.split(' ')[1])

        except (IndexError, ValueError):
            await message.channel.send("Incorrect syntax, use '$addchanger <channelID>'")
            return

        canal = client.get_channel(channelId)

        texto = "React here to change your role\n"

        for key in serverData.cached.rolepairs:
            if serverData.cached.rolepairs[key] != '':
                texto = texto + str(serverData.cached.rolepairs[key]) + ': ' + str(key) + '\n'

        try:
            mensagem = await canal.send(texto)
        except AttributeError:
            await message.channel.send("Could not find channel with that ID")
            return

        for role in serverData.cached.rolepairs:
            try:
                await mensagem.add_reaction(serverData.cached.rolepairs[role])
            except discord.errors.HTTPException:
                await message.channel.send('Could not add one or more reactions')

        idMensagem = mensagem.id

        serverData.cached.rolepairs.clear()

        serverData.rolechangerids.append(str(idMensagem))

        if serverData.rolechangerids[0] == '<NA>':
            serverData.rolechangerids.pop(0)

        datahandling.writeserverdata(message.guild.id, serverData, data)

    # Uses the {role: reaction} pairs to create votes instead of changers.
    # Votes, unlike changers, will not have their message IDs stored and reacting on them will not trigger anything.
    if message.content.startswith('$addvote'):
        if not (message.author.guild_permissions.administrator or message.author.id in privatedata.whitelist):
            await message.channel.send("You don't have permission to use this command")
            return

        try:
            content = str(message.content)
            channelId = int(message.content.split(' ')[1])

        except (IndexError, ValueError):
            await message.channel.send("Incorrect syntax, use '$addvote <channelID>'")
            return

        canal = client.get_channel(channelId)

        texto = "Vote here!\n"

        for key in serverData.cached.rolepairs:
            if serverData.cached.rolepairs[key] != '':
                texto = texto + str(serverData.cached.rolepairs[key]) + ': ' + str(key) + '\n'

        mensagem = await canal.send(texto)

        for role in serverData.cached.rolepairs:
            try:
                await mensagem.add_reaction(serverData.cached.rolepairs[role])
            except discord.errors.HTTPException:
                await message.channel.send('Could not add one or more reactions')

        serverData.cached.rolepairs.clear()

        if serverData.rolechangerids[0] == '<NA>':
            serverData.rolechangerids.pop(0)

        datahandling.writeserverdata(message.guild.id, serverData, data)
