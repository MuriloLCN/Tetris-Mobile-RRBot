import datetime
import math

import discord
import matplotlib.pyplot as plt
import numpy as np

import calculators
import classes
import datahandling


def getscale(value):
    if value < 0:
        value = -1 * value

    scl = 1

    while value > 1:
        value = value/10
        scl += 1

    return scl


async def check(message, serverData, data):

    # Adds a point to be used in the graphs. Has lots of parameters.
    if message.content.startswith('$addpoint'):
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
        point = {username: classes.Parameters(
            year, month, day, quickplayhs, marathonhs, lines, tetrises, allclears, tspins, challenges, streak, btb
        )}

        serverData.cached.datapoints.update(point)

        await message.add_reaction('\U0001F44D')
        datahandling.writeserverdata(message.guild.id, serverData, data)

    # Loads a stored point to be used in the graphs
    if message.content.startswith('$loadpoint'):
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
            await message.channel.send("Point with named {} not found, to see list of stored points use "
                                       "$listpoints".format(name))
            return

        serverData.cached.datapoints.update(pointentry)
        await message.add_reaction('\U0001F44D')
        datahandling.writeserverdata(message.guild.id, serverData, data)

    # Loads all stored points to be used in the graphs
    if message.content.startswith('$loadallpoints'):

        for key in serverData.storedpoints.keys():
            pointentry = {key: serverData.storedpoints[key]}
            serverData.cached.datapoints.update(pointentry)

        await message.add_reaction('\U0001F44D')
        await message.channel.send("Loaded {} points(s)".format(str(len(serverData.storedpoints))))
        datahandling.writeserverdata(message.guild.id, serverData, data)

    # Generates graphs with the points loaded

    # A -> Activity x Technique graph
    # B -> All purpose radar graph
    # C -> Special rate x b2b rate graph
    # D -> Time per day x account life graph
    if message.content.startswith('$generategraphs'):
        # Get the parameter string
        try:
            stringy = str(message.content).split(' ')[1].upper()
        except (IndexError, Exception):
            await message.channel.send("Please pass a parameter (A, B, C, AC, ACD, etc.)")
            return

        # Sorry for the variable naming, it gets repetitive
        if len(serverData.cached.datapoints) <= 1:
            await message.channel.send("You need at least two data points to generate a graph")
            return

        # Had to add a simple picking out system. Graphs can take a toll in resource usage.
        remainingChecks = ['A', 'B', 'C', 'D']

        parameters = []

        accountLife = []    # datetime.timedelta

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

            #avglinesday.append(calculators.calculateaverage((datetime.date.today() - entry.joindate).days, entry.lines,
            #                                                serverData.proprieties.referencepps) * 60)
            avglinesday.append(math.floor(entry.lines / (datetime.date.today() - entry.joindate).days))

            techscore.append(calculators.techniqueScore(entry.quickplayhs, entry.marathonhs, entry.allclears,
                                                        entry.tspins, entry.tetrises,
                                                        serverData.proprieties.referenceparameters))

            specialrate.append(calculators.diffcalculator(entry.tetrises, entry.tspins, entry.backtoback, entry.lines)[0])

        plt.style.use('seaborn-whitegrid')

        # Activity score x talent score
        if 'A' in stringy:
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

            remainingChecks.remove('A')
            lastOne = True
            for r in remainingChecks:
                if r in stringy:
                    lastOne = False
                    break

            if lastOne:
                serverData.cached.datapoints.clear()
                datahandling.writeserverdata(message.guild.id, serverData, data)
                return

        # Complete data graph
        # Huge thanks to BlakeD38! This radar graph would not have been possible without him
        if 'B' in stringy:
            try:
                # The number needed to divide the data points as to make the highest values between 0 and 1

                # Note: Most parameters are no longer used in the graph as per request, though they might be used in the future
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

            referencePlayer = [1, 1, 1, 1, 1]  # This is just here to get the lengh, reference data is no longer used on the graph
            referencePlayer = [*referencePlayer, referencePlayer[0]]

            label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(referencePlayer))

            plt.figure(figsize=(8, 8))
            plt.subplot(polar=True)
            # plt.plot(label_loc, referencePlayer, label='Reference Player')
            plt.title('All purpose visualizer', size=20, y=1.05)

            for i in range(len(usernames)):
                # Everything is divided by scale so that it all goes between 0 and 1
                # playerdata = [qphs[i]/qpscale, mths[i]/mtscale, linec[i]/linescale, tetrises[i]/tetrscale,
                #              allc[i]/allcscale, tsp[i]/tspscale, chl[i]/chlscale, strk[i]/strkscale, btb[i]/btbscale]
                playerdata = [avglinesday[i]/avglinesdayscale, techscore[i]/techscorescale, qphs[i]/qpscale,
                              linec[i]/linescale, specialrate[i]/specialratescale]
                playerdata = [*playerdata, playerdata[0]]
                plt.plot(label_loc, playerdata, label=usernames[i])

            lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
            plt.legend()
            plt.savefig('temp.png')

            await message.channel.send(file=discord.File('temp.png'))
            plt.cla()
            plt.clf()

            remainingChecks.remove('B')
            lastOne = True
            for r in remainingChecks:
                if r in stringy:
                    lastOne = False
                    break

            if lastOne:
                serverData.cached.datapoints.clear()
                datahandling.writeserverdata(message.guild.id, serverData, data)
                return

        # Special rate x b2b per special
        if 'C' in stringy:
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

            remainingChecks.remove('C')
            lastOne = True
            for r in remainingChecks:
                if r in stringy:
                    lastOne = False
                    break

            if lastOne:
                serverData.cached.datapoints.clear()
                datahandling.writeserverdata(message.guild.id, serverData, data)
                return

        # time played per day x account lifespan
        if 'D' in stringy:
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

            remainingChecks.remove('D')
            lastOne = True
            for r in remainingChecks:
                if r in stringy:
                    lastOne = False
                    break

            if lastOne:
                serverData.cached.datapoints.clear()
                datahandling.writeserverdata(message.guild.id, serverData, data)
                return
