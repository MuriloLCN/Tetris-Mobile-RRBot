import texts
import datahandling


# Compares two queues to see if there are matching interests
async def compareQueue(message, entering, entryList, exitList, dataClass, data):

    user = str(message.author.id)

    if entering:
        comparative = exitList.copy()

    else:
        comparative = entryList.copy()

    if len(comparative) > 0:
        await message.channel.send(
            "It's a match! <@" + str(user) + "> and <@" + str(comparative[0]) + "> can switch!"
        )
        if entering:
            dataClass.cached.entryqueue.remove(user)
            dataClass.cached.exitqueue.pop(0)
        else:
            dataClass.cached.exitqueue.remove(user)
            dataClass.cached.entryqueue.pop(0)

    datahandling.writeserverdata(message.guild.id, dataClass, data)


async def check(message, serverData, data):
    # Help command
    if message.content.startswith('$rotation'):
        await message.channel.send(texts.rotation)
        return

    # Join the entry queue
    if message.content.startswith('$enter'):

        name = message.author.id

        if str(name) in serverData.cached.entryqueue:
            serverData.cached.entryqueue.remove(str(name))
            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U00002B55')

        else:
            serverData.cached.entryqueue.append(str(name))
            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U0001F44D')

            await compareQueue(message, True, serverData.cached.entryqueue, serverData.cached.exitqueue, serverData, data)

        return

    # Join the exit queue
    if message.content.startswith('$leave'):

        name = message.author.id

        if str(name) in serverData.cached.exitqueue:
            serverData.cached.exitqueue.remove(str(name))
            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U00002B55')

        else:
            serverData.cached.exitqueue.append(str(name))
            datahandling.writeserverdata(message.guild.id, serverData, data)
            await message.add_reaction('\U0001F44D')
            await compareQueue(message, False, serverData.cached.entryqueue, serverData.cached.exitqueue, serverData, data)

        return

    # Mentions the next person in queue waiting to enter and removes them from it
    if message.content.startswith('$freespot'):

        serverData = datahandling.getserverdata(message.guild.id, data)

        if len(serverData.cached.entryqueue) > 0:
            name = str(serverData.cached.entryqueue[0])
            await message.channel.send("There's an open spot, <@" + name + ">, you can enter")
            serverData.cached.entryqueue.pop(0)
            datahandling.writeserverdata(message.guild.id, serverData, data)

        else:
            await message.channel.send("The entry queue is empty")

        return
