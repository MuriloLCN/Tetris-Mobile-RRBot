import datetime


class ServerData:
    """
    Main class for organizing data for a given server and storing semi-persistent things
    """

    def __init__(self):
        self.id = ''
        self.alarms = dict()  # {user: [id, silenced]}
        self.cached = Cache()
        self.proprieties = Custom()
        self.rolechangerids = []
        self.rotationvisualizerids = dict()
        self.storedpoints = dict()  # {name: Parameters(data)}


class Cache:
    """
    Minor class for organizing low-persistence data for a given server
    """

    def __init__(self):
        self.entryqueue = []
        self.exitqueue = []
        self.donedailies = []
        self.savedtetrises = []
        self.helpmessageids = []
        self.rolepairs = dict()  # {role: reaction}
        self.datapoints = dict()  # {name: Parameters()}


class Custom:
    """
    Minor class for organizing persistent data for a given server
    """

    def __init__(self):
        self.currentrole = '@exampleRole'
        self.currentlimit = 15
        self.referencepps = 1.66
        # Default parameters passed in
        self.referenceparameters = Parameters(2021, 6, 15, 100000, 1000000, 75000, 10000, 50, 750, 1000, 100, 5000)


class Parameters:
    """
    Major class to organize data parameters, used for many different things
    """

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


class Match:
    """
    Class used for organizing matches
    """

    def __init__(self):
        self.players = dict()  # {playerID: [channelID, playerName]}
        self.playerlimit = 5
        self.messageids = dict()  # {channelID: messageID}

    def reset(self):
        """
        Used to reset the Match instance to a virgin state
        """
        # There is only one match that runs currently, so instead of having multiple instances, there is just one that
        # resets once the match starts. This will be expanded upon in the future.
        self.players = dict()
        self.playerlimit = 5
        self.messageids = dict()

    def getPlayerList(self):
        """
        Gets the name of all players in the current match into a sting form
        :return: A string with all connected players
        """
        text = ''
        for player in self.players.keys():
            text = text + str(self.players[player][1]) + '\n'
        return text

    def getMessageContent(self):
        """
        Formats and makes the sting with the stats for the current Match instance
        :return: Status string
        """
        return "Matchmaking status\n" \
               "Players connected: {}/{}\n" \
               "Player list: \n{}".format(len(self.players.keys()), self.playerlimit, self.getPlayerList())


lookout = [Custom, Cache, Parameters]


def recursiveInwardsCheck(oldObject: ServerData, newObject: ServerData) -> ServerData:
    """
    Recursively checks objects and write their data into a new class. Used to make sure that should a new
    attribute be added to a class, the old instances will be updated to have that attribute

    :param oldObject: The old object to be copied
    :param newObject: A new instance of the now updated class
    :return: The new and updated object
    """

    # The type declaration is not exactly right, it just is ServerData so the IDE stops saying it's an error, but this
    # function will work with any object, as long as target classes to be copied are in the lookout list above
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
def updateObject(oldObject: ServerData) -> ServerData:
    """
    Updates the ServerData instances to the current status of the main class to avoid missing attributes

    :param oldObject: The original ServerData instance
    :return: The updated ServerData instance
    """
    newObject = ServerData()  # Blank object

    return recursiveInwardsCheck(oldObject, newObject)
