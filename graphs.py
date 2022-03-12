import datetime
import math

import discord
import matplotlib.pyplot as plt
import numpy as np

import calculators
import classes
import datahandling

import gc

TWO_PI = 6.283185307179586
PI = TWO_PI / 2


def getscale(value: float) -> int:
    """
    Gets the value needed to divide a number in order to make it between 0-1

    :param value: The number to be checked (float)
    :return: The scale of the number (int)
    """
    if value < 0:
        value = -1 * value

    scl = 1

    while value > 10:
        value = value/10
        scl += 1

    return scl


def attLinspace(start: float, end: float, num: int):
    """
    A simple re-implementation of np.linspace

    :param start: Starting value (float)
    :param end: Ending value (float)
    :param num: Number of elements (int)
    :return: an evenly spaced list with 'num' values spaced between start and end (list)
    """
    # Re-invented the wheel while trying to find a memory leak, decided to keep it
    arr = []
    step = (end - start)/(num - 1)
    for i in range(num):
        arr.append(start + (i*step))

    return arr


def attDegrees(val: float) -> float:
    """
    A simple re-implementation of np.degrees

    :param val: Radian value to be converted into degrees
    :return: Converted degree
    """
    return round((val * 180)/PI)


async def addPointCMD(message: discord.Message, serverData: classes.ServerData, data: dict):
    """
    Adds a point to be used in the graph making (note: different from $storepoint, which saves a point to be loaded).
    This point will get deleted once the graphs are made.

    Discord command:
    $addpoint (point name) (day)/(month)/(year) (quick play highscore) (marathon highscore) (lines cleared) (tetrises)
    (all clears) (t-spins) (challenges) (login streak) (back-to-backs)

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """
    try:
        texts = str(message.content).split(' ')
        username = texts[1]
        date = texts[2]
        quickplayhs = int(texts[3])
        marathonhs = int(texts[4])
        lines = int(texts[5])
        tetrises = int(texts[6])
        allclears = int(texts[7])
        tspins = int(texts[8])
        challenges = int(texts[9])
        streak = int(texts[10])
        btb = int(texts[11])
    except IndexError:
        await message.channel.send("One or more of your parameters were missing\n"
                                   "Correct usage: "
                                   "$addpoint username d/m/y qphs mths lines tetris allc tspins chall strk b2b")
        return
    except ValueError:
        await message.channel.send("One or more of your values were invalid")
        return
    except Exception as e:
        print("Error: {}".format(str(e)))
        return

    try:
        day = int(date.split('/')[0])
        month = int(date.split('/')[1])
        year = int(date.split('/')[2])
    except IndexError:
        await message.channel.send("One or more of your date parameters were missing")
        return
    except ValueError:
        await message.channel.send("One or more of your date values were invalid")
        return
    except Exception as e:
        print("Error: {}".format(str(e)))
        return

    #  {username: Parameters()}
    try:
        d = datetime.date(year, month, day)
    except ValueError:
        await message.channel.send("Invalid date")
        return

    del d

    point = {username: classes.Parameters(
        year, month, day, quickplayhs, marathonhs, lines, tetrises, allclears, tspins, challenges, streak, btb
    )}

    serverData.cached.datapoints.update(point)

    await message.add_reaction('\U0001F44D')
    datahandling.writeserverdata(message.guild.id, serverData, data)


async def loadPointCMD(message: discord.Message, serverData: classes.ServerData, data: dict):
    """
    Loads a stored point to be used in graph making

    Discord command:
    $loadpoint (point name)

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """
    try:
        name = str(message.content).split(' ')[1]
        name = name.lower()
    except (IndexError, Exception):
        await message.channel.send("Invalid command, correct usage:\n$loadpoint <pointname>")
        return

    try:
        point = serverData.storedpoints[name]
        pointentry = {name: point}
    except (AttributeError, Exception):
        await message.channel.send("Point with name {} not found, to see list of stored points use "
                                   "$listpoints".format(name))
        return

    serverData.cached.datapoints.update(pointentry)
    await message.add_reaction('\U0001F44D')
    datahandling.writeserverdata(message.guild.id, serverData, data)


