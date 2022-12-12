from datetime import time
import math

# The Hub class keeps track of the unloaded packages, the time, and the Trucks
class Hub:
    def __init__(self):
        # These lists are comprised of the package IDs used to retrieve the hashed package data
        self.__all_packages = []
        self.__loaded = []
        self.__unloaded = []
        self.__same_address_packages = []
        self.__same_address_packages_after_0905 = set()
        self.__trucks = []
        self.__time = 480 

    # Getters
    def get_all_packages(self):
        return self.__all_packages
    def get_loaded(self):
        return self.__loaded
    def get_unloaded(self):
        return self.__unloaded
    def get_same_address_packages(self):
        return self.__same_address_packages
    def get_same_address_packages_after_0905(self):
        return self.__same_address_packages_after_0905
    def get_trucks(self):
        return self.__trucks
    def get_unconverted_time(self):
        return self.__time
    def get_time(self):
        hour = math.floor(self.__time / 60)
        minutes = (self.__time % 60)
        converted_time = time(hour, minutes)
        return converted_time
    # Converts truck mileage into time in format hh:mm:ss
    def get_time_with_mileage(self, mileage_minutes):
        total_time = mileage_minutes + 480
        hour = math.floor(total_time / 60)
        minutes = math.floor(total_time % 60)
        seconds = round(((total_time % 60) % 1) * 60)
        converted_time = time(hour, minutes, seconds)
        return converted_time

    # Setters
    def set_all_packages(self, packages):
        self.__all_packages.append(packages)
    def set_loaded(self, packages):
        self.__loaded.append(packages)
    def set_unloaded(self, packages):
        self.__unloaded.append(packages)
    def set_same_address_packages(self, packages):
        self.__same_address_packages.append(packages)
    # Sets the time to 5:00 PM (end of work day)
    def set_time_to_end_day(self):
        self.__time = 1020


    # Methods
    def add_to_all(self, package):
        self.__all_packages.append(package)
    def remove_from_all(self, package):
        self.__all_packages.remove(package)
    def clear_all(self):
        self.__all_packages.clear()
    
    def add_to_loaded(self, package):
        self.__loaded.append(package)
    def remove_from_loaded(self, package):
        self.__loaded.remove(package)
    def clear_loaded(self):
        self.__loaded.clear()
    
    def add_to_unloaded(self, package):
        self.__unloaded.append(package)
    def remove_from_unloaded(self, package):
        self.__unloaded.remove(package)
    def clear_unloaded(self):
        self.__unloaded.clear()

    def add_to_same_address_packages(self, package):
        self.__same_address_packages.append(package)
    def remove_from_same_address_packages(self, package):
        self.__same_address_packages.remove(package)
    def clear_same_address_packages(self):
        self.__same_address_packages.clear()

    def add_to_same_address_packages_after_0905(self, package):
        self.__same_address_packages_after_0905.add(package)
    def remove_from_same_address_packages_after_0905(self, package):
        self.__same_address_packages_after_0905.remove(package)
    def clear_same_address_packages_after_0905(self):
        self.__same_address_packages_after_0905.clear()

    def add_truck(self, truck):
        self.__trucks.append(truck)
    def remove_truck(self, truck):
        self.__trucks.remove(truck)
    def clear_trucks(self):
        self.__trucks.clear()

    # Prints the information found in the specified package 
    def status_of_one(self, hashtable, key):
        package = hashtable.hash_search(key)
        if (package):
            print("Package ID# " + str(package.get_id()))
            print("Package Delivery Address: " + package.get_address())
            print("Package Deadline: " + package.get_deadline())
            print("Package City: " + package.get_city())
            print("Package Zipcode: " + package.get_zipcode())
            print("Package Weight: " + package.get_weight() + " Kilos")
            print("Package Status: "+ package.get_status())
            print()
        return

    # Prints the status of every package in the hub, and in each truck
    def status_of_all(self, hashtable):
        print(" " * 6, "--STATUS OF ALL PACKAGES--")
        print(" " * 11 + "--as of " + str(self.get_time()) + "--")
        print()
        for key in self.__unloaded:
            package = hashtable.hash_search(key)
            if len(str(package.get_id())) == 1:
                print("At Hub - Package ID# 0" + str(package.get_id()) +
                      " Status: " + package.get_status())
            else:
                print("At Hub - Package ID# " + str(package.get_id()) +
                      " Status: " + package.get_status())
        if self.__unloaded:
            print()
        for truck in self.__trucks:
            truck.status_of_loaded_packages(hashtable)
        return
        
    # Prints the status of all packages in order of package id
    def status_of_ordered_packages(self, hashtable):
        print(" " * 6, "--STATUS OF ALL PACKAGES--")
        print(" " * 11 + "--as of " + str(self.get_time()) + "--")
        print()
        for package_id in self.get_all_packages():
            package = hashtable.hash_search(package_id)
            if len(str(package.get_id())) == 1:
                print("Package ID# 0" + str(package.get_id()) + " Status: " + package.get_status())
            else:
                print("Package ID# " + str(package.get_id()) + " Status: " + package.get_status())
        print()
        return

    # Returns the Mileage of each truck individually and then combined
    def all_truck_mileage(self):
        total_mileage = 0
        for truck in self.__trucks:
            total_mileage += truck.get_mileage()
            print("Mileage for " + truck.get_name() + ": ", round(truck.get_mileage(), 1))
        print("Total mileage for all trucks: ", round(total_mileage, 1))
        print()
        return

    # Allows the Time to proceed by 30 minutes
    def proceed_30_minutes(self):
        if (self.__time + 30 > 1020):
            print("Work Day ends at 17:00 (5:00 PM) Please proceed with a time that ends at or before 17:00")
            return False
        else:
            self.__time += 30
            return True

    # Allows the Time to proceed by 60 minutes
    def proceed_1_hour(self):
        if (self.__time + 60 > 1020):
            print("Work Day ends at 17:00 (5:00 PM) Please proceed with a time that ends at or before 17:00")
            return False
        else:
            self.__time += 60
            return True

    # Allows the Time to proceed by 120 minutes
    def proceed_2_hours(self):
        if (self.__time + 120 > 1020):
             print("Work Day ends at 17:00 (5:00 PM) Please proceed with a time that ends at or before 17:00")
             return False
        else:
            self.__time += 120
            return True
