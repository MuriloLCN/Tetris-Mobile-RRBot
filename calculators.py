import datetime
import math

import classes
import privatedata
import texts


# Raw calculation commands
def getDays(day, month, year):
    todayDate = datetime.date.today()
    dateJoined = datetime.date(year, month, day)
    return int(abs(todayDate - dateJoined).days)


def activityScore(lines, challenges, streak, days, ref):
    refdate = datetime.date.today() - ref.joindate
    return ((refdate.days/days) * (((lines / ref.lines) + 20 * (challenges / ref.challenges) + 50 * (streak /
                                                                                                     ref.streak))))/100


def techniqueScore(quickPlay, marathon, allClears, tspins, tetrises, ref):
    return (9 * (quickPlay / ref.quickplayhs) + 0.001 * (marathon / ref.marathonhs) + 3 * (allClears / ref.allclears) +
            (tspins/ref.tspins) + 0.1 * (tetrises/ref.tetrises)) / (9+0.001+3+1+0.1)


def calculatepps(lines):
    return round((lines * 2.5)/180, 3)  # PPS


def calculateaverage(deltadays, lines, pps):
    # Just in case someone needs an explanation
    # floor(linesCleared/deltaDays) -> lines per day
    # that * 2.5 -> pieces per day
    # that / PPS -> seconds per day (needed to place those pieces)
    # that / 60 / 60 -> converting to hours
    return (((math.floor(lines / deltadays) * 2.5) / pps) / 60) / 60  # Hours played per day


def diffcalculator(tetrises, tspins, btb, lines):
    rate = tetrises / (tetrises + tspins)
    return [
        1 - ((lines - (tetrises * 4) - (tspins * 2)) / lines),  # Special line clear rate
        btb / (tspins + tetrises),  # Back-to-backs per special line clears
        (btb * (2 + (2 * rate))) / lines  # Back-to-backs per total line clears
    ]


def compcalculator(serverData, parameters):
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


async def check(message, serverData):

    # Simple PPS calculation
    if message.content.startswith('$ppscalculator'):
        try:
            lines = int(str(message.content).split(' ')[1])
        except (ValueError, IndexError):
            await message.channel.send("Incorrect syntax, correct usage: '$ppscalculator <lines>'."
                                       " Example: '$ppscalculator 120'.")
            return

        pps = calculatepps(lines)

        await message.channel.send("Your PPS is around " + str(pps) + "PPS.")
        return

    if message.guild.id not in privatedata.blacklist:

        # Amount played per day based on profile data
        if message.content.startswith('$calculateaverage'):

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
                myString = "\nAverage pieces per day: " + str(math.floor(linesCleared/deltaDays) * 2.5)
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
            myString2 = "\n"+str(pps)+" PPS -> " + str(round(number, 3)) + "h"
            myString3 = "\n1.4 PPS -> " + str(round(number*(pps/1.4), 3)) + "h"
            myString4 = "\n1.2 PPS -> " + str(round(number*(pps/1.2), 3)) + "h"
            myString5 = "\n1 PPS -> " + str(round(number*pps, 3)) + "h"

            await message.channel.send('Average lines per day: ' + str(math.floor(linesCleared/deltaDays)) + myString +
                                       tableList +
                                       myString2 + myString3 +
                                       myString4 + myString5)

            return

        # Amount played per day based on royale data
        if message.content.startswith('$royalecalcaverage'):

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
            total_time_played = math.floor(total_time_played*1000)/1000

            royale_time_per_day = total_time_played / day
            royale_lines_per_day_one = (((total_matches_played * time_per_match * 60) * pps)/2.5)/day
            royale_lines_per_day_two = (total_matches_played * lines_per_match)/day
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
                                       "[Royale] Lines per day: between " + str(royale_lines_per_day_one) + " - " + str(royale_lines_per_day_two) +
                                       "\n[Royale] Pieces per day: between " + str(royale_pieces_per_day_one) + " - " + str(royale_pieces_per_day_two) +
                                       "\n[Royale] Time played per day: " + str(royale_time_per_day) + "h"
                                       "\n[Royale] Matches per day: " + str(total_matches_played/day) +
                                       "\nCalculated under "
                                       "these parameters (which vary): \n"
                                       "PPS: " + str(pps) + "\n"
                                       "Lines per royale match: " + str(lines_per_match) + "\n"
                                       "Time per match: " + str(time_per_match) + "min\n"
                                       "")

            return

        # Line clearance rate calculation
        if message.content.startswith('$diffcalculator'):
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

            results = diffcalculator(tetrises, tspins, btb, lines)

            specialRate = results[0]
            btbPerSpecial = results[1]
            btbPerTotal = results[2]

            specialRate = round(specialRate, 3)
            btbPerTotal = round(btbPerTotal, 3)
            btbPerSpecial = round(btbPerSpecial, 3)

            await message.channel.send("Special Line Clears rate: " + str(specialRate) +
                                       "\nB2Bs per specials rate: " + str(btbPerSpecial) +
                                       "\nB2Bs per total rate: " + str(btbPerTotal))
            return

        # Team points simple calculation (not very useful imo, added per request)
        if message.content.startswith('$teamptscalculator'):
            try:
                hours = int(str(message.content).split(' ')[1])
                pts = int(str(message.content).split(' ')[2])
                avg = round(pts / hours, 3)
            except (IndexError, ValueError):
                await message.channel.send("Incorrect syntax, use: '$teamptscalculator <hours> <points>'\n"
                                           "Ex: $teamptscalculator 47 25200")
                return
            await message.channel.send("Average points per hour: " + str(avg))
            return

        # Technique and activity calculator (created by BlakeD38)
        if message.content.startswith('$compcalculator'):

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

            results = compcalculator(serverData, classes.Parameters(
                year, month, day, quickplay, marathon, lines, tetrises, allClears, tspins, challenges, streak, 0
            ))

            await message.channel.send("Activity score compared to reference: " +
                                       str(round(results[0], 3)) +
                                       "\nTechnique score compared to reference: " +
                                       str(round(results[1], 3)))
            return