async def loadAllPointsCMD(message: discord.Message, serverData: classes.ServerData, data: dict):
    """
    Loads all stored point to use in graph making

    Discord command:
    $loadallpoints

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """
    for key in serverData.storedpoints.keys():
        pointentry = {key: serverData.storedpoints[key]}
        serverData.cached.datapoints.update(pointentry)

    await message.add_reaction('\U0001F44D')
    await message.channel.send("Loaded {} point(s)".format(str(len(serverData.storedpoints))))
    datahandling.writeserverdata(message.guild.id, serverData, data)


async def graphA(message: discord.Message, serverData: classes.ServerData, usernames: list, parameters: list):
    """
    Generates the first graph (activity score x technique score)

    :param message: Message context
    :param serverData: Server data
    :param usernames: List of point's names
    :param parameters: List of point's parameters
    """
    scorex = []
    scorey = []

    for i in range(len(usernames)):
        res = calculators.compcalculator(serverData, parameters[i])
        scorex.append(res[0])
        scorey.append(res[1])
        plt.text(res[0], res[1], usernames[i])

    plt.xlabel('Activity score')
    plt.ylabel('Technique score')
    plt.title('Activity score x technique score')
    plt.scatter(scorex, scorey)
    plt.savefig('temp.png')

    await message.channel.send(file=discord.File('temp.png'))
    plt.cla()
    plt.clf()
    plt.close()

    del scorex, scorey, res
    gc.collect()


async def graphB(message: discord.Message, qphs: list, linec: list, avglinesday: list, techscore: list, specialrate: list, usernames: list):
    """
    Generates the second graph (Radar chart)

    :param message: Message context
    :param qphs: List of points' quick play highscore
    :param linec: List of points' lines cleared
    :param avglinesday: List of points' average lines per day
    :param techscore: List of points' technique score
    :param specialrate: List of points' special line clears rate
    :param usernames: List of points' names
    """
    # TODO: Try to find another way of generating radar charts to try and fix the memory leak the occurs here

    # I've traced the memory leak to happen in here and in one of the MatPlotLib's functions, though after some
    # tweaks it's nowhere nearly as bad as it was initially. But still happens.

    try:
        # The number needed to divide the data points as to make the highest values between 0 and 1

        # Note: Most parameters are no longer used in the graph, though they might be used in the future
        getqp = getscale(max(qphs))
        qpscale = 10 ** getqp
        # mtscale = 10 ** getscale(max(mths))
        getlines = getscale(max(linec))
        linescale = 10 ** getlines
        # tetrscale = 10 ** getscale(max(tetrises))
        # allcscale = 10 ** getscale(max(allc))
        # tspscale = 10 ** getscale(max(tsp))
        # chlscale = 10 ** getscale(max(chl))
        # strkscale = 10 ** getscale(max(strk))
        # btbscale = 10 ** getscale(max(btb))

        getavg = getscale(max(avglinesday))
        avglinesdayscale = (10 ** getavg)

        gettech = getscale(max(techscore))
        techscorescale = 10 ** gettech

        getspecial = getscale(max(specialrate))
        specialratescale = 10 ** getspecial

        # Just a quick formatting in the names to help seeing the scales

    except (IndexError, ValueError):
        await message.channel.send("There are no data points for the calculations")
        return

    # categories = ['Quick Play HS', 'Marathon HS', 'Lines cleared', 'Tetrises', 'All clears', 'TSpins',
    #              'Challenges completed', 'Login Streak', 'Back-to-backs']
    categories = ['Lines per day (10^{})'.format(str(getavg)),
                  'Technique Score (10^{})'.format(str(gettech)),
                  'Quick Play HS (10^{})'.format(str(getqp)),
                  'Total Lines (10^{})'.format(str(getlines)),
                  'Special Line Clears Rate (10^{})'.format(str(getspecial))]
    categories = [*categories, categories[0]]

    # ref = serverData.proprieties.referenceparameters

    referencePlayer = [1, 1, 1, 1,
                       1]  # This is just here to get the lengh, reference data is no longer used on the graph
    referencePlayer = [*referencePlayer, referencePlayer[0]]

    label_loc = attLinspace(0, TWO_PI, len(referencePlayer))
    deg_arr = []
    for i in label_loc:
        deg_arr.append(attDegrees(i))
    deg_arr = np.array(deg_arr)
    label_loc = np.array(label_loc)

    plt.figure(figsize=(8, 8), num=1, clear=True)
    plt.subplot(polar=True)
    # plt.plot(label_loc, referencePlayer, label='Reference Player')
    plt.title('All purpose visualizer')

    for i in range(len(usernames)):
        # Everything is divided by scale so that it all goes between 0 and 1
        # playerdata = [qphs[i]/qpscale, mths[i]/mtscale, linec[i]/linescale, tetrises[i]/tetrscale,
        #              allc[i]/allcscale, tsp[i]/tspscale, chl[i]/chlscale, strk[i]/strkscale, btb[i]/btbscale]
        playerdata = [avglinesday[i] / avglinesdayscale, techscore[i] / techscorescale, qphs[i] / qpscale,
                      linec[i] / linescale, specialrate[i] / specialratescale]
        playerdata = [*playerdata, playerdata[0]]
        plt.plot(label_loc, playerdata, label=usernames[i])

    # lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)

    # It says that they're not used but they are needed for the graph to be made.
    # They have to be manually cleaned up because for some reason leaving them
    # eats up RAM like it's a Christmas supper

    lines, labels = plt.thetagrids(deg_arr, labels=categories)
    plt.legend()
    plt.savefig('temp.png')

    await message.channel.send(file=discord.File('temp.png'))
    plt.cla()
    plt.clf()
    plt.close()

    del playerdata, label_loc, lines, labels, deg_arr, referencePlayer, categories, getqp, getlines
    del qpscale, linescale, getavg, avglinesdayscale, gettech, techscorescale, getspecial, specialratescale

    gc.collect()


