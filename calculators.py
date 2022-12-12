import datetime
import gc
import math

import discord

import classes
import texts


# Raw calculation commands
def getDays(day: int, month: int, year: int) -> int:
    """
    Gets the number of days passed between today and the target date

    :param day: The target date's day (int)
    :param month: The target date's month (int)
    :param year: The target date's year (int)
    :return: The number of days passed (int)
    """
    todayDate = datetime.date.today()
    dateJoined = datetime.date(year, month, day)
    return int(abs(todayDate - dateJoined).days)


def activityScore(lines: int, challenges: int, streak: int, days: int, ref: classes.Parameters) -> float:
    """
    Calculates the activity score for a given player, based on the formula from BlakeD38

    :param lines: The number of lines the player has cleared since they started playing (int)
    :param challenges: The number of challenges the player has completed since they started playing (int)
    :param streak: The player's login streak (int)
    :param days: The length of the player's account life (int)
    :param ref: The reference parameters object currently used in the server (classes.Parameters)
    :return: The calculated activity score (float)
    """
    refdate = datetime.date.today() - ref.joindate
    return ((refdate.days/days) * (((lines / ref.lines) + 20 * (challenges / ref.challenges) + 50 * (streak /
                                                                                                     ref.streak))))/100


def techniqueScore(quickPlay: int, marathon: int, allClears: int, tspins: int, tetrises: int, ref: classes.Parameters) -> float:
    """
    Calculates the technique/talent score for a given player, based on the formula from BlakeD38

    :param quickPlay: The player's highscore in the quick play mode (int)
    :param marathon: The player's highscore in the marathon mode (int)
    :param allClears: The number of All Clears the player has ever performed (int)
    :param tspins: The number of T-Spins the player has ever performed (int)
    :param tetrises: The number of Tetris Line Clears the player has ever performed (int)
    :param ref: The reference parameters object currently used in the server (int)
    :return: The calculated technique score (float)
    """
    return (9 * (quickPlay / ref.quickplayhs) + 0.001 * (marathon / ref.marathonhs) + 3 * (allClears / ref.allclears) +
            (tspins/ref.tspins) + 0.1 * (tetrises/ref.tetrises)) / (9+0.001+3+1+0.1)


def calculatepps(lines: int) -> float:
    """
    Calculates the player's average pieces per second in a Quick Play game

    :param lines: The number of lines cleared by the end of the three minute mark (int)
    :return: The player's estimated PPS (float)
    """
    return round((lines * 2.5)/180, 3)  # PPS


def calculateaverage(deltadays: int, lines: int, pps: float) -> float:
    """
    Calculates the average time played per day for a given player

    :param deltadays: The length of the player's account life (int)
    :param lines: The number of lines the player has cleared since they started playing (int)
    :param pps: The reference PPS value set by the server in which the command is used, default is 1.66 (float)
    :return: The estimated time played per day, in hours (float)
    """

    # Just in case someone needs an explanation
    # floor(linesCleared/deltaDays) -> lines per day
    # that * 2.5 -> pieces per day
    # that / PPS -> seconds per day (needed to place those pieces)
    # that / 60 / 60 -> converting to hours
    return (((math.floor(lines / deltadays) * 2.5) / pps) / 60) / 60  # Hours played per day


def diffcalculator(tetrises: int, tspins: int, btb: int, lines: int) -> list:
    """
    Calculates how often a player uses back-to-backs and difficult line clears (Tetrises and T-Spins) in their matches

    :param tetrises: The number of Tetris Line Clears the player has ever performed (int)
    :param tspins: The number of T-Spins the player has ever performed (int)
    :param btb: The number of Back-to-Backs the player has ever performed (int)
    :param lines: The number of lines the player has cleared since they started playing (int)
    :return: List with three rates [(float)]: [Special per total, back-to-backs per special, back-to-backs per total]
    """
    rate = tetrises / (tetrises + tspins)
    return [
        1 - ((lines - (tetrises * 4) - (tspins * 2)) / lines),  # Special line clear rate
        btb / (tspins + tetrises),  # Back-to-backs per special line clears
        (btb * (2 + (2 * rate))) / lines  # Back-to-backs per total line clears
    ]


