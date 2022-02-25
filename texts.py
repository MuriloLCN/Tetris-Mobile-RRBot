# It was a better decision to put most long strings in a separate file to keep things clearer and less messy overall

tasks = "```The current team task system rotates between a set list of tasks, they go as follow (list made by K1DDz)\n\n" \
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
        "  Full Moon (season 14|2)\n"\
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
          "[14|2] Love Quest Season\n"\
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

h_1 = "```Tetris Mobile RRBot command list\n\n" \
      "> Timer for royale\n" \
      "$createtimer <time in minutes>\n" \
      "OR\n" \
      "$createtimer &<timezone> &<hour>:<minute>\n\n" \
      "> Information commands\n" \
      "$tasks | Task cycle\n" \
      "$bonus | Bonus system\n" \
      "$modes | All modes\n" \
      "$seasons | All seasons\n" \
      "$guides | Community guides\n" \
      "$publisher | Info about the game publishers\n" \
      "$fullguide | Complete help command\n\n" \
      "> Calculator commands\n" \
      "$ppscalculator <lines> | Calculate PPS (quick-play)\n\n" \
      "> [ADMIN] Parameter customization commands\n" \
      "$setrole <@role> | Role for the timers\n" \
      "$setnewlimit <new limit in minutes> | Time limit for timers\n\n" \
      "Most other commands can only be seen in verified servers, use '$requestverify' if not yet verified\n" \
      "Note: Messages sent on my DMs are forwarded to humans. Beep boop.\n" \
      "```" \

h_2 = "```Verified server commands (if you can see this, you have access)\n\n" \
      "> Rotation system\n" \
      "$rotation | Help for rotation\n" \
      "$enter | Join/leave EN queue\n" \
      "$leave | Join/leave LE queue \n" \
      "$freespot | Moves EN queue\n\n" \
      "> Tetris notification\n" \
      "$infotetris| Help for Tetris Notify\n" \
      "$savedtetris | Flag for ping\n" \
      "$tetristask | Ping flagged\n\n" \
      "> Bonus notification\n" \
      "$fullbonusping | Help for Bonus Notify\n" \
      "$dailiesdone | Flag for ping\n" \
      "$gotfullbonus | Ping flagged\n\n " \
      "> Calculator commands\n" \
      "$calculateaverage <total lines> <month>/<day>/<fullyear> | Simple calculator\n" \
      "$royalecalcaverage <day of the month> <royale points> | Royale calculator\n" \
      "$teamptscalculator <hours> <points> | Team calculator\n" \
      "$compcalculator <day>/<month>/<year> <qp hs> <mt hs> <lines> <tetrises> <allclears> <tspins> " \
      "<challenges> <streak> | Comparative calculator\n" \
      "$diffcalculator <tetrises> <tspins> <b2bs> <lines> | Rate calculator\n\n" \
      "> Daily reminder creation\n" \
      "$createdailyreminder <timezone> <hour>:<minute> | Create alarm\n" \
      "```"

h_3 = "```" \
      "> Admin commands\n" \
      "$setreferencepps <pps>\n" \
      "$printserverdata\n" \
      "$resetserverdata\n" \
      "$clearcache\n" \
      "$addoption &<:reaction:> &<@role/option text>\n" \
      "$addchanger <channelID>\n" \
      "$addvote <channelID>\n" \
      "$addpoint <name> <day>/<month>/<year> <qp hs> <mt hs> <lines> <tetrises> <allclears> <tspins> <b2bs>" \
      "$generategraphs" \
      "$setbotchannel <#channel>\n" \
      "$setreminderchannel <#channel>\n" \
      "$updatereferencevalues <day>/<month>/<year> <qp hs> <mt hs> <lines> <tetrises> <allclears> <tspins> <b2bs>" \
      " <challenges> <streak>\n" \
      "$forgetchangermessages\n" \
      "$appendchangerid <messageID>\n" \
      "$storepoint <pointName> <day>/<month>/<year> <qp hs> <mt hs> <lines> <tetrises> <allclears> <tspins> <b2bs>\n" \
      "$deletepoint <pointName>\n" \
      "$loadpoint <pointName>\n" \
      "$listpoints\n" \
      "$clearpoints\n" \
      "$printpoint <pointName>\n" \
      "$loadallpoints\n" \
      "```"
