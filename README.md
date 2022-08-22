# Tetris Mobile Royale Reminder Bot (RRBot)

## Summary

## 1. User guide
### 1.1 What is this bot
### 1.2 Installation
### 1.3 Public systems
#### 1.3.1 Timer system
##### 1.3.1.1 Matchmaking system
#### 1.3.2 Content commands
#### 1.3.3 Calculator commands
#### 1.3.4 Data commands
### 1.4 Verified-only systems
#### 1.4.1 Calculator commands
#### 1.4.2 Rotation System
#### 1.4.3 Pinging System
##### 1.4.3.1 Tetris task pinging
##### 1.4.3.2 Daily task pinging
#### 1.4.4 Info commands
#### 1.4.5 Daily reminder system
#### 1.4.6 Role-changing message system
##### 1.4.6.1 Vote system
#### 1.4.7 Graph making system
##### 1.4.7.1 Point system
#### 1.4.8 Admin commands
## 2. General design
## 3. Changelog

# 1. RRBot User Guide

This section is written for those that are going to use RRBot in their servers.

## 1.1. What is this bot

The purpose of this bot, initially, was simply to make it easier for two people enter the same match together in the Royale mode in the Tetris Mobile game,
hence the name, but has since grown to have a lot of tools used to coordinate and manage top-level teams in the game. Many tools like calculators, reminders,
graphs, etc. have been added with teams in mind.

This bot contains several systems and lots of commands made with the organization of an international team of players through a Discord server in mind, as has been
tailored around this concept.

## 1.2 Installation

You can add the bot to your server (like most bots) with this link: https://discord.com/api/oauth2/authorize?client_id=867241160062009360&permissions=8&scope=bot

## 1.3 Public systems

These are the systems/commands that every server has access to by default.

### 1.3.1 Timer system

This is the original system that gave life to this project. The idea behind it is simple: create a timer close to now, get ready to join the matchmaking lobby in-game,
join in sync with your mates once you guys get pinged.

Commands:

```$createtimer <time in minutes>```
  or
```$createtimer &<timezone> &<hour>:<minute>```

Both create a timer from N minutes from now. The first one takes in the time directly, so if let's say you passed in 9 in the command, it'd take 9 minutes for
the timer to run out and ping you. The second one takes a timezone and a time, and once it reaches that time, you'll be pinged.

 ### 1.3.2 Content commands
 
 These are simple commands to help you with some info.

Commands:

```$tasks```
Lists the current task cycle for teams

```$bonus```
Describes the current bonus mechanic in-game for teams

```$guides```
Some community-made guides for Tetris

```$fullguide```
Links to this page

### 1.3.3 Calculator commands

In the open version, there is only one command. Most other calculators are in the verified-only field for many reasons.

Commands:

```$ppscalculator <lines>```
Calculates the PPS, where LINES is the number of lines cleared at the end of a quick-play (3 minutes) game.

### 1.3.4 Data commands

Commands for admins to customize and tweak some parameters regarding their server.
 
Commands:

```$setrole <@role>```
Changes the role that gets pinged in the timer system.

```$setnewlimit <limit>```
Changes the time limit of how long a timer can be.
  
## ~1.4 Verified-only systems~

## Notice: The verification system was lifted so now every server has access to these commands

### 1.4.1 Calculator commands

These are the calculators built to make looking for patterns in player data easier.

```$calculateaverage <total lines> <month>/<day>/<full year>```
Calculates the average lines cleared per day and time played per day (based on server-defined refence PPS) of a player, where TOTAL LINES is the Lines Removed
stat on the player's profile and MONTH/DAY/YEAR are the join dates on the player's profile (read: when they started playing)

```$royalecalcaverage <day of the month> <royale points>```
Calculates the average lines cleared per day and time played per day (based on server-defined reference parameters) of a player, where DAY OF THE MONTH is how long
the current season's competition has been going for and ROYALE POINTS is the number of royale score they've gotten so far into the competition. Currently, winning
one match gets you 10k points.

```$compcalculator <day>/<month>/<year> <quickplay highscore> <marathon highscore> <lines> <tetrises> <all clears> <tspins> <challenges> <streak>```
Equation made by BlakeD38. Calculates a player's Activity Score and Technique Score based on many of their stats and in relation to the current comparative
parameters for the server. This is a comparative calculator and, for example, an Activity Score of 2.0 means that the player has an activity score 2x higher than
the same calculated for the reference parameters while a score of 0.5 means that the score is half of that calculated for the reference parameters.

By default, a predefined set of parameters is assigned to every server, which can be customized at will. The parameters are all from the player's profile
statistics, where DAY/MONTH/YEAR is their join date, QUICKPLAY and MARATHON HIGHSCORE are their highest scores ever for the respective modes, LINES is the total
of lines the player has ever removed in the game, TETRISES is the total number of Tetris Line Clears the player has ever performed, TSPINS is the total number
of T-Spins the player has ever performed, ALL CLEARS is the total number of All Clears/Perfect Clears the player has ever performed, CHALLENGES is the total number
of single-player seasonal tasks/challenges the player has ever completed and STREAK is their current login streak.

