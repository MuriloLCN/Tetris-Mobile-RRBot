import datetime

# Main data object with semi-persistent data


class ServerData:
    def __init__(self):
        self.id = ''
        self.alarms = dict()  # {user: [id, silenced]}
        self.cached = Cache()
        self.proprieties = Custom()
        self.rolechangerids = []
        self.storedpoints = dict()  # {name: Parameters(data)}


# Subclass containing temporary data
class Cache:
    def __init__(self):
        self.entryqueue = []
        self.exitqueue = []
        self.donedailies = []
        self.savedtetrises = []
        self.rolepairs = dict()  # {role: reaction}
        self.datapoints = dict()  # {name: Parameters()}


# Subclass containing persistent server-defined data
class Custom:
    def __init__(self):
        self.currentrole = '@exampleRole'
        self.currentlimit = 15
        self.botchannel = 'bot_channel'
        self.reminderchannel = 'reminder_channel'
        self.referencepps = 1.66
        # Default parameters passed in
        self.referenceparameters = Parameters(2021, 6, 15, 100000, 1000000, 75000, 10000, 50, 750, 1000, 100, 5000)


# Class to organize parameters for calculations. Also used as subclass from Custom()
class Parameters:
    def __init__(self, y, m, d, qphs, mths, lines, tet, allc, tsd, chall, strk, btb):
        self.joindate = datetime.date(y, m, d)
        self.quickplayhs = qphs
        self.marathonhs = mths
        self.lines = lines
        self.tetrises = tet
        self.allclears = allc
        self.tspins = tsd
        self.challenges = chall
        self.streak = strk
        self.backtoback = btb


# Class to organize matchmaking
class Match:
    def __init__(self):
        self.players = dict()  # {playerID: [channelID, playerName]}
        self.playerlimit = 5
        self.messageids = dict()  # {channelID: messageID}

    def reset(self):
        self.players = dict()
        self.playerlimit = 5
        self.messageids = dict()

    def getPlayerList(self):
        text = ''
        for player in self.players.keys():
            text = text + str(self.players[player][1]) + '\n'
        return text

    def getMessageContent(self):
        return "Matchmaking status\n" \
               "Players connected: {}/{}\n" \
               "Player list: \n{}".format(len(self.players.keys()), self.playerlimit, self.getPlayerList())


lookout = [Custom, Cache, Parameters]


def recursiveInwardsCheck(oldObject, newObject):
    for var in vars(oldObject):
        if type(getattr(oldObject, var)) not in lookout:
            if var not in vars(newObject):
                pass
            else:
                ltz = getattr(oldObject, var)
                setattr(newObject, var, ltz)
        else:
            recursiveInwardsCheck(getattr(oldObject, var), getattr(newObject, var))
    return newObject

# Function to update all previously stored objects in order to avoid missing attributes when a new feature is made


def updateObject(oldObject):
    newObject = ServerData()  # Blank object

    return recursiveInwardsCheck(oldObject, newObject)
