import dill

import classes


# Loads stored data from file when the bot is turned on
# Data is stored in the form of a dict with pairs being {serverID(int): data(classes.ServerData)}
# TODO: Change data from 'all data stored in a single file' to 'a folder containing separate files for each server'
# There's no real reason to load all data all the time. For now it's good but if it was something bigger or heavier
# this would be an important thing to do.
def loadDict() -> dict:
    """
    Loads the data stored in the dataset into the bot
    :return: A dict containing the stored data ({Server ID (int): Server Data (classes.ServerData),...})
    """
    with open('dataset.pkl', 'rb') as f:
        try:
            setdict = dill.load(f)
        except EOFError:
            return dict()
        if type(setdict) != dict:
            return dict()
        return setdict


def getclass(serverID: str, setdict: dict) -> classes.ServerData:
    """
    Retrieves the stored classes.ServerData for a given server using it's server ID

    :param serverID: The ID of the server which to retrieve data (int or str)
    :param setdict: The data dict() in which the data is stored (dict)
    :raise IndexError: If there is no data for the given server ID
    :return: The stored data class (classes.ServerData)
    """
    serverID = int(serverID)
    if serverID in setdict:
        storedclass = setdict.get(serverID)
        return storedclass
    else:
        raise IndexError


# TODO: Normalize some of the input types so that things like serverID that sometimes are str and sometimes are int will
# always be of the same type
def getserverdata(serverID: str, setdict: dict) -> classes.ServerData:
    """
    Retrieves the data stored for a given serverID on the dataset. Creates a new entry and returns a default object if
    the server still does not have data stored
    :param serverID: The ID of the server which to retrieve data (int or str)
    :param setdict: The data dict() in which the data is stored (dict)
    :return: The stored (or new, if not found) data for that server (classes.ServerData)
    """
    try:
        storedclass = getclass(serverID, setdict)
    except IndexError:
        createnewentry(serverID, setdict)
        print('server id not in db, creating new entry: ' + str(serverID))
        return classes.ServerData()
    return storedclass


def writeserverdata(serverID: str, serverData: classes.ServerData, setdict: dict):
    """
    Writes the current stored data for that server into the stored file

    :param serverID: The ID of the server which to retrieve data (int or str)
    :param serverData: The updated data for that server (classes.ServerData)
    :param setdict: The data dict() in which the data is stored (dict)
    """
    # Update server data on the dataset dict
    setdict[int(serverID)] = serverData

    # Save it to file
    with open('dataset.pkl', 'wb') as f:
        dill.dump(setdict, f)


# Simply writes a new entry with the default parameters
def createnewentry(serverID: str, setdict: dict):
    """
    Creates a new entry with default data for new servers

    :param serverID: The ID of the server which to retrieve data (int or str)
    :param setdict: The data dict() in which the data is stored (dict)
    """
    writeserverdata(serverID, classes.ServerData(), setdict)