These parameters (quickplay highscore, lines, etc) are used in other places too, and they're all the same, so this is the only time it should be needed to clarify
what those parameters are.

```$diffcalculator <tetrises> <tspins> <b2bs> <lines>```
This is a Difficult Line Clears rate calculator. It calculates three rates: Difficult Line Clears / Total Line Clears, Back-to-Backs / Total Line Clears, and
Back-to-backs / Difficult Line Clears. These serve as indicators of efficiency related to the use of the pieces in a tetris game (note: but are not all, things
like downstacking and other important skills are not picked up by these numbers, and like every calculator, data should be seen with a pinch of salt, humans are
not numbers). It calculates the three percentages where B2BS is the number of Back-To-Back Line Clears the player has ever performed.

### 1.4.2 Rotation system

This system is designed to help teams where the might be more than 30 players wanting to play at the same time, or teams where players from different timezones
may want to organize their workflow more efficiently and swiftly. The core idea is: If you want to do an action (enter/leave), you join a queue until a person with a matching
interest joins it (opposing, leave/enter) or there is a move opportunity for you, in both cases you will be pinged to do your move.

Commands:

```$enter```
Joins the ENTER TEAM queue

```$leave```
Joins the LEAVE TEAM queue

```$freespot```
Signals the next person waiting to join the team that there is a free spot.

```$addvisualizer```
Adds a visual board where the queues are displayed. Helps to see and understand better the current status of the queues.

### 1.4.3 Pinging system

This is a simple and niche system. The basic idea is that you do an action but need to wait for an event to happen before moving forward. In this case the
actions are unloading stored Tetris Line Clears and proceeding with Team task completion.

#### 1.4.3.1 Tetris task pinging

This helps people who store Tetris Line Clears in Marathon mode and then only count them in whenever the team needs it for the task.

Commands:

```$savedtetris```
Signals the bot that you have Tetris Line Clears stored in a marathon game.

```$tetristask```
Signals the bot that the Tetris Line Clears task is live, and thus will proceed to ping all players who have stored Tetrises as to put them in for the task.

#### 1.4.3.2 Daily task pinging

Similar to the one above, this one is for those waiting for the team to reach a higher bonus (usually 400%) before carrying on with their gameplay.

Commands:

```$dailiesdone```
Signals the bot that you have done your daily tasks and is waiting for the team to reach full bonus. Also silences your daily reminder if you have one.

```$gotfullbonus```
Signals the bot that the team has reached full bonus, and this will procced to ping all players who were waiting for it.

### 1.4.4 Info commands

Simple info commands regarding some systems.

Commands:

```$rotation```
Help for the rotation system

```$infotetris```
Help for the tetris task system

```$fullbonusping```
Help for the bonus system

### 1.4.5 Daily reminder system

This is a very useful system in which you can set a reminder every day for you to do your daily tasks. Unlike the old system, the new one is much simpler to use
and to set up. No longer needs AlarmBot to work.

Commands:

```$reminder <hour>:<minute> <timezone> <#channel>```
Creates/Deletes your daily reminder, where HOUR:MINUTE is the time in which you'd like to be reminded, TIMEZONE is your current timezone (...-2,-1,0,1,2...) and
#CHANNEL is the channel that you'd like to receive your notifications in. You can use 123 as the channel to make them be sent in your DMs for privacy.

### 1.4.6 Role-changing message

This is our own implementation of the useful 'React here to change your role' messages. You can set up one of these messages by using the commands and generating one
or by sending your own message and adding it's id with another command. 

Commands:

```$addoption &<reaction> &<role>```
Loads an option that pairs that reaction to that role, so once in the final message someones uses that emoji, they'll gain that role.
Please bear in mind that custom emojis will not work with this.

```$addchanger <channel ID>```
Adds a role changing message with all options that were loaded beforehand to the desired channel.

Note that once a message is generated, all options are cleared for future messages.

### 1.4.6.1 Vote system

This is just a quick extension to the Role changing messages, as to easily use the same commands to make a vote message instead of a role changing one.
The vote message will be similar to the role changing one, but will have no function regarding the addition of emojis.

Commands:

```$addvote <channel ID>```
Adds a vote message with all options that were loaded beforehand to the desired channel.

### 1.4.7 Graph making system

This system simply helps team leaders to look for patterns in player data by using graphs for it. It can generate up to four different graphs as of current version.

Commands:

