from keeble_erica.Traffic.Behavior import *
from keeble_erica.Traffic.Menu import *
from keeble_erica.Traffic.Street import *


def executeChoice(choice, street):
    """
    Executes whichever Menu option was chosen
    :param choice: menu option
    :param street: the street object on which to perform menu operations
    :return:
    """
    def ShowStreet():
        """
        Menu option which prints the street to the screen
        :return:
        """
        street.printStreet()
        return 0

    def MakeRoad():
        """
        Menu option which gets inputs to create the new street, and then creates it
        """

        newStreet = Street()
        blockLength = -1
        speedLimit = -1
        cycleLength = -1
        trying = -1

        try:
            numBlocks = input("Number of Blocks: ")
            numBlocks = int(numBlocks)
        except:
            "Number of blocks must be an integer."
            numBlocks = 0

        print()

        for i in range(numBlocks):
            # getting input to make the blocks
            print("_____Block " + str(i) + "_____")
            try:
                trying = "blockLength"
                blockLength = input("   Length of block in miles: ")
                blockLength = float(blockLength)
                print(end='')
                if blockLength < 0.5:
                    raise ValueError

                trying = "speedLimit"
                speedLimit = input("   Speed limit of block in mph: ")
                speedLimit = int(speedLimit)
                print(end='')
                if speedLimit < 5:
                    raise ValueError

                if i < numBlocks - 1:
                    trying = "cycleLength"
                    cycleLength = input("   Length of cycle in minutes: ")
                    cycleLength = float(cycleLength)
                    print(end='')
                    if cycleLength < 0.5 or cycleLength % 0.5 != 0:
                        raise ValueError

            except ValueError:
                if trying == "blockLength":
                    print("A block must be at least 0.5 miles. Got:", blockLength)
                elif trying == "speedLimit":
                    print("Speed limit must be at least 5 mph and a whole number. Got:", speedLimit)
                elif trying == "cycleLength":
                    print("Light cycle must be positive and an increment of 0.5 min. Got:", cycleLength)
                break

            # overwrite default block
            if i == 0:
                newStreet.deleteFirstBlock()

            # add new block to street
            newBlock = Block(blockLength, speedLimit)
            newStreet.addBlock(newBlock)

            # add new light to street
            if i < numBlocks - 1:
                newLight = Light(cycleLength)
                newStreet.addLight(newLight)

            print()

        return newStreet

    def AddCar():
        """
        Menu option which gets information to create new car, and then creates it
        """

        # get input to add car
        streetEnd = input("Which end: 0-->left, 1-->right: ")
        driverType = input("Which type: 0-->slow, 1-->norm, 2-->fast: ")

        if streetEnd == '0':
            streetEnd = "goingRight"
        elif streetEnd == '1':
            streetEnd = "goingLeft"

        if driverType == '0':
            driverType = Slow()
        elif driverType == '1':
            driverType = Normal()
        elif driverType == '2':
            driverType = Fast()

        street.addCar(streetEnd, driverType)

    def ShowCars():
        """
        Menu option which iterates through all the blocks and all the cars and prints them
        """
        streetIter = street.makeIterator()
        blockNum = 0
        for block in streetIter:
            if isinstance(block, Block):
                print("_____Block " + str(blockNum) + "_____")
                print("Block Length: " + str(round(block.length, 2)))
                print("Block Speed: " + str(block.mph))
                blockNum += 1

                leftLane = block.makeIterator("Left")  # leftLane is cars going left
                print('{0: <7}'.format("Left:"), end='')
                # GRADING: INTER_CAR
                for Lcar in leftLane:
                    print(Lcar, end='')

                print()
                rightLane = block.makeIterator("Right")  # rightLane is cars going right
                print('{0: <7}'.format("Right:"), end='')
                # GRADING: LOOP_CAR
                for Rcar in rightLane:
                    print(Rcar, end='')
                print()

    def UpdateWDebug():
        """
        Menu option which updates the state of the street assuming 30 seconds has passed, and then displays the street and all the cars
        """
        street.update()
        ShowStreet()
        ShowCars()

    def UpdateWODebug():
        """
        Menu option which updates the state of the street assuming 30 seconds has passed
        """
        street.update()

    def Quit():
        """
        Menu Option which Exits the program
        """
        print("")


    menuFunction = {
        1: ShowStreet,
        2: MakeRoad,
        3: AddCar,
        4: ShowCars,
        5: UpdateWODebug,
        6: UpdateWDebug,
        0: Quit,
    }

    return menuFunction[choice]()


def main():
    street = Street()
    choice = 1

    while choice != 0:
        validChoice = False
        while not validChoice:
            menu = Menu("\n"
                        "1) Show Street\n"
                        "2) Make Road\n"
                        "3) Add Car\n"
                        "4) Show Cars\n"
                        "5) Update without Debug Info\n"
                        "6) Update with Debug Info\n"
                        "0) Quit\n")

            menu.printMenu()
            try:
                choice = menu.getMenuOption()
            except ValueError:
                validChoice = False
            else:
                validChoice = True

        result = executeChoice(choice, street)
        if choice == 2:
            street = result
    # add remaining code for main here, you call your class's function that has your menu loop


if __name__ == '__main__':
    main()
