import texts
import datahandling


async def check(message, serverData, data):
    if message.content.startswith('$savedtetris'):

        name = str(message.author.id)

        if name in serverData.cached.savedtetrises:
            serverData.cached.savedtetrises.remove(name)
            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U00002B55')

        else:
            serverData.cached.savedtetrises.append(name)
            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U0001F44D')
        return

    if message.content.startswith('$tetristask'):
        myString = ''

        while len(serverData.cached.savedtetrises) != 0:
            for name in serverData.cached.savedtetrises:
                myString += "<@" + str(name) + ">, "
                serverData.cached.savedtetrises.remove(name)

        datahandling.writeserverdata(message.guild.id, serverData, data)

        await message.channel.send("Tetris task is live! " + myString)

        return

    if message.content.startswith('$infotetris'):
        await message.channel.send(texts.infotetris)
        return
