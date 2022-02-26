# Tetris Mobile Royale Reminder Bot use guide

You can add it to your server in this link https://discord.com/api/oauth2/authorize?client_id=867241160062009360&permissions=8&scope=bot

In this guide, I'll go over the basics of the mechanics implemented so far with RRB. 
The most important ones you need to know about are below.

## Basic and Complete Help Commands ($? and $fullguide)

'$?': shows a list of available commands to the user and a summarized description of them
as well

'$fullguide': links to this page for a complete description



## Information Commands

($tasks; $bonus; $modes; $seasons; $guides; $publisher; $rotation; $infotetris; $fullbonusping)

These commands show a brief description of the systems they represent, a more in-depth view is in here.
    
    

## Royale Timer System

This is the main feature and what brought this project to life.

This system's goal is to make people across the world be able to join the same royale match as their friends. As Tetris Mobile currently does not have a way for parties to join together in any meaningful way.

The way it works is:
> You create a timer

> You get ready to join the match

> Once you receive a notification from the bot, join the matchmaking

> You and your friends/teammates will likely join the same lobby

> Have fun!

###    Commands:

```$createtimer <minutes from now>```
OR
```$createtimer &<timezone in relation to GMT> &<time to enter>```

Both will create a timer with the desired lengths, and once that timer runs out, a desired role will be pinged.

**Examples:**

```$createtimer 25```
  Creates a timer to 25 minutes from now

```$createtimer &-3 &10:25```
  Creates a timer to 10:25 in GMT-3 time (13:25 in GMT)

```$createtimer &2 &17:25```
  Creates a timer to 17:25 in GMT+2 time (15:25 in GMT)
  
(Note: Use &0 for GMT timezone)

Once a timer runs out, the following message will be sent:

```"<@desiredRole>, connect now!"```

The desired role can be changed by admins with this command:

```$setrole @desiredRole```

This will make that role be pinged when timers run out

Make sure to press TAB to select the role you want in the menu that shows up to correctly mention it

**Examples:**

```$setrole @here```

```$setrole @group1```

...

If you are creating a timer with a long time span, you may run into an error saying that that timer exceeds
the set limit for that server.

Each server has their own time limit, which is set to 15 minutes by default.

Admins can change the time limit to something they choose, this limit is set in place to avoid spam and similar
things. Use carefully the time limit.

The command to change is

```$setnewlimit <time in minutes>```

**Examples:**

```$setnewlimit 7```

```$setnewlimit 30```

```$setnewlimit 180```

...

        
        

## Calculator mechanics

These mechanics are in place to help players to more easy calculate analytical information with the little data
provided in the game.

The first one is the Pieces Per Second (PPS) calculator. It uses data from a Quick Play Match (3 minutes long).

```$ppscalculator <number of lines at the end of a quick play game>```

**Examples:**

```$ppscalculator 100```
    -> 1.38 PPS

```$ppscalculator 120```
    -> 1.66 PPS

```$ppscalculator 80```
    -> 1.11 PPS

Note that the real result may vary, as the calculation assumes that you played uniformely across the match and that
you finished the game in a perfect clear. Real results may be lower that the ones showed.

The second one is the Average Player Data calculator, it shows data from a player based on their join date and
total lines cleared.

```$calculateaverage <total lines cleared> <month joined>/<day joined>/<year joined>```

**Examples:** (They were run on November 22nd, 2021. The results vary on the current day when the command is run)

Note: As added in v9, the PPS rate used for the calculations is no longer 1.66 by default and instead use the server-defined value.

```$calculateaverage 150000 2/14/2021```
  
-> Average lines per day: 533
  
-> Average pieces per day: 1332.5
  
-> Average time played per day (expected at a rate of 1.66 PPS): 0.222h


```$calculateaverage 25000 7/27/2021```
  
-> Average lines per day: 211
  
-> Average pieces per day: 527.5
  
-> Average time played per day (expected at a rate of 1.66 PPS): 0.088h


```$calculateaverage 400000 3/3/2020```
  
-> Average lines per day: 635
  
-> Average pieces per day: 1587.5
  
-> Average time played per day (expected at a rate of 1.66 PPS): 0.265h

