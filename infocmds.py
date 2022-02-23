import texts
import privatedata


async def check(client, message):

    if message.content.startswith('$?'):
        usuario = await client.fetch_user(message.author.id)
        try:
            dm = await usuario.create_dm()
        except:
            await message.channel.send("You need to have your DMs open to receive the command list")
            return
        await dm.send(texts.h_1)

        if message.guild.id in privatedata.fullAccessServers:
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

    if message.content.startswith('$publisher'):
        await message.channel.send("Here's a link with the information from this tab:\n"
                                   "shorturl.at/qyK03\n")
        return

    if message.content.startswith('$fullguide'):
        await message.channel.send("You can find the full guide in here:\n"
                                   "shorturl.at/msCR0")
        return

    if message.content.startswith('$requestverify'):
        await message.channel.send("Request sent, you should get contacted soon")
        usuario = await client.fetch_user(privatedata.myid)
        dm = await usuario.create_dm()
        await dm.send('Request for verification coming through:\n'
                      'User: ' + str(message.author) +
                      ' (' + str(message.author.id) + ')' +
                      '\nServer: ' + str(message.guild) +
                      ' (' + str(message.guild.id) + ')')
        return
