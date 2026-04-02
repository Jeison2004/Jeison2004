from datetime import datetime

class Storehistory:

    __filename = None
    __Date = None

    # Constructor
    def __init__(self, filename, date=None):
        self.__filename = filename
        self.__Date = date

    # getter
    def get_filename(self):
        return self.__filename

    def get_date(self):
        return self.__Date

    # setter
    def set_filename(self, value):
        self.__filename = value

    def set_date(self, value):
        self.__Date = value

    # save result on the file (AUTO DATE HERE)
    def save_result(self, result_text):
        self.__Date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.__filename, "a") as file:
            file.write(f"[{self.__Date}] {result_text}\n")

    # string
    def __str__(self):
        output = "History File:\n" + \
                 "\tResult is going save in the filename: " + self.__filename + "\n"
        return output