# The PackageGroup class helps keep track of several package id sets used to sort and load the packages onto the Trucks
class PackageGroup:
    def __init__(self):
        self.__truck_2_only_set = set()
        self.__after_0905_set = set()
        self.__delivered_together_set = set()
        self.__deadline_1030_set = set()
        self.__deadline_0900_set = set()
        self.__deadline_1030_copy = set()
        self.__deadline_0900_copy = set()

    # Getters
    def get_truck_2_only_set(self):
        return self.__truck_2_only_set
    def get_after_0905_set(self):
        return self.__after_0905_set
    def get_delivered_together_set(self):
        return self.__delivered_together_set
    def get_deadline_1030_set(self):
        return self.__deadline_1030_set
    def get_deadline_0900_set(self):
        return self.__deadline_0900_set
    def get_deadline_1030_copy(self):
        return self.__deadline_1030_copy
    def get_deadline_0900_copy(self):
        return self.__deadline_0900_copy

    # Setters
    def set_1030_copy(self):
        self.__deadline_1030_copy = self.__deadline_1030_set
    def set_0900_copy(self):
        self.__deadline_0900_copy = self.__deadline_0900_set

    # Methods
    def add_to_truck_2_only_set(self, package):
        self.__truck_2_only_set.add(package)
    def remove_from_truck_2_only_set(self, package):
        self.__truck_2_only_set.remove(package)
    def clear_truck_2_only_set(self):
        self.__truck_2_only_set.clear()

    def add_to_after_0905_set(self, package):
        self.__after_0905_set.add(package)
    def remove_from_after_0905_set(self, package):
        self.__after_0905_set.remove(package)
    def clear_after_0905_set(self):
        self.__after_0905_set.clear()

    def add_to_delivered_together_set(self, package):
        self.__delivered_together_set.add(package)
    def remove_from_delivered_together_set(self, package):
        self.__delivered_together_set.remove(package)
    def clear_delivered_together_set(self):
        self.__delivered_together_set.clear()

    def add_to_deadline_1030_set(self, package):
        self.__deadline_1030_set.add(package)
    def remove_from_deadline_1030_set(self, package):
        self.__deadline_1030_set.remove(package)
    def clear_deadline_1030_set(self):
        self.__deadline_1030_set.clear()

    def add_to_deadline_0900_set(self, package):
        self.__deadline_0900_set.add(package)
    def remove_from_deadlie_0900_set(self, package):
        self.__deadline_0900_set.remove(package)
    def clear_deadline_0900_set(self):
        self.__deadline_0900_set.clear()

    def add_to_deadline_1030_copy(self, package):
        self.__deadline_1030_copy.add(package)
    def remove_from_deadline_1030_copy(self, package):
        self.__deadline_1030_copy.remove(package)
    def clear_deadline_1030_copy(self):
        self.__deadline_1030_copy.clear()

    def add_to_deadline_0900_copy(self, package):
        self.__deadline_0900_copy.add(package)
    def remove_from_deadline_0900_copy(self, package):
        self.__deadline_0900_copy.remove(package)
    def clear_deadline_0900_copy(self):
        self.__deadline_0900_copy.clear()
