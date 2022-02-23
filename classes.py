import datetime

# {user: [id, silenced]}

class ServerData:
    def __init__(self):
        self.id = ''
        self.alarms = dict()
        self.cached = Cache()
        self.proprieties = Custom()
        self.rolechangerids = []


class Cache:
    def __init__(self):
        self.entryqueue = []
        self.exitqueue = []
        self.donedailies = []
        self.savedtetrises = []
        self.rolepairs = dict()


class Custom:
    def __init__(self):
        self.currentrole = '@exampleRole'
        self.currentlimit = 15
        self.botchannel = 'bot_channel'
        self.reminderchannel = 'reminder_channel'
        self.referencepps = 1.66
        # Default parameters passed in
        self.referenceparameters = Parameters(2021, 6, 15, 100000, 1000000, 75000, 10000, 50, 750, 1000, 100)


class Parameters:
    def __init__(self, y, m, d, qphs, mths, lines, tet, allc, tsd, chall, strk):
        self.joindate = datetime.date(y, m, d)
        self.quickplayhs = qphs
        self.marathonhs = mths
        self.lines = lines
        self.tetrises = tet
        self.allclears = allc
        self.tspins = tsd
        self.challenges = chall
        self.streak = strk
