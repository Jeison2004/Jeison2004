class Num:

    # Creates a class that stores in GUI
    entryNum1 = None
    __labelResult = None
    __entryNum3 = None
    __entryNum2 = None
    __entryNum1 = None

    # init / Constructor method
    # These are private attributes (only used inside the class)
    # They are meant to store the Entry and Label widgets

    def __init__(self, entrynum1, entrynum2, entrynum3,labelresult):
        self.__entryNum1 = entrynum1
        self.__entryNum2 = entrynum2
        self.__entryNum3 = entrynum3
        self.__labelResult = labelresult

    # getters
    def get_entrynum1(self):
        return self.__entryNum1

    def get_entrynum2(self):
        return self.__entryNum2

    def get_entrynum3(self):
        return self.__entryNum3

    def get_labelresult(self):
        return self.__labelResult

    # setters
    def set_entrynum1(self, entrynum1):
        self.__entryNum1 = entrynum1

    def set_entrynum2(self, entrynum2):
        self.__entryNum2 = entrynum2

    def set_entrynum3(self, entrynum3):
        self.__entryNum3 = entrynum3

    # ADDED
    def set_labelresult(self, labelresult):
        self.__labelResult = labelresult

    # string
    def __str__(self):
        output = "Calculator:\n" + \
                 "\tNumber 1/Numero 1: " + self.__entryNum1.get() + "\n" + \
                 "\tNumber 2/Numero 2: " + self.__entryNum2.get() + "\n" + \
                 "\tNumber 3/Numero 3: " + self.__entryNum3.get() + "\n" + \
                 "\tResult/Resultado: " + self.__labelResult.cget("text") + "\n"
        return output

