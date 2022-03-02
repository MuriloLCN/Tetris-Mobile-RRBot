import datahandling
import texts


async def check(message, serverData, data):

    # Help command
    if message.content.startswith('$fullbonusping'):
        await message.channel.send(texts.fullbonusping)
        return

    # Add/Remove name from list
    if message.content.startswith('$dailiesdone'):
        name = str(message.author.id)

        if name in serverData.cached.donedailies:
            serverData.cached.donedailies.remove(name)
            await message.add_reaction('\U00002B55')

            # Reactivate the alarm
            if str(name) in serverData.alarms.keys():
                if serverData.alarms[str(name)][1]:
                    serverData.alarms[str(name)][1] = False

        else:
            serverData.cached.donedailies.append(name)

            await message.add_reaction('\U0001F44D')

            # Deactivate the alarm
            if str(name) in serverData.alarms.keys():
                if not serverData.alarms[str(name)][1]:
                    serverData.alarms[str(name)][1] = True

        datahandling.writeserverdata(message.guild.id, serverData, data)

        return

    # Pinging command
    if message.content.startswith('$gotfullbonus'):
        myString = ''

        for name in serverData.cached.donedailies:
            myString += "<@" + str(name) + ">, "

        await message.channel.send("Team now has full bonus, let's get that bread! " + myString)
        serverData.cached.donedailies.clear()

        datahandling.writeserverdata(message.guild.id, serverData, data)
        return
