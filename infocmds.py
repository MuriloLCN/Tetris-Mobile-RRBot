import discord.errors

import privatedata
import texts


async def requestVerify(client: discord.Client, message: discord.Message):
    """
    Sends a verification request via DMs for a given server. Only verified servers have full access to commands.

    :param client: Client context
    :param message: Message context
    """
    usuario = await client.fetch_user(privatedata.myid)
    dm = await usuario.create_dm()

    # There are no servers in the blacklist currently, this is just to make sure that if someone decides to spam me
    # I can filter the notifications.
    if message.guild.id in privatedata.blacklist:
        return

    await message.channel.send("Request sent, you should get contacted soon")
    await dm.send('Request for verification coming through:\n'
                  'User: ' + str(message.author) +
                  ' (' + str(message.author.id) + ')' +
                  '\nServer: ' + str(message.guild) +
                  ' (' + str(message.guild.id) + ')')
    return


async def check(client: discord.Client, message: discord.Message):
    """
    Main check function

    :param client: Client context
    :param message: Message context
    """

    if message.content.startswith('$tasks'):
        await message.channel.send(texts.tasks)
        return

    if message.content.startswith('$bonus'):
        await message.channel.send(texts.bonus)
        return

    if message.content.startswith('$guides'):
        await message.channel.send(texts.guides)
        return

    if message.content.startswith('$fullguide'):
        await message.channel.send("You can find the full guide in here:\n"
                                   "https://github.com/MuriloLCN/Tetris-Mobile-RRBot/blob/main/README.md")
        return

    if message.content.startswith('$requestverify'):
        await requestVerify(client, message)