Keep in mind that the statistics are all based on averages, and that older players that did not play as much back
then will have lower stats compared to newer players, and the time played per day only counts in-game time:
menus, ads, chats and alike do not count towards this indicator.

Take these numbers with a pinch of salt, as they represent fluid indicators, not complete criteria.

The third calculator mechanic the almost the same as the one above, but only based on royale data.

```$royalecalcaverage <day of the month/competition/season> <number of points>```

**Examples:**

```$royalecalcaverage 8 350000```
  
-> [Royale] Lines per day: between 2614.5 - 1837.5
  
-> [Royale] Pieces per day: between 6536.25 - 4593.75
  
-> [Royale] Time played per day: 1.09h
  
-> [Royale] Matches per day: 4.375

```$royalecalcaverage 13 75000```
  
-> [Royale] Lines per day: between 344.76 - 242.3
  
-> [Royale] Pieces per day: between 861.92 - 605.76
  
-> [Royale] Time played per day: 0.14h
  
-> [Royale] Matches per day: 0.576

```$royalecalcaverage 26 2500000```
  
-> [Royale] Lines per day: between 5746.15 - 4038.46
  
-> [Royale] Pieces per day: between 14365.38 - 10096.15
  
-> [Royale] Time played per day: 2.4h
  
-> [Royale] Matches per day: 9.615

A disclaimer for where the data comes from and what it covers is also shown at the end of the command.
It also shows the parameters in which the calculator was run in, which are just somewhat of an average
and change a lot from player to player in reality.

If you try to match the parameters, they won't add up, but that's on purpose to get a range of values to show
instead of a single value, since there's no absolute parameter. As you can see in the 'lines per day' and 'pieces
per day' info. The others are averages.

Note:

The day of the month is actually how long the current season has been going for, which coincides with
the day of the month as they currently start on day 1 and end at the end of the month.

The fourth calculator is the simplest one, used for calculating average team points per hour

```$teamptscalculator <hours> <points>```

It simply returns the points per hour average, added just to make things easier.

**Examples**

```$teamptscalculator 2 100``` -> 50 pts per hour

The next calculator is the Comparative Calculator

Made by BlakeD38 on Discord, this calculator compares data from a player to that of a default dataset
defined on that server.

```$compcalculator <day>/<month>/<year> <qp hs> <mt hs> <lines> <tetrises> <allclears> <tspins> <challenges> <streak>```

It has a lot of parameters and takes a lot into account for the comparison.

In order for the command to work, the server needs to have defined the parameters to be compared with. That can
be done with

```$updatereferencevalues <day>/<month>/<year> <qp hs> <mt hs> <lines> <tetrises> <allclears> <tspins> <challenges> <streak>```

Note: For servers that added the bot after this has been implemented, a default data has been passed in, but for
those servers that already used the bot before this update, the command will not work until those parameters are defined.
The default parameters currently are:
```15/6/2021 100000 1000000 75000 10000 50 750 1000 100```.
Also note that Activity Score is heavily influenced by login streak, if you want to remove this weight, simply set the streak
for the default parameters to 1 and also pass 1 for the calculations.

**Examples (with default data as reference)**

```$compcalculator 23/3/2020 367141 4021293 425545 20469 334 24428 1048 13```

-> Activity score compared to reference: 0.251

-> Technique score compared to reference: 4.545

```$compcalculator 9/5/2021 51420 388493 62504 6427 1 104 684 1```

-> Activity score compared to reference: 0.005

-> Technique score compared to reference: 0.396

The final calculator is the Special Rate Calculator, which calculates how a player uses Tetrises and TSpins compared
agains just improvising with other types of line clears.

```$diffcalculator <tetrises> <tspins> <b2bs> <lines>```

**Examples**

```$diffcalculator 3375 3 272 24693```

Special Line Clears rate: 0.547

B2Bs per specials rate: 0.081

B2Bs per total rate: 0.044

```$diffcalculator 20469 24428 25187 425545```

Special Line Clears rate: 0.307

B2Bs per specials rate: 0.561

B2Bs per total rate: 0.172

```$diffcalculator 30360 75445 41912 1079612```

Special Line Clears rate: 0.252

B2Bs per specials rate: 0.396

