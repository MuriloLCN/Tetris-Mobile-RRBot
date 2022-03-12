import gc

import discord.errors

import classes
import datahandling
import privatedata


async def addOption(message: discord.Message, serverData: classes.ServerData, data: dict):
    """
    Adds a {role: reaction} pair to be used in the creation of a role changing message

    Discord command:
    $addoption &(:reaction:) &(@role)

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """
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
        del reaction, role, newData
        gc.collect()

    except (IndexError, ValueError):
        await message.channel.send("Incorrect syntax, use '$addoption &<reaction> &<role/option text>'")
        return


async def addChanger(message: discord.Message, serverData: classes.ServerData, client: discord.Client, data: dict):
    """
    Adds a changer message to a specific channel so users can alternate roles. Clears added options after creation

    Discord command:
    $addchanger (target channel ID)

    :param message: Message context
    :param serverData: Server data
    :param client: Client context
    :param data: Loaded data
    """
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

    del content, channelId, canal, texto, mensagem, idMensagem, serverData, data, message
    gc.collect()
    return


async def addVote(message: discord.Message, serverData: classes.ServerData, client: discord.Client, data: dict):
    """
    Adds a vote message to a specific channel so users can alternate roles. Clears added options after creation.
    Vote messages, unlike changer messages, do not do anything when reactions are added and are used only for easy
    vote creation.

    Discord command:
    $addvote (target channel ID)

    :param message: Message context
    :param serverData: Server data
    :param client: Client context
    :param data: Loaded data
    """
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

    try:
        mensagem = await canal.send(texto)
    except AttributeError:
        await message.channel.send("The channel you sent was invalid")
        return

    for role in serverData.cached.rolepairs:
        try:
            await mensagem.add_reaction(serverData.cached.rolepairs[role])
        except discord.errors.HTTPException:
            await message.channel.send('Could not add one or more reactions')

    serverData.cached.rolepairs.clear()

    if serverData.rolechangerids[0] == '<NA>':
        serverData.rolechangerids.pop(0)

    datahandling.writeserverdata(message.guild.id, serverData, data)
    del content, channelId, canal, texto, mensagem, serverData, data, message
    gc.collect()
    return


async def check(client, message, serverData, data):
    """
    Main check function

    :param client: Client context
    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """

    if message.content.startswith('$addoption'):
        await addOption(message, serverData, data)

    # Adds a changer message to a specific channel so users can alternate roles.
    # Also clears the options added in the cache
    if message.content.startswith('$addchanger'):
        await addChanger(message, serverData, client, data)

    # Uses the {role: reaction} pairs to create votes instead of changers.
    # Votes, unlike changers, will not have their message IDs stored and reacting on them will not trigger anything.
    if message.content.startswith('$addvote'):
        await addVote(message, serverData, client, data)
