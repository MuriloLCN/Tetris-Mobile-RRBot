# It was a better decision to put most long strings in a separate file to keep things clearer and less messy overall

tasks = "```The current team task system rotates between a set list of tasks, as follow (list made by K1DDz):\n\n" \
       "Score |500.000 * x| points in Quick Play\n"\
       "Knockout |250 * x| players in Royale\n"\
       "Clear |1250 * x| lines in Quick Play\n"\
       "Send |1000 * x| garbage lines in Royale\n"\
       "Clear |750 * x| lines in royale\n"\
       "Perform |400 * x| Tetris line clears\n"\
       "And then it goes back to the beginning\n"\
       "> [x = log2(Points given by the task/100) + 1]```"

bonus = "```The team bonus is the bonus that multiplies each reward that the team receives while it's active\n"\
        "It's the little yellow flag on the task, and it can only go up to 400% for now\n"\
        "The bonus achieved depends on how many people completed their daily goals for that day, it doubles for every five people done\n"\
        "The bonus can be calculated using this formula (there is no 800% bonus)\n"\
        "Bonus = 25 * (2 ^ (floor(number of players done/5))).\n"\
        "> This formula only works for 30>number of players>=5, because there is no bonus for less than 5 nor 30```"

modes = "```Here's a list of all the gamemodes that are/were in the game\n\n"\
        "Marathon | Our current marathon\n"\
        "Quick Play | 3 minutes race\n"\
        "Royale | Our current royale\n"\
        "Old Royale | Old royale system (no PvP, win by endurance/patience)\n"\
        "Primetime | Gameshow with cash prizes\n"\
        "Modes in which level increases every two line clears: \n" \
        "  Easy as a pie (season 11)\n" \
        "  Ninja Trials (season 12)\n" \
        "  Double Scoop (season 12)\n" \
        "  Let it snow (season 12)\n" \
        "  Fire breath (season 13|1)\n" \
        "  Hugging (season 13|1)\n" \
        "  Chocolate Bliss (season 13|1)\n" \
        "  Perfect Slice (season 14|2)\n" \
        "  Ice Walk (season 14|2)\n" \
        "Modes in which the pieces are all random:\n" \
        "  Hallow's eve (season 10)\n" \
        "  Folding Madness (season 11)\n" \
        "  Tetricassen (season 11)\n" \
        "  Lotta Llama (season 12)\n" \
        "  Wacky Wobbler (season 13|1)\n" \
        "  Year of the tiger (season 14|2)\n" \
        "  Full Moon (season 14|2)\n" \
        "  Wild (season 15|3)\n"\
        "```"

seasons = "```Here's a list of recorded seasons for now\n\n"\
          "[1] Christmas Season (even though it was in January...)\n"\
          "[2] Valentine Season\n"\
          "[3] Ancient Egypt Season\n"\
          "[4] Easter Season\n"\
          "[5] Under the sea Season\n"\
          "[6] Space Season\n"\
          "[7] Japan Season\n"\
          "[8] Pet Season\n"\
          "[9] Dino season\n"\
          "[10] Halloween Season\n"\
          "[11] Adventure Season\n" \
          "[12] Winter Season\n" \
          "[13|1] Monters Season\n" \
          "[14|2] Love Quest Season\n" \
          "[15|3] Space Fantasy Season\n"\
          "```"

guides = ""\
         "Here are a few guides on the most common topics\n\n"\
         "> Tetrising: https://four.lol/stacking/tetris\n"\
         "> T-Spins: https://harddrop.com/wiki/T-Spin_Guide\n"\
         "> All Clears: https://four.lol/perfect-clears/opener\n"\
         "> Openers: https://four.lol/openers/practical-openers\n"\
         "> 4 Wide: https://four.lol/stacking/4-wide\n"\
         "> Supershocky's guide on ST Stacking: https://docs.google.com/document/d/1oqu0zqANYqorEf3tRpWuoMQ8FIJPWCi13uJSjgjrvbA/edit?usp=sharing\n\n"\
         "More guides will be added in the future\n" \
         ""

rotation = "```Here's a quick rundown on the rotation system\n\n"\
           "If you are in the team but want to rotate out, do '$leave'\n"\
           "Then, you'll enter the queue to leave once someone wants to join\n"\
           "If you change your mind, just do '$leave' again to get out of queue\n\n"\
           "Same thing goes for people that are willing to rotate in\n"\
           "If you are not in the team but can rotate in if needed, do '$enter'\n"\
           "Then, you'll enter the queue to enter once someone leaves\n"\
           "Like before, to get out of queue just run the command again\n\n"\
           "Once, in the same DISCORD SERVER (it has to be the team's discord),\n"\
           "One player wants to leave and one to enter, there'll be a match and both will be notified\n\n"\
           "Hope this clears things up a bit```"

