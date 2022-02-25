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


# Function to update all previously stored objects in order to avoid missing attributes when a new feature is made
def updateObject(oldObject):
    newObject = ServerData()

    newObject.id = oldObject.id
    newObject.alarms = oldObject.alarms
    newObject.rolechangerids = oldObject.rolechangerids

    # New things that are added to the main ServerData class might need to be checked individually after each update,
    # though after being run once they can be skipped as all servers are updated when the bot is turned on
    try:
        newObject.storedpoints = oldObject.storedpoints
    except AttributeError:
        newObject.storedpoints = dict()

    newCache = Cache()
    newProprieties = Custom()
    newParameters = Parameters(2021, 6, 15, 100000, 1000000, 75000, 10000, 50, 750, 1000, 100, 5000)

    for var in vars(oldObject.cached):
        try:
            newCache.var = var
        except AttributeError:
            pass

    for var in vars(oldObject.proprieties):
        try:
            newProprieties.var = var
        except AttributeError:
            pass

    for var in vars(oldObject.proprieties.referenceparameters):
        try:
            newParameters.var = var
        except AttributeError:
            pass

    newObject.cached = newCache
    newObject.proprieties = newProprieties
    newObject.proprieties.referenceparameters = newParameters

    return newObject