async def graphC(message: discord.Message, usernames: list, tetrises: list, tsp: list, btb: list, linec: list):
    """
    Generates the third graph (special line clears rate x back-to-backs line clears rate)

    :param message: Message context
    :param usernames: List of points' names
    :param tetrises: List of points' tetrises
    :param tsp: List of points' t-spins
    :param btb: List of points' back-to-backs
    :param linec: List of points' lines cleared
    """
    ratex = []
    ratey = []

    for i in range(len(usernames)):
        res = calculators.diffcalculator(tetrises[i], tsp[i], btb[i], linec[i])
        ratex.append(res[0])
        ratey.append(res[2])
        plt.text(res[0], res[2], usernames[i])

    plt.xlabel('Special line clears rate')
    plt.ylabel('B2B line clears rate')
    plt.title('Special line clears rate x b2b line clears rate')
    plt.scatter(ratex, ratey)
    plt.savefig('temp.png')

    await message.channel.send(file=discord.File('temp.png'))
    plt.cla()
    plt.clf()
    plt.close()

    del ratex, ratey, res
    gc.collect()


async def graphD(message: discord.Message, serverData: classes.ServerData, accountLife: list, usernames: list, linec: list):
    """
    Generates the fourth graph (account life x time played per day)

    :param message: Message context
    :param serverData: Server data
    :param accountLife: List of points' account life in days
    :param usernames: List of points' names
    :param linec: List of points' lines cleared
    """
    timeperday = []
    acclife = []

    for i in range(len(usernames)):
        res = calculators.calculateaverage(accountLife[i].days, linec[i], serverData.proprieties.referencepps)
        res = res * 60
        timeperday.append(res)
        plt.text(accountLife[i].days, res, usernames[i])

    for i in accountLife:
        acclife.append(int(i.days))

    plt.xlabel('Account life (in days)')
    plt.ylabel('Time played per day (at {} pps, in minutes)'.format(str(serverData.proprieties.referencepps)))
    plt.title('Time played per day x account life')
    plt.scatter(acclife, timeperday)
    plt.savefig('temp.png')

    await message.channel.send(file=discord.File('temp.png'))
    plt.cla()
    plt.clf()
    plt.close()

    del timeperday, acclife, res
    gc.collect()


