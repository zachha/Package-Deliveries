# The Package class contains all information pertaining to the package such as address, deadline, zipcode, etc
class Package:
    def __init__(self, id, address, deadline, city, zipcode, weight, status, notes):
        self.__id = int(id)
        self.__address = address
        self.__deadline = deadline
        self.__city = city
        self.__zipcode = zipcode
        self.__weight = weight
        self.__status = status
        self.__notes = notes

    # Getters
    def get_id(self):
        return self.__id
    def get_address(self):
        return self.__address
    def get_deadline(self):
        return self.__deadline
    def get_city(self):
        return self.__city
    def get_zipcode(self):
        return self.__zipcode
    def get_weight(self):
        return self.__weight
    def get_status(self):
        return self.__status
    def get_notes(self):
        return self.__notes

    # Setters
    def set_id(self, id):
        self.__id = id
    def set_address(self, address):
        self.__address = address
    def set_deadline(self, deadline):
        self.__deadline = deadline
    def set_city(self, city):
        self.__city = city
    def set_zipcode(self, zipcode):
        self.__zipcode = zipcode
    def set_weight(self, weight):
        self.__weight = weight
    def set_status(self, status):
        self.__status = status
    def set_notes(self, notes):
        self.__notes = notes