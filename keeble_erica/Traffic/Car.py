class Car:
    def __init__(self, carID=0, behavior=None):
        self.id = carID
        self.currBehavior = behavior
        self.location = 0

    def setBehavior(self, behavior):
        self.currBehavior = behavior

    def callBehavior(self):
        return self.currBehavior.doThis()

    def calculateNewLocation(self, speedLimit):
        """
        Calculates new location based on speed limit and car's behavior
        :param speedLimit: current speed limit of the car
        :return:
        """
        # new location = (old location) + (speed limit + behavior) * (30 secs)
        # converting from miles/hour to miles/min
        speed = speedLimit + self.callBehavior()
        newLoc = self.location + (speed / 60) * 0.5
        return newLoc

    def setNewLocation(self, newLoc):
        self.location = newLoc

    def __str__(self):
        formattedLoc = "%.2f" % self.location
        return '{0: <15}'.format(str(self.id) + ': ' + str(formattedLoc) + ' ')