```$generategraphs <any subset of 'ABCD'>```
Will generate the graphs in the channel the command was sent in. The parameter 'any subset of ABCD' dictates which graphs are to be generated.
If 'A' is in the text, the first graph will be generated, same for 'B', 'C' and 'D'. So, for example, the text 'ADC' will generate all but the second graph, while
the text 'BD' will generate the second and fourth graphs, and so on. 

This command on it's own won't do anything until you have loaded some points into it. So this system is useless without this next one:

### 1.4.7.1 Point system

This point system is simply the system to manage data loading and handling for the graphs, as every graph needs to show some piece of data for it to exist.
The way data is handled is as forms of points, named collections of data.
To generate the graphs, you need to load at least two points. You can load points only once, store them to load as many times as needed, delete stored ones, and so on.
The command names should be self explanatory.

Commands:

```$addpoint <point name> <day>/<month>/<year> <quickplay highscore> <marathon highscore> <lines> <tetrises> <allclears> <tspins> <challenges> <login streak> <back-to-backs>```
This command loads a point to the graph generation process, but does not store it or anything. Load once, run once.

```$storepoint <point name> <day>/<month>/<year> <quickplay highscore> <marathon highscore> <lines> <tetrises> <allclears> <tspins> <challenges> <login streak> <back-to-backs>```
This command stores a point to be loaded as many times as needed in the future simply by using it's name. Does not automatically load it to graph generation, only
stores it.

```$loadpoint <point name>```
Loads a stored point to be used in the graph generation process. Complement to the ```$storepoint``` command above. Load once, run as many times as you want.

```$deletepoint <point name>```
Deletes a stored point.

```$printpoint <point name>```
Prints the data stored in a point.

```$listpoints```
Lists all currently stored points.

```$clearpoints```
Deletes all currently stored points.

```$loadallpoints```
Loads all currently stored points to be used in graph generation.

### 1.4.8 Admin commands

These are the admin commands that change stored server data. 

Commands:

```$setreferencepps <pps>```
Changes the reference PPS valued used in calculations. Default is 1.66 PPS.

```$printserverdata```
Prints currently stored server data.

```$resetserverdata```
Resets all currently stored server data to default.

```$clearcache```
Clears the server cached info.

```$appendchangerid <message ID>```
Adds a message ID to the list of role-changing messages so it behaves as one.

```$forgetchangermessages```
Deletes the list of role-changing messages currently active in the server so they stop working.

```$updatereferencevalues <day>/<month>/<year> <quickplay highscore> <marathon highscore> <lines> <tetrises> <allclears> <tspins> <challenges> <login streak> <back-to-backs>```
Changes the default parameters used in calculations to custom parameters.

# 2. General design

The general idea of the bot falls under this diagram.

![sysdiag](https://user-images.githubusercontent.com/88753590/161403158-bfaef102-8424-4f4f-be9f-465c6299596f.png)

Here's what each file does:

~```dataset.pkl```~ (now every server as a separate file kept in ```.../servers/```)
and
```alarmset.pkl```
are both used to store data and serve as sort of databases.
```/servers/``` stores pickle files for each server and loads their server data directly, where the data is an instance of the class serverData defined in ```classes.py```
```alarmset.pkl``` stores a Python Dict containing the following:
```{player ID: [hour, minute, timezone, desired channel ID, isSilenced]}```, where only isSilenced is a Boolean while the rest are Integers. 

```requirements.txt``` are the dependencies of the project.

```infocmds.py```, ```savingtetris.py```, ```helpcommand.py```, ```bonuspinging.py```, ```timer.py```, ```rolegiving.py```, ```rotation.py```,
```graphs.py```, ```dataupdate.py``` and ```calculators.py``` are the command files. They are where the magic happens and can be seen as merely extensions of the
```main.py``` file, as all of their context comes from there. It could all be done in one file but it's much better to keep separate systems in separate files for
organization. 

```datahandling.py``` and ```classes.py``` are very important files, as in them are defined functions and classes that are used throughout the code.
```datahandling.py``` contains functions related to storing and retrieving server data from the files, and ```classes.py``` contains the base classes used as
structure for the data throughout all files.

```clock.py``` is an odd file, as it has it's own methods for file handling, commands and loop function (for the daily reminder system) in itself. It deals with
things related to the function of the daily reminder system, and serves as a complete replacement of the need of AlarmBot to work.

```main.py``` is the main file, and also the one that needs to run to start the bot. It imports all other files and is where the messages are first forwarded to.

```performancetests.py``` is a quick set of tests for commands in terms of input sanitizing and performance. Originally added because of a memory leak, not very
useful on most occasions.

Two files are used in the project but are not in the repository, as they store private data privately and locally.
 
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

Added basic matchmaking system

### -v11

Reworked the help command

Added visualizer to rotation system

Removed commands: $seasons, $modes and $publisher

Added new daily reminder system and removed old one

AlarmBot no longer needed for the new system to work

Rewrote many things

Better documentation of the code
