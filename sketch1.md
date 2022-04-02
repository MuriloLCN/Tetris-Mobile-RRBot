Sketch of a new and better guide for this repo, WIP

Introduction
Summary
User guide
General design
Changelog

# Tetris Mobile Royale Reminder Bot (RRBot)

## Summary

# 1. User guide
## 1.1 What is this bot
## 1.2 Installation
## 1.3 Public systems
### 1.3.1 Timer system
#### 1.3.1.1 Matchmaking system
### 1.3.2 Content commands
### 1.3.3 Calculator commands
### 1.3.4 Data commands
## 1.4 Verified-only systems
### 1.4.1 Calculator commands
### 1.4.2 Rotation System
### 1.4.3 Pinging System
#### 1.4.3.1 Tetris task pinging
#### 1.4.3.2 Daily task pinging
### 1.4.4 Info commands
### 1.4.5 Daily reminder system
### 1.4.6 Role-changing message system
#### 1.4.6.1 Vote system
### 1.4.7 Graph making system
#### 1.4.7.1 Point system
### 1.4.8 Admin commands

## 3. General design
## 4. Changelog

# 1. RRBot User Guide

This section is written for those that are going to use RRBot in their servers.

## 1.1. What is this bot

The purpose of this bot, initially, was simply to make it easier for two people enter the same match together in the Royale mode in the Tetris Mobile game,
hence the name, but has since grown to have a lot of tools used to coordinate and manage top-level teams in the game. Many tools like calculators, reminders,
graphs, etc. have been added with teams in mind.

This bot contains several systems and lots of commands made with the organization of an international team of players through a Discord server in mind, as has been
tailored around this concept. In order to access most of the systems and functions within the bot, a server needs to be verified, as this is an ongoing project and
things can break from time to time. To verify a server, simply drop me a DM (PyrooKil#6673) or use the command '$requestverify'.

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

### 1.3.1.1 Matchmaking system

This system is still very rudimentary and early in creation. The core idea behind it is to make a more dynamic and easier to use version of the timer system, but
in it's current state it still lacks a lot of features.

Commands:
 ```$matchmaking```
 
 It shows a self updating message with the list of players in the matchmaking lobby with you. Once the lobby fills up, the players in it are pinged.
 
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
  
## 1.4 Verified-only systems

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
### 1.4.6.1 Vote system

### 1.4.7 Graph making system
### 1.4.7.1 Point system

### 1.4.8 Admin commands

  >> Important note: Custom emojis won't work <<
> $addoption &<:reaction:> &<@role/option text>
Stores an option for a text/role to be paired with a reaction.
> $addchanger <channelID>
Uses all stored options to make a message that users can use to change their roles.
> $addvote <channelID>
Uses all stored options to make a message in which users can vote.
  
> $addpoint <name> <day>/<month>/<year> <quickplay highscore> <marathon highscore> <lines> <tetrises> <allclears> <tspins> <challenges> <login streak> <back-to-backs>
> $storepoint <name> <day>/<month>/<year> <quickplay highscore> <marathon highscore> <lines> <tetrises> <allclears> <tspins> <challenges> <login streak> <back-to-backs>
> $deletepoint <pointName>
> $loadpoint <pointName>
> $listpoints
> $clearpoints
> $printpoint <pointName>
> $loadallpoints
> $generategraphs <any subset of 'ABCD'>
  
> $setreferencepps <pps>
> $printserverdata
> $resetserverdata
> $clearcache
> $updatereferencevalues <name> <day>/<month>/<year> <quickplay highscore> <marathon highscore> <lines> <tetrises> <allclears> <tspins> <challenges> <login streak> <back-to-backs>
> $forgetchangermessages
> $appendchangerid <messageID>




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

### First public release