B2Bs per total rate: 0.1

## Rotation Mechanic

This is by far one of the most useful mechanics in this bot.

It is designed to help teams where there may be more than 30 players to rotate in and out more
swiftly by matching players with similar interests.

The way this works is:
If a player wants to leave/enter, they do the command ```$leave```/```$enter```
If after doing that command there's someone waiting to do the opposite action (enter/leave),
they will be matched and pinged. They can rotate with each other.
If after doing that command there's no one waiting to do the opposite action, they will enter
a queue for that action, and when someone does the opposite action they will be matched.

Examples scenarios:

Player A wants to leave and does ```$leave``` |
Player B was waiting to enter and had already done ```$enter``` |
Players A and B will be matched and will rotate with each other
  
  

Player C wants to enter and does ```$enter``` |
There's no one wanting to leave yet so player C needs to wait for someone to rotate with |
Player D wants to leave now and does ```$leave``` |
Players C and D can rotate now.
  
  

Player E wants to leave and does ```$leave``` |
Player E decided to no longer leave |
All they have to do is run the command ```$leave``` again to leave the rotation queue

**Commands:**

```$enter```
AND
```$leave```

Both commands will put your name in a queue for that action, if there are people at both queues they will be
matched for rotation.
    
```$freespot```
    
This command will ping the next person in the entry queue if there are users waiting to join.

This system is simple to use and rather useful for team management.
    

    
    

## Pinging Mechanics

There are two pinging mechanics, one for people with saved tetrises and one for people that have completed their
daily tasks and are waiting for a better multiplier to complete tasks (usually 400%)

The way they work is the player runs a command and their name will be added to a list.
Once someone runs the pinging command, everyone in that list will be pinged.

The first one:

```$savedtetris```
AND
```$tetristask```

If a player runs $savedtetris because they have a marathon game saved where they have a lot of tetrises and are
waiting for the 'Perform X Tetris Line Clears' task, their name will be saved.

Once a player sees that that task came, they just run ```$tetristask```


The second one:

```$dailiesdone```
AND
```$gotfullbonus```

It's very similar to the first one, I think there's not much need for a detailed explanation

    
    

## Daily Tasks Reminder Mechanic

