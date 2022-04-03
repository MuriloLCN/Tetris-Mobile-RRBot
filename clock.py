import asyncio
import datetime
import math
import dill
import discord
import privatedata


def loadAlarms() -> dict:
    """
    Retrieves stored alarms from file.

    :return: A dict with the alarms data. {userID: [hour, minute, timezone, channelID]}.
    """
    try:
        open('alarmset.pkl', 'x')
    except FileExistsError:
        pass

    with open('alarmset.pkl', 'rb') as f:
        try:
            setdict = dill.load(f)
        except EOFError:
            return dict()
        if type(setdict) != dict:
            return dict()
        return setdict


def writeUpdatedAlarms(updatedAlarmSet: dict):
    """
    Writes new updated data to file.

    :param updatedAlarmSet: Updated (increased/decreased) alarm data dict.
    """
    with open('alarmset.pkl', 'wb') as f:
        dill.dump(updatedAlarmSet, f)


def createReminder(alarmSet: dict, playerID: int, hour: int, minute: int, timezone: int, desiredChannelID: int):
    """
    Creates a new alarm entry in the dataset

    :param alarmSet: Loaded alarm dict
    :param playerID: User ID
    :param hour: Hour for the reminder to be sent
    :param minute: Minute for the reminder to be sent
    :param timezone: Timezone in which the alarm is in
    :param desiredChannelID: Desired channel for mentioning
    """
    # Last item in array indicates whether the alarm is silenced or not. It's off by default.
    entry = {playerID: [hour, minute, timezone, desiredChannelID, False]}
    alarmSet.update(entry)
    writeUpdatedAlarms(alarmSet)


def removeReminder(alarmSet: dict, playerID: int):
    """
    Removes an existing alarm from dataset

    :param alarmSet: Loaded alarm dict
    :param playerID: User ID
    """
    alarmSet.pop(playerID)
    writeUpdatedAlarms(alarmSet)


# Todo: Might be better to store them separatedly and indexed by time in the future,
# so only the necessary ones are loaded. This should suffice for now, though
'''
stored -> dict
{key: values}
{playerID: [hour, minute, timezone, desiredChannelID, isSilenced]}
'''


async def createNewTimer(message: discord.Message):
    """
    Check function for command '$reminder'. Creates/deletes clock points for personal notification.

    :param message: Message context
    """

    try:
        s = str(message.content).split(' ')

        hour = int(s[1].split(':')[0])
        if hour < 0 or hour > 23:
            raise ValueError

        minute = int(s[1].split(':')[1])
        if minute < 0 or minute > 59:
            raise ValueError

        timezone = int(s[2])
        if timezone < -12 or timezone > 12:
            raise ValueError

        desiredChannel = int(s[3].replace('<', '').replace('>', '').replace('#', ''))
        # Any irregular/invalid channels will be caught in here. Discord shows channels as <#ID>

    except (IndexError, ValueError):
        await message.channel.send("Incorrect syntax, correct usage: $reminder <hour>:<minute> <timezone> <#channel>")
        return

    pID = message.author.id

    allAlarms = loadAlarms()

    if pID in allAlarms.keys():
        removeReminder(allAlarms, pID)
        await message.add_reaction('\U00002B55')
    else:
        createReminder(allAlarms, pID, hour, minute, timezone, desiredChannel)
        await message.add_reaction('\U0001F44D')


async def sendMessage(playerID: int, desiredChannelID: int, client: discord.client):
    """
    Sends the reminder message on the desired channel

    :param playerID: User to be mentioned
    :param desiredChannelID: Channel to send the messages
    :param client: Client context
    """
    text = '<@{0}>, it\'s your reminder to do daily tasks'.format(playerID)

    try:
        channel = await client.fetch_channel(desiredChannelID)
    except (discord.errors.NotFound, Exception):
        try:
            usuario = await client.fetch_user(playerID)
            dm = await usuario.create_dm()
            # 123 -> code for DM-only, so you don't receive the entire message
            if desiredChannelID == 123:
                await dm.send(text)
                return
            await dm.send(text + ' (You are receiving this in your DMs because the channel in which you should receive'
                                 ' is either non-existent, forbidden or broken.'
                                 ' Please check with server admins or verify that the ID of the channel you wanted to'
                                 ' receive reminders in is {0})'.format(str(desiredChannelID)))
            return
        except (discord.errors.NotFound, Exception) as e:
            print('Could not ping alarm for player {0} in desired channel {1}. Error: {2}'.format(
                str(playerID), str(desiredChannelID), str(e)
            ))
            return

    await channel.send(text)


async def clockLoop(client: discord.client):
    """
    Function that loops every minute to serve as the internal clock for reminders.

    :param client: Client context
    """

    currentTime = datetime.datetime.now()

    minute = currentTime.minute
    hour = currentTime.hour
    day = currentTime.day

    minute += 1

    if minute >= 60:
        minute = 0
        hour += 1
        if hour >= 24:
            hour = 0
            day += 1

    timeUntilNextMinute = datetime.datetime(currentTime.year, currentTime.month, day, hour, minute, 0, 0) - currentTime

    # Waits until start of next minute to start clock loop
    await asyncio.sleep(math.floor(timeUntilNextMinute.seconds))

    # Host's timezone
    currentTimezone = -3

    while True:
        allAlarms = loadAlarms()

        t = datetime.datetime.now()

        # Current time in GMT 0
        currentHour = int(t.hour - currentTimezone)
        currentMinute = int(t.minute)

        for key in allAlarms.keys():
            if currentHour == (allAlarms[key][0] - allAlarms[key][2]):
                if currentMinute == allAlarms[key][1]:
                    try:
                        isSilenced = allAlarms[key][4]
                    except IndexError:
                        isSilenced = False
                        allAlarms[key].append(isSilenced)
                        writeUpdatedAlarms(allAlarms)
                    if isSilenced:
                        allAlarms[key][4] = False
                        writeUpdatedAlarms(allAlarms)
                    else:
                        await sendMessage(key, allAlarms[key][3], client)

        await asyncio.sleep(60)


async def check(message: discord.Message):
    """
    Main check function

    :param message: Message context
    """

    if message.content.startswith('$reminder'):
        await createNewTimer(message)

    if message.content.startswith('$printalarms'):
        # For debugging
        if message.author.id in privatedata.whitelist:
            p = loadAlarms()
            await message.channel.send(str(p))
