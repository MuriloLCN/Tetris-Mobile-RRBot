import gc

import discord

import bonuspinging
import calculators
import classes
import dataupdate
import graphs
import infocmds
import rolegiving
import rotation
import savingtetris
import timer
import matchmaking

import privatedata

import requests


def getMemory() -> float:
    """
    Gets the memory used value from DisCloud's api
    :return: The memory value
    """
    results = requests.get("https://discloud.app/status/bot/" + str(privatedata.mybotid), headers={"api-token": privatedata.api_token}).json()
    return float(results['memory'].split('M')[0])


numbertest = [
    '123',
    '1',
    '0',
    '-1',
    '-123',
    '-123123123123123123123123',
    '123123123123123123123123',
    '0.123124212321232123',
    '-0.123232452343123123',
    '123123123123123123.12323232',
    '-11111111111111111111111111111111111111'
]

stringtest = [
    'abc',
    'oiafhuihioeghuiewhfiohewfhuioewfhiewiofioewhfioewifhiewfhioewhfiooiwehfiohweiofhiewfhioewhfio',
    'i23hrui3el-0f1090@!5yh3ionic90219029112413u8tu2903riçasçlldknçççbçnnjkbwiebfw',
    '',
    'Testing «ταБЬℓσ»: 1<2 & 4+1>3, now 20% off!',
    '٩(-̮̮̃-̃)۶ ٩(●̮̮̃•̃)۶ ٩(͡๏̯͡๏)۶ ٩(-̮̮̃•̃).',
    '朝活した',
    '早上住过',
    'Жил утром',
    'Έζησε το πρωί',
    'عاش في الصباح',
    'อยู่แต่เช้า',
    'காலையில் வாழ்ந்தார்',
    'सुबह रहते थे',
    '123.123,123',
    '123232123212321',
    '-3',
    '9.1',
    '9,1'
]

datetest = [
    '1',
    '2020',
    '32',
    '1.4',
    '-2',
    '-2.5',
    '-32',
    '-17',
    '24',
    '25',
    '0',
    '0.0',

]

commands = [
        '$createtimer <number>',
        '$createtimer &<number> &<date>:<date>',
        '$ppscalculator <number>',
        '$setrole <string>',
        '$setnewlimit <number>',
        '$calculateaverage <number> <date>/<date>/<date> ',
        '$royalecalcaverage <number> <number>',
        '$teamptscalculator <number> <number> ',
        '$compcalculator <date>/<date>/<date> <number> <number> <number> <number> <number> <number> <number> <number>',
        '$diffcalculator <number> <number> <number> <number>',
        '$createdailyreminder <date> <date>:<date>',
        '$setreferencepps <number>',
        '$addoption &<string> &<string>',
        '$addchanger <number>',
        '$addvote <number>',
        '$addpoint <string> <date>/<date>/<date> <number> <number> <number> <number> <number> <number> <number> <number> <number>',
        '$updatereferencevalues <date>/<date>/<date> <number> <number> <number> <number> <number> <number> <number> <number> <number>',
        '$appendchangerid <number>',
        '$storepoint <string> <date>/<date>/<date> <number> <number> <number> <number> <number> <number> <number> <number> <number>',
        '$deletepoint <string>',
        '$loadpoint <string>',
        '$printpoint <string>',
        '$enter',
        '$leave',
        '$savedtetris',
        '$dailiesdone',
        '$loadallpoints',
        '$generategraphs ABCD'
]

numbers = '1'

strings = 'test'

dates = '7'

sequential_commands = [
    ['$loadallpoints', '$generategraphs ABCD'],
    ['$dailiesdone', '$gotfullbonus'],
    ['$savedtetris', '$tetristask']
]


async def check_command(message: discord.Message, serverdata: classes.ServerData, client: discord.Client, matches: classes.Match, value: int):
    """
    Runs the list of commands to be checked with some wacky parameters
    """
    for command in commands:
        newcommand = command.replace('<', '{').replace('>', '}')
        for i in range(value):
            # RANDOM is no longer used to test parameters, instead it simply goes through the lists normally
            random_num = numbertest[i % len(numbertest)]
            random_string = stringtest[i % len(stringtest)]
            random_date = datetest[i % len(datetest)]
            newcommands = newcommand.format(number=random_num, string=random_string, date=random_date)
            message.content = newcommands
            await all_checks(message, serverdata, client, matches)
    del random_num, random_string, random_date, newcommands, newcommand
    gc.collect()


async def stress_test(message: discord.Message, serverdata: classes.ServerData, client: discord.Client, matches: classes.Match, value: int):
    """
    Runs the list of commands with somewhat normal parameters for stress testing
    """
    for command in commands:
        newcommand = command.replace('<', '{').replace('>', '}')
        for i in range(value):
            newcommands = newcommand.format(number=numbers, string=strings, date=dates)
            message.content = newcommands
            await all_checks(message, serverdata, client, matches)

    for arrcommands in sequential_commands:
        for i in range(value):
            message.content = arrcommands[0]
            await all_checks(message, serverdata, client, matches)
            message.content = arrcommands[1]
            await all_checks(message, serverdata, client, matches)
    del newcommand, newcommands
    gc.collect()


async def all_checks(message: discord.Message, serverdata: classes.ServerData, client: discord.Client, matches: classes.Match):
    """
    Compares the edited message content with all current modules' check() command to run the given command
    """
    await bonuspinging.check(message, serverdata)
    await calculators.check(message, serverdata)
    await dataupdate.check(message, serverdata)
    await graphs.check(message, serverdata)
    await infocmds.check(client, message)
    await rolegiving.check(client, message, serverdata)
    await rotation.check(message, serverdata, client)
    await savingtetris.check(message, serverdata)
    await timer.check(message, serverdata)
    await matchmaking.check(message, matches, client)


async def check(message, serverdata, client, matches):
    """
    Main check function

    :param message: Message context
    :param serverdata: Server data
    :param client: Client context
    :param matches: Match object
    """
    if message.content.startswith('$$test'):

        try:
            value = int(str(message.content).split(' ')[1])
            if value <= 0:
                return
        except (IndexError, ValueError):
            return

        if message.author.id != privatedata.myid:
            return

        # First check is simply to see if weird inputs break the command
        await check_command(message, serverdata, client, matches, value)
        # Only needs to be checked again when new features are added
        print('Compatibility test done, starting stress test')
        # Second check is used for a better measurement of RAM usage for each command
        await stress_test(message, serverdata, client, matches, value)

        # print('RAM after: {}'.format(getMemory()))
        del client, matches, message, serverdata
        gc.collect()
