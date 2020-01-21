from keeble_erica.Traffic.Light import Light
from keeble_erica.Traffic.Block import *
from keeble_erica.Traffic.Car import *


class Street:
    """
        Return the x intercept of the line M{y=m*x+b}.  The X{x intercept}
        of a line is the point at which it crosses the x axis (M{y=0}).

        This function can be used in conjuction with L{z_transform} to
        find an arbitrary function's zeros.

        @type  m: number
        @param m: The slope of the line.
        @type  b: number
        @param b: The y intercept of the line.  The X{y intercept} of a
                  line is the point at which it crosses the y axis (M{x=0}).
        @rtype:   number
        @return:  the x intercept of the line M{y=m*x+b}.
        """
    carID = 1

    def __init__(self):
        b = Block()
        self.theStreet = [b]

    class IterStreet:
        def __init__(self, theStreet):
            self.__street = theStreet

        #  GRADING: INTER_STREET
        def __iter__(self):
            self.__index = 0
            return self

        def __next__(self):
            try:
                element = self.__street[self.__index]
                self.__index += 1
                return element
            except:
                raise StopIteration

    def deleteFirstBlock(self):
        self.theStreet.pop(0)

    def addCar(self, direction, behavior):
        """
        Adds a new car to the street.

        @param direction: direction the car will be traveling across the street
        @param behavior: function which indicates the speed of the driver compared to the speed limit
        """
        car = Car(self.carID, behavior)
        firstBlock, lastBlock = self.getFirstAndLastBlock()

        if direction == "goingRight":
            firstBlock.addCar(car, direction)
        elif direction == "goingLeft":
            lastBlock.addCar(car, direction)
        Street.carID += 1

    def makeIterator(self):
        return self.IterStreet(self.theStreet)

    def printStreet(self):
        print("Entry:: ", end='')
        iterator = self.IterStreet(self.theStreet)
        # GRADING: LOOP_STREET
        for element in iterator:
            print(element, end='')
        print(" ::Exit")

    def addBlock(self, block):
        self.theStreet.append(block)

    def addLight(self, light):
        self.theStreet.append(light)

    def getFirstAndLastBlock(self):
        """
        Gets the first and last block from the street
        """

        # if first and last block will be the same block if there is only one block in the street
        firstBlock = 0
        lastBlock = 0
        streetIterator = self.makeIterator()
        i = 0
        for element in streetIterator:
            if i == 0:
                firstBlock = element
            if i == len(self.theStreet) - 1:
                lastBlock = element
            i += 1
        return firstBlock, lastBlock

    def attemptMovingCarRight(self, leftBlock, rightBlock):
        """
        Moves car from left block to right block if there is a car ready to move

        @param leftBlock: block from which the car will be moving
        @param right: block to which the car will be moving
        """
        try:
            carClosestToLight = leftBlock.carsGoingRight[len(leftBlock.carsGoingRight) - 1]
            if carClosestToLight.location == leftBlock.length:
                leftBlock.moveCar(rightBlock, "Right")
        except:
            # no cars going right
            pass

    def attemptMovingCarLeft(self, leftBlock, rightBlock):
        """
        Moves car from right block to left block if there is a car ready to move

        @param leftBlock: block to which the car will be moving
        @param right: block from which the car will be moving
        """
        try:
            carClosestToLight = rightBlock.carsGoingLeft[0]
            if carClosestToLight.location == rightBlock.length:
                rightBlock.moveCar(leftBlock, "Left")
        except:
            # no cars going left
            pass

    def removeCarGoingLeft(self, block):
        """
        Removes car from block's carsGoingLeft if there is a car ready to remove

        @param block: block from which the car will be removed
        """
        try:
            # walk thru cars to find first one with distance == block.length
            carsGoingLeft = block.makeIterator("Left")
            for car in carsGoingLeft:
                if car.location == block.length:
                    block.exitCar("Left", car)
                    return
            '''
            carClosestToExit = block.carsGoingLeft[0]
            if carClosestToExit.location == block.length:
                block.exitCar("Left")'''
        except:
            # no cars going left
            pass

    def removeCarGoingRight(self, block):
        """
        Removes car from block's carsGoingLeft if there is a car ready to remove

        @param block: block from which the car will be removed
        """
        try:
            carsGoingRight = block.makeIterator("Right")
            for car in carsGoingRight:
                if car.location == block.length:
                    block.exitCar("Right", car)
                    return
        except:
            # no cars going right
            pass

    def carsMoveThruLights(self):
        """
        Moves all cars through to the next block if they are ready to move
        """

        intersection = []
        streetIterator = self.makeIterator()
        i = 0
        for element in streetIterator:
            intersection.append(element)
            if i >= 2 and i % 2 == 0:
                # update intersection
                leftBlock = intersection[0]
                light = intersection[1]
                rightBlock = intersection[2]
                if light.status == "On":
                    # Move one car right if light is green and there is a car at the intersection
                    self.attemptMovingCarRight(leftBlock, rightBlock)
                    # Move one car left if light is green and there is a car at the intersection
                    self.attemptMovingCarLeft(leftBlock, rightBlock)

                # remove updated elements from intersection as long as we are not at the last intersection in the street
                intersection.pop(0)
                intersection.pop(0)
            i += 1

    def carsExitStreet(self, ):
        """
        Removes cars from the street if they are ready to exit
        """
        firstBlock, lastBlock = self.getFirstAndLastBlock()

        self.removeCarGoingLeft(firstBlock)
        self.removeCarGoingRight(lastBlock)

    def updateCarLocations(self):
        """
        The location of each car on the street is updated based on their behavior and the current speed limit
        """
        streetIterator = self.makeIterator()
        for element in streetIterator:
            if isinstance(element, Block):
                rightLane = element.makeIterator("Right")
                leftLane = element.makeIterator("Left")
                for car in rightLane:
                    newLoc = car.calculateNewLocation(element.mph)
                    if newLoc > element.length:
                        newLoc = element.length
                    car.setNewLocation(newLoc)
                for car in leftLane:
                    newLoc = car.calculateNewLocation(element.mph)
                    if newLoc > element.length:
                        newLoc = element.length
                    car.setNewLocation(newLoc)

    def moveCarsThruStreet(self):
        """
        Moves all cars through the street that are ready to move, and exits the ones at the end of the street ready
        to exit
        """
        self.carsMoveThruLights()
        self.carsExitStreet()

    def updateAllLights(self):
        """
        Assuming 30 seconds have passed, update lights accordingly
        """
        streetIterator = self.makeIterator()
        for element in streetIterator:
            if isinstance(element, Light):
                element.updateLight()

    def update(self):
        """
        Updates the status of the street assuing 30 seconds have passed
        """
        self.updateAllLights()
        self.moveCarsThruStreet()
        self.updateCarLocations()
