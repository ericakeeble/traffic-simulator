class Behavior:
    def doThis(self):
        pass


class Slow(Behavior):
    def doThis(self):
        return -5


class Normal(Behavior):
    def doThis(self):
        return 0


class Fast(Behavior):
    def doThis(self):
        return 5
