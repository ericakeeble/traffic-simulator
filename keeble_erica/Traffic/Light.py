class Light:
    def __init__(self, cycleLength=0):
        self.cycle = cycleLength
        self.status = "Off"
        self.countDown = self.cycle

    def __str__(self):
        return ' ::' + self.status + ":: "

    def updateLight(self):
        self.countDown -= 0.5
        if self.countDown <= 0:
            self.__switch()
            self.countDown = self.cycle

    def __switch(self):
        if self.status == "Off":
            self.status = "On"
        else:
            self.status = "Off"