infotetris = "```"\
             "Here's a quick guide to the Tetris Task notification system\n\n"\
             "> If you have saved a marathon game with tetrises in it for when the task comes up\n"\
             "> Just type '$savedtetris' in the chat, and your name will be added to a list\n\n"\
             "> Once the Tetris task is live, simply type '$tetristask' on the chat, and "\
             "everyone in that list will be pinged and removed from it. That's your cue to "\
             "put in those tetrises\n\n"\
             "```"

fullbonusping = "```"\
                "Bonus pinging system\n\n"\
                "The bonus pinging system works in a way that "\
                "if you want to be warned whenever the team reaches "\
                "full bonus (400%), just type '$dailiesdone'.\n"\
                "If you want to signal that the team has reached that bonus, "\
                "just type '$gotfullbonus'.\n"\
                "```"

calculateaverage_exception_one = "Incorrect syntax, correct usage: "\
                                 "'$calculateaverage numberoflines month/day/year\n"\
                                 "Please check if you used "\
                                 "'/' to separate the date\n"\
                                 "Also keep in mind the (bad) order of the date: Month / Day / Year"\
                                 " and use full year (2021 instead of 21)"

royalecalcaverage_exception_one = "Incorrect command, correct usage: "\
                                  "'royalecalcaverage <dayofthemonth> <points>'.\n"\
                                  "Make sure that the parameters"\
                                  " are integers. Also, day of the month is how long the"\
                                  " current season has been going for, since they start on day 1"

# Timer system + matchmaking
menu_help_one = "```(help page 1)\n" \
                "Timer commands\n" \
                "[Public]\n" \
                "> $createtimer <time in minutes>\n" \
                "or\n" \
                "> $createtimer &<timezone> &<hour>:<minute>\n" \
                "Creates a timer to a set amount of minutes from the current time or to a set time.\n" \
                "Pings the designed role once the timer runs out\n\n" \
                "Matchmaking commands [WIP]\n" \
                "> $matchmaking\n" \
                "Joins the matchmaking lobby. Once lobby is full every plyer is pinged to join royale lobby.\n" \
                "```" \
                ""

menu_help_two = "```(help page 2)\n" \
                "Information commands\n" \
                "[Public]\n" \
                "> $tasks\n" \
                "Lists the task cycle\n" \
                "> $bonus\n" \
                "Info for the team bonus mechanic\n" \
                "> $guides\n" \
                "List of some community-made guides for Tetris\n" \
                "> $fullguide\n" \
                "Full in-depth guide for my commands\n" \
                "[Verified only]\n" \
                "> $rotation\n" \
                "Help command for rotation system\n" \
                "> $infotetris\n" \
                "Help command for Tetris task pinging system\n" \
                "> $fullbonusping\n" \
                "Help command for Full bonus pinging system\n" \
                "```"

menu_help_three = "```(help page 3)\n" \
                  "Calculator commands\n" \
                  "[Public]\n" \
                  "> $ppscalculator <lines>" \
                  "Calculates PPS (pieces per second) based on lines cleared in a single Quick Play game\n" \
                  "[Verified only]\n" \
                  "> $calculateaverage <total lines> <month>/<day>/<fullyear>\n" \
                  "Calculates player averages based on profile data.\n" \
                  "> $royalecalcaverage <day of the month> <royale points>\n" \
                  "Calculates player averages based on royale season's data.\n" \
                  "> $compcalculator <day>/<month>/<year> <qp hs> <mt hs> <lines> <tetrises> <allclears> <tspins> " \
                  "<challenges> <streak>\n" \
                  "Calculates ACxTH scores based on server-defined reference values.\n" \
                  "> $diffcalculator <tetrises> <tspins> <b2bs> <lines>\n" \
                  "Calculates SP/Total, B2B/Total and B2B/SP clearance rates.\n" \
                  "```" \
                  ""

menu_help_four = "```(help page 4)\n" \
                 "Rotation system\n" \
                 "[Verified only]\n" \
                 "> $enter\n" \
                 "Joins/exits the ENTER TEAM queue.\n" \
                 "> $leave\n" \
                 "Joins/exits the LEAVE TEAM queue.\n" \
                 "> $freespot\n" \
                 "Notifies the next person in the ENTER TEAM queue that there is a spot.\n" \
                 "> $addvisualizer\n" \
                 "Adds a visual list of the queue to the channel that gets updated with all names.\n" \
                 "```"

meun_help_five = "```(help page 5)\n" \
                 "Notification systems\n" \
                 "[Verified only]\n" \
                 "> $savedtetris\n" \
                 "Signals the bot you have stored Tetris line clears.\n" \
                 "> $tetristask\n" \
                 "Pings every player that has Tetris line clears stored.\n" \
                 "> $dailiesdone\n" \
                 "Signals the bot that you have done your daily tasks. Silences daily reminder, if you have one.\n" \
                 "> $gotfullbonus\n" \
                 "Pings every player that has done their daily tasks.\n" \
                 "```" \
                 ""

