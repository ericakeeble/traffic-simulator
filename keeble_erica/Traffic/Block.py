class Block:
    def __init__(self, blockLength=0.5, speedLimit=30):
        self.mph = speedLimit
        self.length = blockLength
        self.carsGoingRight = []  # --> [new .. old]
        self.carsGoingLeft = []  # <-- [old ... new]

    def __str__(self):
        arrows = "-" + str(len(self.carsGoingRight)) + "-> "
        arrows += "<-" + str(len(self.carsGoingLeft)) + "-"
        return arrows

    def addCar(self, car, direction):
        """
        Adds car to the block in the correct direction
        :param car: car to add
        :param direction: indicates which list to insert car into
        :return:
        """
        if direction == "goingRight":
            self.carsGoingRight.insert(0, car)  # [newCar ... oldCars]
        elif direction == "goingLeft":
            self.carsGoingLeft.append(car)  # [oldCars ... newCar]

    def moveCar(self, block, direction):
        """
        Moves car from this block to the parameter block, in the parameter direction
        :param block: move car to this block
        :param direction: in this direction
        :return:
        """
        if direction == "Right":
            # pop last car in "cars going right" list, then insert in next block
            car = self.carsGoingRight.pop(len(self.carsGoingRight) - 1)
            car.location = 0
            block.carsGoingRight.insert(0, car)
        elif direction == "Left":
            # pop first car in "cars going left" list, then insert in next block
            car = self.carsGoingLeft.pop(0)
            car.location = 0
            block.carsGoingLeft.insert(len(block.carsGoingLeft), car)

    def exitCar(self, direction, car):
        """
        Remove car from this block in the indicated direction
        :param direction: indicates which list to remove car from
        :param car: car to remove
        :return:
        """
        if direction == "Right":
            self.carsGoingRight.remove(car)
            # self.carsGoingRight.pop(len(self.carsGoingRight)-1)
        elif direction == "Left":
            self.carsGoingLeft.remove(car)
            # self.carsGoingLeft.pop(0)

    def makeIterator(self, direction):
        if direction == "Right":
            return self.IterBlock(self.carsGoingRight, direction)
        elif direction == "Left":
            return self.IterBlock(self.carsGoingLeft, direction)

    class IterBlock:
        def __init__(self, cars, direction):
            self.__cars = cars
            if direction == "Left":
                self.__index = 0
                self.__increment = 1
            elif direction == "Right":
                self.__index = len(cars) - 1
                self.__increment = -1

        # GRADING: INTER_CAR
        def __iter__(self):
            return self

        def __next__(self):
            try:
                car = self.__cars[self.__index]
                self.__index += self.__increment
                if self.__index < -1:
                    raise StopIteration
                return car
            except:
                raise StopIteration