This is the most convoluted mechanic as it requires two dedicated channels (optional, but recommended) and the
addition of AlarmBot to your server (https://top.gg/bot/754350217876340816).

This mechanic sends a message to every person with an alarm every day at the time of their choice in their timezone.

Important: If the player types ```$dailiesdone``` their alarm for that day will be silenced and they won't be pinged.

***Setup and maintenance guide***

**Step 1:**
Add AlarmBot to your server

**Step 2:**
Set up two dedicated channels for the mechanic:
  One where people will receive their daily reminders
  and one private for the maintenance of alarms

**Step 3:**
Make sure both bots have access to both channels, and that the maintenance one is private (it may get a bit
floody in there with enough people)

**Step 4:**
Maintain.

The only limitation of this mechanic is that, while RRB can listen to AlarmBot's messages and commands,
the other way around is not true, due to the nature of most Discord bots, so once someone tries to create or delete an
alarm, you or whoever mantains that channel has to copy the command sent by RRB and send it again on the same
chat for AlarmBot to create the alarm.

Don't fret, because there are only so many alarms that can be created, and for a Tetris team this is not much
work, just copy and paste the commands sporadically. The rest will work automatically.

As added in v7, the messages that need to be copied and pasted are now marked with a ping preceding the actual message, so
it's easier to see.

**Commands:**

```$setbotchannel #channel```

Sets the maintenance channel [REQUIRED]


```$setreminderchannel #channel```

Sets a channel dedicated for the reminders to be sent to the players [REQUIRED]


```$pingalarm <uID>```

Don't worry about this one, this is what AlarmBot sends to RRB in order for the mentioning to happen


```$createdailyreminder <timezone> <hour>:<minute>```

Sets up an alarm for that hour and minute every day on that timezone

**Examples:**

```$createdailyreminder -3 12:45```

```$createdailyreminder 0 17:36```

```$createdailyreminder 3 9:00```

## Vote/Role changing by reaction mechanic

This is a mechanic made for servers to easily add votes or messages in which a user can react to receive a desired role.

You first need to load the options into the cache with

```$addoption &<:reaction:> &<@role/option text>```

This will pair a reaction with a role or a text.
Keep in mind that texts will have their spaces removed, so if you want to write a sentence, use underscores (_)

Then, when all desired options are loaded, just do

```$addchanger <channelID>```

If you want to create a message in which users can switch roles, or do

```$addvote <channelID>```

If you simply want to use the message for voting.

**Examples**

To make a role changing message with three roles

```
>$addoption &:thinking: & @chatting

>$addoption &:upside_down: & @lurking

>$addoption &:joystick: & @gaming

>$addchanger 123456789012345678      <--- Desired channel ID goes here
```

Will lead to this message on the desired channel

![example](https://user-images.githubusercontent.com/88753590/149683355-8ee6f1f8-fc8b-47ba-9e41-21c501542631.PNG)

To make a vote with four options

```
>$addoption &:dog: &dogs

>$addoption &:cat: &cats

>$addoption &:bird: &birds

>$addoption &:hamster: &hamsters

>$addvote 123456789012345678      <--- Desired channel ID goes here
```

Will make this poll

![vote](https://user-images.githubusercontent.com/88753590/149683448-5ff4d7d6-fe46-4532-bbde-986433d92288.PNG)

## Graph making mechanic

EDIT: After noticing that generating all graphs at once would flood the chats a bit and also spike RAM usage for a moment, the decisison was to add a choice to
the user of which graphs to generate. There are currently four graphs that are used with the parameters A, B, C and D.

This mechanic was added to the bot as a way to help recruiters to easily and seamlessly visualize data with a few commands.
The basic commands are 
```$addpoint <name> <day>/<month>/<year> <qp hs> <mt hs> <lines> <tetrises> <allclears> <tspins> <challenges> <streak> <b2bs>```
and
```$generategraphs <graphs to generate>```

The way this works is you add a data point based on user data from the profile tab in-game, you can name it whatever you want.
Once you have two or more data points loaded, you can use ```$generategraphs``` to create (currently) four graphs displaying helpful information for each player.

An immense shoutout to BlakeD38, without him, this mechanic would have been very limited.

**Examples:**

```
> $addpoint player1 25/2/2021 75000 550000 250000 15000 2 250 275 15 7500

> $addpoint player2 25/2/2020 25000 115000 50000 4000 1 100 105 7 450

> $generategraphs
```
Note: On current version, this will not generate. In order to generate the first graph, use parameter 'A', in order to generate third and fourth graphs at once,
use parameter 'CD', and so on. In order to generate all four use parameter 'ABCD'.

Will generate these graphs, currently:
![temp](https://user-images.githubusercontent.com/88753590/155718587-36ed709e-7a32-4bbb-bd9b-2f0b1aaab452.png)
![temp](https://user-images.githubusercontent.com/88753590/155718603-9ee7a9d7-c3fc-4551-87e2-96047da904c5.png)
![temp](https://user-images.githubusercontent.com/88753590/155718611-f130bc07-53e4-47c2-80a4-0474e8325f50.png)
![temp](https://user-images.githubusercontent.com/88753590/155718622-e00ce114-87c2-4207-9c7e-1d83495b2521.png)

(Please note that with only two points the scatter graphs look empty, they're better used with 3 or more points)

But the biggest hardship when it comes to this mechanic is the repetitive and monotonous task of writing down all parameters every time, for each player.

With that in mind, along with the two basic commands, a few other quality-of-life commands were added to store the point once and load again any time without needing to 
write down each parameter

The commands are:
```$storepoint <name> <day>/<month>/<year> <qp hs> <mt hs> <lines> <tetrises> <allclears> <tspins> <challenges> <streak> <b2bs>```
```$deletepoint <name>```
```$loadpoint <name>```
```$listpoints```
```$printpoint <name>```
```$clearpoints```
```$loadallpoints```

The names should be somewhat self-explanatory, but to keep things short, you can save and load points for the graphs with these.

```$storepoint <param>``` Stores the data for a point with that name, that point can then be used in the future. Using this command twice with the same name will NOT
overwrite the data.

```$deletepoint <name>``` Deletes a stored point

```$loadpoint <name>``` Loads a stored point for use in the graph making. Stored points will only be used in the graphs if they are loaded.

```$listpoints``` Lists all points

```$printpoint <name>``` Prints the parameters stored for a point

```$clearpoints``` Deletes all points

```$loadallpoints``` Loads all points. Warning: The radar chart gets really cluttered and hard to read with too many points.

**Examples:**

```
> $storepoint user1 <parameters1...>

> $storepoint user2 <parameters2...>

> $storepoint user3 <parameters3...>

> $storepoint user4 <parameters4...>

> $listpoints 

RRB:
List of stored points:
user1
user2
user3
user4

> $loadpoint user1

> $loadpoint user4

> $loadpoint user3

> $generategraphs

RRB:
(Would make a graph with users 1, 3 and 4)

> $printpoint user1

RRB:
(parameters1...)

> $deletepoint user4

> $listpoints

RRB:
List of stored points:
user1
user2
user3

> $loadallpoints

> $generategraphs

RRB:
(Would make a graph with users 1,2 and 3)

> $clearpoints

> $printpoints

RRB:
List of stored points:

```

## Other data commands

```$setreferencepps <pps>```

Sets the PPS used for reference in the calculators. Default is 1.66.

```$printserverdata```

Prints the stored data for that server.

```$resetserverdata```

Resets all data for that server to the defaults.

```$clearcache```

Clears data for that server that are somewhat temporary.

```$forgetchangermessages```

Removes all role changing messages from list of interactable messages, so users can no longer use them to change roles and new ones need to be created or re-appended

```$appendchangerid <messageID>```

Adds a message to the list of interactable messages, so users adding reactions to it will trigger the check for giving roles, useful if server data was reset and can
help avoid unecessary pings.

That's all of the mechanics for now, if you have any ideas for new mechanics or changes to existing mechanics, don't hesitate to say them so this project can
keep growing :D

**Note:** Your server may not have access to all features listed here, as there is a whitelist for trusted servers for the
time being. If you wish to get all features, just use ```$requestverify``` and I'll be in contact asap.

# Version Changelog

### -v1
Created basic timer and customization functionality

### -v2
Added persistance and server-dependent variables with Pickle files
    
Added multithreading
    
Started using DisCloud for hosting the bot

### -v3
Made informational commands
    
Added the team rotation mechanic
    
Added the Tetris task pinging mechanic

### -v4
Overall changes to commands and permissions
    
Added daily task pinging mechanic
    
Made the time limit variable for each server

### -v5
Added the player stats calculator
    
Added datetime support for the timers

### -v6
Replaced some repetitive messages with reactions
    
Removed countdown timer, for several reasons
    
Changed persistent files from several Pickle files to a single Excel file
    
Shifted data loading and writing to specific points to save resources
    
Added daily reminders alogside integration with AlarmBot

### -v7
Moved most text strings to a separate file to keep things shorter and cleaner

Changed the way to arrange the data being worked with so it's easier to deal with, more concise and easier to expand upon
    
Added ```$freespot``` and ```$fullguide``` commands

Fixed some issues

### -v8
Changed the way to arrange data again, so it's even better to work with

Added a debug command and made data presentation more concise

Made average PPS used on calculations server-based and changeable for each server

Moved most functions to different files to make things more compact and readable

### -v9
Added three new calculators

Added vote/role changing mechanic

Moved more remaining functions to different files

Removed the need for (&) before most commands to make them easier to use in mobile

Added several data handling commands

Renamed the bot to "Tetris Mobile RRBot" and changed the profile picture to that of a T Tetrimino

Rewrote lots of texts

Help command is now sent in DMs

Overall cleanup and tweaking

### -v10
Changed way to store and organize data to a more secure and much cleaner way. Data is now stored with dill, because it stores and retrieves classes as a whole, much better for
maintaining. No more bubblegun and duct tape holding the code together...

Added more classes to organize code

Added graph making mechanic and point storing mechanic

Changed way private data is stored. It now stays in a separate file far away from GitHub

Moved some raw calculations to functions

Added a few data handling commands

Fixed some bugs

Overall cleanup of the code
