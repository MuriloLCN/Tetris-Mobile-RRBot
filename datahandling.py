import dill
import classes
import os


def loadData(serverID: str) -> classes.ServerData:
    """
    Loads the data stored in the dataset into the bot
    :return: A dict containing the stored data ({Server ID (int): Server Data (classes.ServerData),...})
    """

    dirname = os.path.abspath(__file__)
    finalPath = dirname.replace('datahandling.py', "servers\\")

    if not os.path.exists(finalPath + serverID + '.pkl'):
        t = open(finalPath + serverID + '.pkl', 'w')
        t.close()

    with open(f"{finalPath}{serverID}.pkl", "rb") as f:
        try:
            serverData = dill.load(f)
        except EOFError:
            return classes.ServerData()
        if type(serverData) != classes.ServerData:
            return classes.ServerData()
        return serverData


def writeserverdata(serverID: str, serverData: classes.ServerData):
    """
    Writes the current stored data for that server into the stored file

    :param serverID: The ID of the server which to retrieve data (int or str)
    :param serverData: The updated data for that server (classes.ServerData)
    """
    dirname = os.path.abspath(__file__)
    finalPath = dirname.replace('datahandling.py', "servers\\")

    # Save it to file
    with open(f"{finalPath}{serverID}.pkl", 'wb') as f:
        dill.dump(serverData, f)


# Simply writes a new entry with the default parameters
def createnewentry(serverID: str):
    """
    Creates a new entry with default data for new servers

    :param serverID: The ID of the server which to retrieve data (int or str)
    """
    writeserverdata(serverID, classes.ServerData())
