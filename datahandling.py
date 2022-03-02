import dill

import classes


# Loads stored data from file when the bot is turned on
# Data is stored in the form of a dict with pairs being {serverID(int): data(classes.ServerData)}
def loadDict():
    with open('dataset.pkl', 'rb') as f:
        try:
            setdict = dill.load(f)
        except EOFError:
            return dict()
        if type(setdict) != dict:
            return dict()
        return setdict


# Tries to retrieve the 'classes.ServerData' for a given 'serverID' in the dataset 'setdict'
def getclass(serverID, setdict):
    serverID = int(serverID)
    if serverID in setdict:
        storedclass = setdict.get(serverID)
        return storedclass
    else:
        raise IndexError


# Retrieves the data stored for a given serverID on the dataset. Creates a new entry and returns a default object if
# the server still does not have data stored
def getserverdata(serverID, setdict):
    try:
        storedclass = getclass(serverID, setdict)
    except IndexError:
        createnewentry(serverID, setdict)
        print('server id not in db, creating new entry: ' + str(serverID))
        return classes.ServerData()
    return storedclass


# Stores data to file
# setdict 'data' was made global to avoid needing to read the file on each command as an attempt to make the bot use
# less RAM. I'm not sure how much of an impact it has but I currently only have 100MB of RAM to work with so anything
# counts
def writeserverdata(serverID, serverData, setdict):
    # Update server data on the dataset dict
    setdict[int(serverID)] = serverData

    # Save it to file
    with open('dataset.pkl', 'wb') as f:
        dill.dump(setdict, f)


# Simply writes a new entry with the default parameters
def createnewentry(serverID, setdict):
    writeserverdata(serverID, classes.ServerData(), setdict)