async def generateGraphsCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Generates graphs

    Discord command:
    $generategraphs (any subset of the string 'ABCD', ex: A, BC, ABD, BCD, ABDC...)

    :param message: Message context
    :param serverData: Server data
    """
    # Get the parameter string
    try:
        stringy = str(message.content).split(' ')[1].upper()
    except (IndexError, Exception):
        await message.channel.send("Please pass a parameter (A, B, C, AC, ACD, etc.)")
        return

    if len(serverData.cached.datapoints) <= 1:
        await message.channel.send("You need at least two data points to generate a graph")
        return

    parameters = []

    accountLife = []  # datetime.timedelta

    usernames = []

    qphs = []
    # mths = []
    linec = []
    tetrises = []
    # allc = []
    tsp = []
    # chl = []
    # strk = []
    btb = []

    # Requested in v10
    avglinesday = []
    techscore = []
    specialrate = []

    if len(serverData.cached.datapoints) == 0:
        await message.channel.send("No data points defined")
        return

    for key in serverData.cached.datapoints:
        entry = serverData.cached.datapoints[key]  # Parameters() object

        usernames.append(key)
        parameters.append(entry)

        accountLife.append(datetime.date.today() - entry.joindate)
        qphs.append(entry.quickplayhs)
        # mths.append(entry.marathonhs)
        linec.append(entry.lines)
        tetrises.append(entry.tetrises)
        # allc.append(entry.allclears)
        tsp.append(entry.tspins)
        # chl.append(entry.challenges)
        # strk.append(entry.streak)
        btb.append(entry.backtoback)

        avglinesday.append(math.floor(entry.lines / (datetime.date.today() - entry.joindate).days))

        techscore.append(calculators.techniqueScore(entry.quickplayhs, entry.marathonhs, entry.allclears,
                                                    entry.tspins, entry.tetrises,
                                                    serverData.proprieties.referenceparameters))

        specialrate.append(calculators.diffcalculator(entry.tetrises, entry.tspins, entry.backtoback, entry.lines)[0])

    plt.style.use('seaborn-whitegrid')

    # Activity score x talent score
    if 'A' in stringy:
        await graphA(message, serverData, usernames, parameters)

    # Complete data graph
    # Huge thanks to BlakeD38! This radar graph would not have been possible without him
    if 'B' in stringy:
        await graphB(message, qphs, linec, avglinesday, techscore, specialrate, usernames)

    # Special rate x b2b per special
    if 'C' in stringy:
        await graphC(message, usernames, tetrises, tsp, btb, linec)

    # time played per day x account lifespan
    if 'D' in stringy:
        await graphD(message, serverData, accountLife, usernames, linec)

    del parameters, accountLife, usernames, qphs, linec, tetrises, tsp, btb, avglinesday, techscore
    del specialrate, entry, key, message, serverData, stringy
    gc.collect()


async def check(message, serverData, data):
    """
    Main check function

    Discord commands:
    $addpoint
    $loadpoint
    $loadallpoints
    $generategraphs

    :param message: Message context
    :param serverData: Server data
    :param data: Loaded data
    """

    if message.content.startswith('$addpoint'):
        await addPointCMD(message, serverData, data)

    if message.content.startswith('$loadpoint'):
        await loadPointCMD(message, serverData, data)

    if message.content.startswith('$loadallpoints'):
        await loadAllPointsCMD(message, serverData, data)

    if message.content.startswith('$generategraphs'):
        await generateGraphsCMD(message, serverData)
