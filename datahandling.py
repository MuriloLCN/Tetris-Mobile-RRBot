import dill
import classes


def loadDict():
    # Makes sure to create the file when it's run for the first time in a new env

    #open('dataset.pkl', 'a').close()

    with open('dataset.pkl', 'rb') as f:
        try:
            setdict = dill.load(f)
        except EOFError:
            return dict()
        if type(setdict) != dict:
            return dict()
        return setdict


def getclass(serverID, setdict):
    serverID = int(serverID)
    if serverID in setdict:
        storedclass = setdict.get(serverID)
        return storedclass
    else:
        # Main file needs to handle this when it happens so data gets updated
        raise IndexError


def getserverdata(serverID, setdict):
    try:
        storedclass = getclass(serverID, setdict)
    except IndexError:
        createnewentry(serverID, setdict)
        print('server id not in db, creating new entry: ' + str(serverID))
        return classes.ServerData()
    return storedclass


def writeserverdata(serverID, serverData, setdict):
    # Update server data on the dataset dict
    setdict[int(serverID)] = serverData

    # Save it to file
    with open('dataset.pkl', 'wb') as f:
        dill.dump(setdict, f)


def createnewentry(serverID, setdict):
    # Simply writes a new entry with the default parameters
    writeserverdata(serverID, classes.ServerData(), setdict)
