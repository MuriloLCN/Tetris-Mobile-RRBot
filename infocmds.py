import discord.errors

import privatedata
import texts


async def check(client, message):

    # Self explanatory, simply sends a help message
    if message.content.startswith('$?'):
        usuario = await client.fetch_user(message.author.id)
        try:
            dm = await usuario.create_dm()
        except (discord.errors.NotFound, discord.errors.Forbidden, Exception):
            await message.channel.send("You need to have your DMs open to receive the command list")
            return
        await dm.send(texts.h_1)

        if message.guild.id not in privatedata.blacklist:
            await dm.send(texts.h_2)
            await dm.send(texts.h_3)

        await message.add_reaction('\U0001F44D')

        return

    if message.content.startswith('$tasks'):
        await message.channel.send(texts.tasks)
        return

    if message.content.startswith('$bonus'):
        await message.channel.send(texts.bonus)
        return

    if message.content.startswith('$modes'):
        await message.channel.send(texts.modes)
        return

    if message.content.startswith('$seasons'):
        await message.channel.send(texts.seasons)
        return

    if message.content.startswith('$guides'):
        await message.channel.send(texts.guides)
        return

    # This tab is no longer available after the new studios bought over and all that was written became obsolete
    if message.content.startswith('$publisher'):
        await message.channel.send("Page under construction")
        return

    if message.content.startswith('$fullguide'):
        await message.channel.send("You can find the full guide in here:\n"
                                   "shorturl.at/bcejC")
        return

    # Simply makes the bot send a DM to me (PyrooKil) as to manually add a new server to the verified list.
    # It looks like gatekeeping at first but having that helpline of comms really help to keep any malicious intent at
    # bay. Users can be trolls sometimes...
    if message.content.startswith('$requestverify'):
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
