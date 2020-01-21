class Menu:
    def __init__(self, menu):
        self.theMenu = "\n" \
                       "1) Show Street\n" \
                       "2) Make Road\n" \
                       "3) Add Car\n" \
                       "4) Show Cars\n" \
                       "5) Update without Debug Info\n" \
                       "6) Update with Debug Info\n" \
                       "0) Quit\n"

    def printMenu(self):
        print(self.theMenu)

    def getMenuOption(self):
        try:
            choice = input("Choice: ")
            choice = int(choice)
        except:
            print("Invalid Option\n")
            raise ValueError
        return choice