def compcalculator(serverData: classes.ServerData, parameters: classes.Parameters) -> list:
    """
    Calculates the activity and technique score for a given player compared with the server's default parameter data

    :param serverData: The current server's data (classes.ServerData)
    :param parameters: The parameters with data from the target player (classes.Parameters)
    :return: A list with the activity and technique score [(float)]: [Activity score, Technique score]
    """
    ref = serverData.proprieties.referenceparameters
    return [
        # Player activity / Reference activity
        activityScore(parameters.lines, parameters.challenges, parameters.streak, getDays(parameters.joindate.day,
        parameters.joindate.month, parameters.joindate.year), ref) / activityScore(ref.lines, ref.challenges, ref.streak,
        getDays(ref.joindate.day, ref.joindate.month, ref.joindate.year), ref),

        # Player technique / Reference technique
        techniqueScore(parameters.quickplayhs, parameters.marathonhs, parameters.allclears, parameters.tspins,
        parameters.tetrises, ref) / techniqueScore(ref.quickplayhs, ref.marathonhs, ref.allclears, ref.tspins,
        ref.tetrises, ref)
    ]


# Calculator commands
async def ppsCalculatorCMD(message: discord.Message):
    """
    Calculates the player's average PPS in a quick play game

    Discord command:
    $ppscalculator (lines cleared by the end of the 3 minutes)

    :param message: Message context
    """
    try:
        lines = int(str(message.content).split(' ')[1])
    except (ValueError, IndexError):
        await message.channel.send("Incorrect syntax, correct usage: '$ppscalculator <lines>'."
                                   " Example: '$ppscalculator 120'.")
        return

    pps = calculatepps(lines)

    await message.channel.send("Your PPS is around " + str(pps) + "PPS.")
    del lines, pps, message
    gc.collect()


