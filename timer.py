import asyncio
import datetime
import math


async def datetimeCountdown(message, serverData):
    content = str(message.content)

    try:
        timezone = int(content.split('&')[1])
        hour = int(content.split('&')[2].split(':')[0])
        minute = int(content.split('&')[2].split(':')[1])
    except ValueError:
        await message.channel.send("One or more of your values were not valid or were missing")
        return
    except IndexError:
        await message.channel.send("One or more of your parameter delimiters was incorrect or was missing")
        return

    if timezone > 12 or timezone < -12:
        await message.channel.send("Timezones have to be between 12 and -12")
        return

    if hour > 23 or hour < 0:
        await message.channel.send("Hours have to be between 0 and 23")
        return

    if minute > 59 or minute < 0:
        await message.channel.send("Minutes have to be between 0 and 59")
        return

    meuGmt = datetime.timedelta(hours=-3)  # <-- Host's timezone
    ddt = datetime.timezone(meuGmt)
    tempoAgora = datetime.datetime.now(ddt)

    dateGmt = datetime.timedelta(hours=timezone)
    ddn = datetime.timezone(dateGmt)
    tempoLa = datetime.datetime(tempoAgora.year, tempoAgora.month, tempoAgora.day, hour, minute, 0, 0, ddn)

    diferencaDeTempo = tempoLa - tempoAgora
    segundos = diferencaDeTempo.seconds
    minutos = segundos / 60
    minutos = math.floor(minutos)

    if float(minutos) > serverData.proprieties.currentlimit:
        await message.channel.send("Time exceeds current limit of {} minutes"
                                   .format(serverData.proprieties.currentlimit))
        return

    await message.channel.send("Timer created to {} minutes from now".format(minutos))
    await asyncio.sleep(segundos)
    await message.channel.send("{}, join now!".format(serverData.proprieties.currentrole))


async def normalCountdown(message, serverData):
    content = str(message.content)
    try:
        minutes = str(content).split(' ')[1]
        minutes = float(minutes)
    except IndexError:
        await message.channel.send("One or more of your parameters were missing")
        return
    except ValueError:
        await message.channel.send("One or more of yout parameters were invalid")
        return

    if minutes < 0:
        await message.channel.send("Minutes cannot be negative")
        return
    if minutes > serverData.proprieties.currentlimit:
        await message.channel.send("Time exceeds current server limit of {} minutes"
                                   .format(serverData.proprieties.currentlimit))
        return

    await message.channel.send("Timer created to {} minutes from now".format(minutes))
    await asyncio.sleep(math.floor(minutes * 60))
    await message.channel.send("{}, join now!".format(serverData.proprieties.currentrole))


async def check(message, serverData):
    if message.content.startswith('$createtimer'):

        myContent = str(message.content).split('&')

        if len(myContent) == 3:
            await datetimeCountdown(message, serverData)
        elif len(myContent) == 1:
            if len(str(message.content).split(' ')) >= 3:
                await message.channel.send("It looks like you were trying to use the GMT form without delimiters or "
                                           "had an extra space, please double check to make sure you've used the "
                                           "correct timer")
            await normalCountdown(message, serverData)
        else:
            await message.channel.send("Incorrect syntax, use '$?' for help")
