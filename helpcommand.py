import discord
import datahandling
import classes
import texts


def getHelpPage(content: str):
    """
    Gets the number of the page the help command is currently in

    :param content: Content of the help message
    :return: The number of the page, in case of IndexError or ValueError returns 1
    """
    try:
        page = int(content.split(')')[0].split(' ')[2])
        return page
    except (IndexError, ValueError):
        return 1


async def check(message: discord.Message, serverData: classes.ServerData):
    """
    Main check function

    :param message: Message context
    :param serverData: Server data
    """

    if message.content.startswith('$?'):

        # If there are more than 3 help commands active at the same time in a server, stop registering the older one
        if len(serverData.cached.helpmessageids) > 3:
            serverData.cached.helpmessageids.pop(0)

        newMessage = await message.channel.send(texts.menu_help_header)

        await newMessage.add_reaction('⬅')
        await newMessage.add_reaction('➡')

        serverData.cached.helpmessageids.append(newMessage.id)

        datahandling.writeserverdata(message.guild.id, serverData)


async def reaction_check(client, payload):
    """
    Checks for reaction events and changes the pages accordingly

    :param client: Client context
    :param payload: Message payload
    """

    user = payload.member

    if user.id == client.user.id:
        return

    serverData = datahandling.loadData(str(payload.guild_id))

    if payload.message_id not in serverData.cached.helpmessageids:
        return

    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    reaction = payload.emoji

    pages = [
        texts.menu_help_one,
        texts.menu_help_two,
        texts.menu_help_three,
        texts.menu_help_four,
        texts.meun_help_five,
        texts.menu_help_six,
        texts.menu_help_seven,
        texts.menu_help_eight,
        texts.menu_help_nine
    ]

    page = getHelpPage(message.content)

    reaction = str(reaction)

    if reaction == '\U00002B05':
        if page == 1:
            newPage = len(pages)
        else:
            newPage = page - 1

    elif reaction == '\U000027A1':
        if page == len(pages):
            newPage = 1
        else:
            newPage = page + 1

    else:
        return

    newText = pages[newPage - 1]

    await message.edit(content=newText)