async def calculateAverageCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Calculates the average time played per day of an user

    Discord command:
    $calculateaverage (total lines cleared) (day)/(month)/(year)

    :param message: Message context
    :param serverData: Server data
    """
    try:
        linesClearedString = str(str(message.content).split(' ')[1])

    except IndexError:
        await message.channel.send(texts.calculateaverage_exception_one)

        return

    try:
        linesCleared = int(linesClearedString)
    except (ValueError, IndexError):
        await message.channel.send("Incorrect parameter 'number of lines', it must be "
                                   "an integer")
        return

    try:
        monthJoined = int(str(str(message.content).split(' ')[2]).split('/')[0])
        dayJoined = int(str(str(message.content).split(' ')[2]).split('/')[1])
        yearJoined = int(str(str(message.content).split(' ')[2]).split('/')[2])
    except (ValueError, IndexError):
        await message.channel.send("Incorrect parameter 'join date', it must be of the "
                                   "form 'month/day/year', all must be integers and "
                                   "separated by '/'")

        return

    todayDate = datetime.date.today()

    try:
        dateJoined = datetime.date(yearJoined, monthJoined, dayJoined)
    except ValueError:
        await message.channel.send("Incorrect date format, months must be less than 13, days less than 32, and so on")
        return

    deltaDays = int(abs(todayDate - dateJoined).days)
    try:
        myString = "\nAverage pieces per day: " + str(math.floor(linesCleared / deltaDays) * 2.5)
    except ZeroDivisionError:
        await message.channel.send("The date cannot be today")
        return

    pps = serverData.proprieties.referencepps
    try:
        pps = float(pps)
    except TypeError:
        await message.channel.send("No reference PPS value set")
        return

    number = calculateaverage(deltaDays, linesCleared, pps)
    tableList = "\nAt PPS -> Avg time player per day:"
    myString2 = "\n" + str(pps) + " PPS -> " + str(round(number, 3)) + "h"
    myString3 = "\n1.4 PPS -> " + str(round(number * (pps / 1.4), 3)) + "h"
    myString4 = "\n1.2 PPS -> " + str(round(number * (pps / 1.2), 3)) + "h"
    myString5 = "\n1 PPS -> " + str(round(number * pps, 3)) + "h"

    await message.channel.send('Average lines per day: ' + str(math.floor(linesCleared / deltaDays)) + myString +
                               tableList +
                               myString2 + myString3 +
                               myString4 + myString5)

    del linesClearedString, linesCleared, monthJoined, dayJoined, yearJoined, todayDate, dateJoined, myString
    del pps, number, tableList, myString2, myString3, myString4, myString5, serverData, message

    gc.collect()


async def royaleCalcAverageCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Calculates the average time played and lines cleared per day of an user

    Discord command:
    $royalecalcaverage (days passed since beginning of the season) (royale points)

    :param message: Message context
    :param serverData: Server data
    """
    try:
        day = int(str(message.content).split(' ')[1])
        pts = int(str(message.content).split(' ')[2])
        if day == 0:
            await message.channel.send("Day cannot be zero")
            return
    except (ValueError, IndexError):
        await message.channel.send(texts.royalecalcaverage_exception_one)
        return

    time_per_match = 15

    lines_per_match = 420
    try:
        pps = float(serverData.proprieties.referencepps)
    except ValueError:
        await message.channel.send("No reference PPS set")
        return

    # Ugly calculations...

    total_matches_played = pts / 10000  # 10k pts for each match won
    total_time_played = total_matches_played * time_per_match
    total_time_played /= 60
    total_time_played = math.floor(total_time_played * 1000) / 1000

    royale_time_per_day = total_time_played / day
    royale_lines_per_day_one = (((total_matches_played * time_per_match * 60) * pps) / 2.5) / day
    royale_lines_per_day_two = (total_matches_played * lines_per_match) / day
    royale_pieces_per_day_one = royale_lines_per_day_one * 2.5  # Each line has mathematically 2.5 pieces in it
    royale_pieces_per_day_two = royale_lines_per_day_two * 2.5

    royale_pieces_per_day_one = round(royale_pieces_per_day_one, 3)
    royale_pieces_per_day_two = round(royale_pieces_per_day_two, 3)
    royale_lines_per_day_one = round(royale_lines_per_day_one, 3)
    royale_lines_per_day_two = round(royale_lines_per_day_two, 3)
    royale_time_per_day = round(royale_time_per_day, 3)
    total_matches_played = round(total_matches_played, 3)

    # Decided to keep this text here due to the variables in it

    await message.channel.send(""
                               "[Royale] Lines per day: between " + str(royale_lines_per_day_one) + " - " + str(
        royale_lines_per_day_two) +
                               "\n[Royale] Pieces per day: between " + str(royale_pieces_per_day_one) + " - " + str(
        royale_pieces_per_day_two) +
                               "\n[Royale] Time played per day: " + str(royale_time_per_day) + "h"
                                                                                               "\n[Royale] Matches per day: " + str(
        total_matches_played / day) +
                               "\nCalculated under "
                               "these parameters (which vary): \n"
                               "PPS: " + str(pps) + "\n"
                                                    "Lines per royale match: " + str(lines_per_match) + "\n"
                                                                                                        "Time per match: " + str(
        time_per_match) + "min\n"
                          "")
    del day, pts, time_per_match, lines_per_match, pps, total_matches_played, total_time_played
    del royale_time_per_day, royale_lines_per_day_one, royale_lines_per_day_two
    del royale_pieces_per_day_one, royale_pieces_per_day_two, serverData, message

    gc.collect()

    return