menu_help_six = "```(help page 6)\n" \
                "Daily reminder system\n" \
                "> $createdailyreminder <timezone> <hours>:<minutes>\n" \
                "Creates a recurring daily alarm to remind the daily tasks. Requires AlarmBot integration.\n" \
                "> $reminder <hour>:<minute> <timezone> <#channel>\n" \
                "Creates a recurring daily alarm to remind you to do dailty tasks. NOTE: You can use '123' for the " \
                "channel to receive it in your DMs. Does not require any external bots to function. [New - in beta]\n" \
                "```" \
                ""

menu_help_seven = "```(help page 7)\n" \
                  "Role changer/vote system\n" \
                  "[Admin only]\n" \
                  ">> Important note: Custom emojis won't work <<\n" \
                  "> $addoption &<:reaction:> &<@role/option text>\n" \
                  "Stores an option for a text/role to be paired with a reaction.\n" \
                  "> $addchanger <channelID>\n" \
                  "Uses all stored options to make a message that users can use to change their roles.\n" \
                  "> $addvote <channelID>\n" \
                  "Uses all stored options to make a message in which users can vote.\n" \
                  "```" \
                  ""

menu_help_eight = "```(help page 8)\n" \
                  "Graph making system\n" \
                  "[Verified only]\n" \
                  "[Admin only]\n" \
                  "> $addpoint <name> <day>/<month>/<year> <quickplay highscore> <marathon highscore> <lines>" \
                  " <tetrises> <allclears> <tspins> <challenges> <login streak> <back-to-backs>\n" \
                  "Loads a one-time-use point for graph making.\n" \
                  "> $storepoint <name> <day>/<month>/<year> <quickplay highscore> <marathon highscore> <lines>" \
                  " <tetrises> <allclears> <tspins> <challenges> <login streak> <back-to-backs>\n" \
                  "Stores a multi-use point that can be loaded for graph making at any time.\n" \
                  "> $deletepoint <pointName>\n" \
                  "Deletes a specific stored point.\n" \
                  "> $loadpoint <pointName>\n" \
                  "Loads a stored point to be used in graph making.\n" \
                  "> $listpoints\n" \
                  "Lists all stored points.\n" \
                  "> $clearpoints\n" \
                  "Deletes all stored points\n" \
                  "> $printpoint <pointName>\n" \
                  "Prints data stored under a given point.\n" \
                  "> $loadallpoints\n" \
                  "Loads all points to be used in graph making.\n" \
                  "> $generategraphs <any subset of 'ABCD'>\n" \
                  "Generates the desired graphs. It can be 'A', 'AD', 'CBD', 'ABDC', etc." \
                  "```" \
                  ""

menu_help_nine = "```(help page 9)\n" \
                 "Administrator commands\n" \
                  "[Public]\n" \
                  "> $setrole <@role>\n" \
                  "Sets the role to be pinged when timers run out.\n" \
                  "> $setnewlimit <limit>\n" \
                  "Changes the time limit (minutes) of how long a timer can be.\n" \
                  "[Verified only]\n" \
                  "> $setreferencepps <pps>\n" \
                  "Changes the reference value for PPS used in calculations.\n" \
                  "> $printserverdata\n" \
                  "Prints server's data.\n" \
                  "> $resetserverdata\n" \
                  "Resets server's data to the default state.\n" \
                  "> $clearcache\n" \
                  "Clears server's cached info.\n" \
                  "> $setbotchannel <#channel>\n" \
                  "Sets the channel in which the Alarm System integration will occur. Gets floody.\n" \
                  "> $setreminderchannel <#channel>\n" \
                  "Sets the channel in which daily reminders will be sent in. Gets floody.\n" \
                  "> $updatereferencevalues <day>/<month>/<year> <quickplay highscore> <marathon highscore>" \
                  " <lines> <tetrises> <allclears> <tspins> <challenges> <login streak> <back-to-backs>\n" \
                  "Changes the reference values used in calculations for the server.\n" \
                  "> $forgetchangermessages\n" \
                  "Removes changer messages from memory so they no longer work.\n" \
                  "> $appendchangerid <messageID>\n" \
                  "Stores a message ID into the changer messages memory so it behaves as one.\n" \
                  "```" \
                  ""

menu_help_header = "```\nTetris Mobile RRBot Help command" \
                   "\n\nUse the reactions to navigate between pages" \
                   "\n\n" \
                   "    ────────────────────┐\n" \
                   "   /                   /│      Pages summary:\n" \
                   "  /                   / │      Page 1: Timer commands\n" \
                   " ┌───────────────────┐  │      Page 2: Information commands\n" \
                   " │                   │  │      Page 3: Calculator commands\n" \
                   " │      TETRIS       │ /       Page 4: Rotation commands\n" \
                   " │                   │/        Page 5: Notification commands\n" \
                   " └──────┐     ┌──┬───┘         Page 6: Reminder commands\n" \
                   "        │     │  │             Page 7: Changer & votes commands\n" \
                   "        │     │  │             Page 8: Graphing commands\n" \
                   "        │     │ /              Page 9: Admin and management commands\n" \
                   "        │     │/         \n" \
                   "        └─────┘          \n" \
                   "```"

# TODO: Make $updatereferencevalues take in as an optional parameter a stored point
