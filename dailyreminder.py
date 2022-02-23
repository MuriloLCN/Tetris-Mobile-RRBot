import datahandling


async def check(client, message, serverData, data):
    if message.content.startswith('$createdailyreminder'):
        try:
            timezone = int(str(message.content).split(' ')[1])
            if timezone > 12 or timezone < -12:
                raise ValueError
        except (IndexError, ValueError):
            await message.channel.send("Incorrect timezone, use integers only for that (-2,-1,0,1,2,...)")
            return

        try:
            hora = int(str(message.content).split(' ')[2].split(':')[0])
            minuto = int(str(message.content).split(' ')[2].split(':')[1])
            if hora < 0 or hora > 23:
                raise ValueError
            if minuto < 0 or minuto > 59:
                raise ValueError
        except (IndexError, ValueError):
            await message.channel.send("Incorrect time, use the form as in '17:45'")
            return

        usuario = message.author.id

        if str(usuario) not in serverData.alarms.keys():

            try:
                canalBot = client.get_channel(int(serverData.proprieties.botchannel))
            except (IndexError, ValueError):
                await message.channel.send("No botmntn channel set")
                return

            await message.add_reaction('\U0001F44D')

            try:
                await canalBot.send('<@here> Copy and paste the command below')
                if timezone > 0:
                    await canalBot.send('$alarm GMT+' + str(timezone) + ' ' + str(minuto) + ' ' + str(hora) +
                                        " * * * $pingalarm &" + str(message.author.id))
                elif timezone == 0:
                    await canalBot.send('$alarm GMT ' + str(minuto) + ' ' + str(hora) +
                                        " * * * $pingalarm &" + str(message.author.id))
                else:
                    await canalBot.send('$alarm GMT' + str(timezone) + ' ' + str(minuto) + ' ' + str(hora) +
                                        " * * * $pingalarm &" + str(message.author.id))
            except AttributeError:
                await message.channel.send("Target channel not found")

            entry = {str(usuario): ['temp', False]}
            serverData.alarms.update(entry)
            datahandling.writeserverdata(message.guild.id, serverData, data)

        else:
            try:
                canalBot = client.get_channel(int(serverData.proprieties.botchannel))
            except (IndexError, ValueError):
                await message.channel.send("No bmtn channel set")
                return

            if str(usuario) in serverData.alarms.keys():
                aID = serverData.alarms[str(usuario)][0]

                try:
                    await canalBot.send("<@here> Copy and paste the command below")
                    await canalBot.send("$deletealarm " + str(aID))
                except AttributeError:
                    await message.channel.send("Target channel not found")

                serverData.alarms.pop(str(usuario), None)
                datahandling.writeserverdata(message.guild.id, serverData, data)

                await message.add_reaction('\U00002B55')

            else:
                await message.channel.send("Could not locate your name in ID list, something went wrong")

    if message.content.startswith('$pingalarm'):
        uID = str(message.content).split('&')[1]
        try:
            canal = client.get_channel(int(serverData.proprieties.reminderchannel))
        except (IndexError, ValueError):
            await message.channel.send("No destination channel set")
            return

        if not serverData.alarms[str(uID)][1]:  # If it's not silenced
            await canal.send('<@' + str(uID) + ">, it's your reminder to do daily tasks")

        else:
            try:
                serverData.cached.donedailies.remove(str(uID))
            except (ValueError, IndexError) as e:
                print('Could not remove ' + str(uID) + ' from doneDailies array: ' + str(e))
                pass
            try:
                serverData.alarms[str(uID)][1] = False

                datahandling.writeserverdata(message.guild.id, serverData, data)
            except Exception as err:
                print('Could not either reRunData or remove ' + str(uID) + ' from silencedAlarmUIDs: ' + str(err))
                return
        return