async def diffCalculatorCMD(message: discord.Message):
    """
    Calculates the rate at which the player does special line clears and back to backs

    Discord command:
    $diffcalculator (tetrises) (T-spins) (back-to-backs) (lines cleared)

    :param message: Message context
    """
    texto = str(message.content)
    try:
        tetrises = int(texto.split(' ')[1])
        tspins = int(texto.split(' ')[2])
        btb = int(texto.split(' ')[3])
        lines = int(texto.split(' ')[4])
    except (ValueError, IndexError):
        await message.channel.send("Incorrect syntax, use: '$diffcalculator <tetris> <tspin> <b2b> <lines>'\n"
                                   "Ex: $diffcalculator 100 50 40 1500")
        return

    try:
        results = diffcalculator(tetrises, tspins, btb, lines)
    except ZeroDivisionError:
        await message.channel.send("The parameters you gave resulted in a division by zero")
        return

    specialRate = results[0]
    btbPerSpecial = results[1]
    btbPerTotal = results[2]

    specialRate = round(specialRate, 3)
    btbPerTotal = round(btbPerTotal, 3)
    btbPerSpecial = round(btbPerSpecial, 3)

    await message.channel.send("Special Line Clears rate: " + str(specialRate * 100) +
                               "%\nB2Bs per specials rate: " + str(btbPerSpecial * 100) +
                               "%\nB2Bs per total rate: " + str(btbPerTotal * 100) + '%')

    del texto, tetrises, tspins, btb, lines, results, specialRate, btbPerSpecial, btbPerTotal, message
    gc.collect()


async def compCalculatorCMD(message: discord.Message, serverData: classes.ServerData):
    """
    Comparative calculator command, compares the player's activity and technique score, calculated by a formula made
    by BlakeD38, to the reference data's activity and technique score.

    Discord command:
    $compcalculator (day)/(month)/(year) (quick play highscore) (marathon highscore) (lines) (tetrises) (all clears)
    (t-spins) (challenges completed) (login streak)

    :param message: Message context
    :param serverData: Server data
    """
    content = str(message.content)
    content = content.split(' ')

    try:
        day = int(content[1].split('/')[0])
        month = int(content[1].split('/')[1])
        year = int(content[1].split('/')[2])

        quickplay = int(content[2])
        marathon = int(content[3])
        lines = int(content[4])
        tetrises = int(content[5])
        allClears = int(content[6])
        tspins = int(content[7])
        challenges = int(content[8])
        streak = int(content[9])

    except (IndexError, ValueError):
        await message.channel.send("Invalid syntax, please check if all parameters are filled and are "
                                   "integers. Correct usage:\n"
                                   "$compcalculator <day>/<month>/<year> <quickplay hscore> <marathon hscore>"
                                   " <lines> <tetrises> <allclears> <tspins> <challenges> <streak>")
        return

    try:
        d = datetime.date(year, month, day)
    except ValueError:
        await message.channel.send("Invalid date")
        return

    results = compcalculator(serverData, classes.Parameters(
        year, month, day, quickplay, marathon, lines, tetrises, allClears, tspins, challenges, streak, 0
    ))

    await message.channel.send("Activity score compared to reference: " +
                               str(round(results[0], 3)) +
                               "\nTechnique score compared to reference: " +
                               str(round(results[1], 3)))

    del d, content, day, month, year, quickplay, marathon, lines, tetrises, allClears, tspins, challenges, streak
    del serverData, message
    gc.collect()


async def check(message, serverData):
    """
    Main check function

    Discord commands:
    $ppscalculator
    $calculateaverage
    $royalecalcaverage
    $diffcalculator
    $teamptscalculator
    $compcalculator

    :param message: Message context
    :param serverData: Server data
    """
    # Simple PPS calculation
    if message.content.startswith('$ppscalculator'):
        await ppsCalculatorCMD(message)

    # Amount played per day based on profile data
    if message.content.startswith('$calculateaverage'):
        await calculateAverageCMD(message, serverData)

    # Amount played per day based on royale data
    if message.content.startswith('$royalecalcaverage'):
        await royaleCalcAverageCMD(message, serverData)

    # Line clearance rate calculation
    if message.content.startswith('$diffcalculator'):
        await diffCalculatorCMD(message)

    # Technique and activity calculator (created by BlakeD38)
    if message.content.startswith('$compcalculator'):
        await compCalculatorCMD(message, serverData)
