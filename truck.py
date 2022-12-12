import math

# Truck class that keeps track of loaded packages, locations, and mileage
class Truck:
    def __init__(self, name, location):
        self.__name = name
        self.__delivery_queue = []
        self.__loaded_packages = set()
        self.__undelivered = set()
        self.__delivered = set()
        self.__deadline_0900_loaded = set()
        self.__deadline_1030_loaded = set()
        self.__loaded_0900_vertices_set = set()
        self.__loaded_1030_vertices_set = set()
        self.__loaded_eod_vertices_set = set()
        self.__location = location
        self.__destination = None
        self.__destination_distance = 0
        self.__is_going_to_hub = False
        self.__is_done_delivering = False
        self.__mileage = 0
        self.__mph = 18

    # Getters
    def get_name(self):
        return self.__name
    def get_delivery_queue(self):
        return self.__delivery_queue
    def get_loaded_packages(self):
        return self.__loaded_packages
    def get_undelivered(self):
        return self.__undelivered
    def get_delivered(self):
        return self.__delivered
    def get_deadline_0900_loaded(self):
        return self.__deadline_0900_loaded
    def get_deadline_1030_loaded(self):
        return self.__deadline_1030_loaded
    def get_loaded_0900_vertices_set(self):
        return self.__loaded_0900_vertices_set
    def get_loaded_1030_vertices_set(self):
        return self.__loaded_1030_vertices_set
    def get_loaded_eod_vertices_set(self):
        return self.__loaded_eod_vertices_set
    def get_location(self):
        return self.__location
    def get_destination(self):
        return self.__destination
    def get_destination_distance(self):
        return self.__destination_distance
    def get_is_going_to_hub(self):
        return self.__is_going_to_hub
    def get_is_done_delivering(self):
        return self.__is_done_delivering
    def get_mileage(self):
        return self.__mileage
    def get_mph(self):
        return self.__mph

    # Methods
    def add_to_delivery_queue(self, package):
        self.__delivery_queue.append(package)
    def remove_from_delivery_queue(self, package):
        self.__delivery_queue.remove(package)
    def pop_front_delivery_queue(self):
        self.__delivery_queue.pop(0)
    def clear_delivery_queue(self):
        self.__delivery_queue.clear()

    def add_to_loaded_packages(self, package):
        self.__loaded_packages.add(package)
    def remove_from_loaded_packages(self, package):
        self.__loaded_packages.remove(package)
    def clear_loaded(self):
        self.__loaded_packages.clear()

    def add_to_undelivered(self, package):
        self.__undelivered.add(package)
    def remove_from_undelivered(self, package):
        self.__undelivered.remove(package)
    def clear_undelivered(self):
        self.__undelivered.clear()

    def add_to_delivered(self, package):
        self.__delivered.add(package)
    def remove_from_delivered(self, package):
        self.__delivered.remove(package)
    def clear_delivered(self):
        self.__delivered.clear()

    def add_to_0900_loaded(self, package):
        self.__deadline_0900_loaded.add(package)
    def remove_from_0900_loaded(self, package):
        self.__deadline_0900_loaded.remove(package)
    def clear_0900_loaded(self):
        self.__deadline_0900_loaded.clear()

    def add_to_1030_loaded(self, package):
        self.__deadline_1030_loaded.add(package)
    def remove_from_1030_loaded(self, package):
        self.__deadline_1030_loaded.remove(package)
    def clear_1030_loaded(self):
        self.__deadline_1030_loaded.clear()

    def add_to_loaded_0900_vertices_set(self, vertex):
        self.__loaded_0900_vertices_set.add(vertex)
    def remove_from_loaded_0900_vertices_set(self, vertex):
        self.__loaded_0900_vertices_set.remove(vertex)
    def clear_loaded_0900_vertices_set(self):
        self.__loaded_0900_vertices_set.clear()

    def add_to_loaded_1030_vertices_set(self, vertex):
        self.__loaded_1030_vertices_set.add(vertex)
    def remove_from_loaded_1030_vertices_set(self, vertex):
        self.__loaded_1030_vertices_set.remove(vertex)
    def clear_loaded_1030_vertices_set(self):
        self.__loaded_1030_vertices_set.clear()

    def add_to_loaded_eod_vertices_set(self, vertex):
        self.__loaded_eod_vertices_set.add(vertex)
    def remove_from_loaded_eod_vertices_set(self, vertex):
        self.__loaded_eod_vertices_set.remove(vertex)
    def clear_loaded_eod_vertices_set(self):
        self.__loaded_eod_vertices_set.clear()

    # Converts the total mileage of a truck into minutes passed since 8:00 AM
    def mileage_into_minutes(self, new_mileage):
        return (new_mileage / self.__mph) * 60

    def change_location(self, location_vertex):
        self.__location = location_vertex

    def change_destination(self, destination_vertex):
        self.__destination = destination_vertex

    def change_destination_distance(self, destination_distance):
        self.__destination_distance = destination_distance
    
    # Switches the is_going_to_hub attribute from True to False or vice verse
    def change_is_going_to_hub(self):
        if self.__is_going_to_hub:
            self.__is_going_to_hub = False
        if not self.__is_going_to_hub:
            self.__is_going_to_hub = True
    # Switches the is_done_delivering attribute from True to False or vice versa
    def change_is_done_delivering(self):
        if self.__is_done_delivering:
            self.__is_done_delivering = False
        if not self.__is_done_delivering:
            self.__is_done_delivering = True

    # Adds miles to a Truck's mileage and checks to see if enough time has passed for package 9 to get it's corrected address
    def add_to_mileage(self, miles, hashtable, graph):
        if 9 in self.__loaded_packages:
            # If mileage brings the Truck past 10:20, package 9 is updated
            if (self.__mileage < 42.0) and (self.__mileage + miles >= 42.0):
                package = hashtable.hash_search(9)
                package.set_address("410 S State St")
                package.set_zipcode("84111")
                print("Package #", package.get_id(), "had incorrect address corrected to: ", package.get_address(), package.get_zipcode())
                print()
                # Truck needs to add the location vertex from package 9 into the laoded package vertices set
                self.fill_loaded_vertices(graph, hashtable)
        self.__mileage += miles

    # Prints the status of each package= that has been loaded onto the Truck Object
    def status_of_loaded_packages(self, hashtable):
        for package_id in self.__loaded_packages:
            package = hashtable.hash_search(package_id)
            if len(str(package.get_id())) == 1:
                print("On " + self.__name + " - " + "Package ID# 0" +str(package.get_id()) + " Status: " + package.get_status())
            else:
                print("On " + self.__name + " - " + "Package ID# " +str(package.get_id()) + " Status: " + package.get_status())
        if self.__loaded_packages:
            print()
        for package_id in self.__delivered:
            package = hashtable.hash_search(package_id)
            if len(str(package.get_id())) == 1:
                print("Delivered by " + self.__name + " - " + "Package ID# 0" +str(package.get_id()) + " Status: " + package.get_status())
            else:
                print("Delivered by " + self.__name + " - " + "Package ID# " +str(package.get_id()) + " Status: " + package.get_status())
        if self.__delivered:
            print()
        return

    # Fills the Truck's loaded vertices set with the location vertices to be visited so they can later be sorted by distance
    def fill_loaded_vertices(self, graph, hashtable):
        # Iterate through the Truck's deadline 9:00 AM packages and add their vertices to the laoded vertices set
        for package_id in self.get_deadline_0900_loaded(): 
            package = hashtable.hash_search(package_id)
            for vertex in graph.vertices: 
                if package.get_address() == vertex.address:
                    self.add_to_loaded_0900_vertices_set(vertex)
        # Iterate through the Truck's deadline 10:30 AM packages and add their vertices to the laoded vertices set
        for package_id in self.get_deadline_1030_loaded():  
            package = hashtable.hash_search(package_id)
            for vertex in graph.vertices: 
                if package.get_address() == vertex.address:
                    self.add_to_loaded_1030_vertices_set(vertex)
        # Second time will load every package vertex into the Truck's loaded vertices set
        for package_id in self.get_loaded_packages():  
            package = hashtable.hash_search(package_id)
            for vertex in graph.vertices: 
                if package.get_address() == vertex.address:
                    self.add_to_loaded_eod_vertices_set(vertex)

    # If the truck can get to the new destination in the alotted time, it does so and delivers all packages matching the destination address
    def deliver_packages(self, graph, hub, hashtable):

        # Truck proceeds to destination, adding to mileage and changing its location
        self.add_to_mileage(float(self.__destination_distance), hashtable, graph)
        self.change_location(self.__destination)

        # Removes the destination vertex from the appropriate set 
        if self.__destination in self.get_loaded_0900_vertices_set():
            self.remove_from_loaded_0900_vertices_set(self.__destination)
        if self.__destination in self.get_loaded_1030_vertices_set():
            self.remove_from_loaded_1030_vertices_set(self.__destination)
        if self.__destination in self.get_loaded_eod_vertices_set():
            self.remove_from_loaded_eod_vertices_set(self.__destination)

        undelivered_temp = set()
        # Iterates through each undelivered package on the truck and delivers them if they have a matching address
        for package_id in self.get_undelivered():
            package = hashtable.hash_search(package_id)
            if package.get_address() == self.__destination.address:
                delivery_string = "Delivered at " + str(hub.get_time_with_mileage(self.mileage_into_minutes(self.__mileage)))
                package.set_status(delivery_string)
                if len(str(package.get_id())) == 1:
                    print("Package # 0" + str(package.get_id()) + " Delivered by", self.__name, "at:", hub.get_time_with_mileage(self.mileage_into_minutes(self.__mileage)))
                else:
                    print("Package #", package.get_id(), "Delivered by", self.__name, "at:", hub.get_time_with_mileage(self.mileage_into_minutes(self.__mileage)))
                undelivered_temp.add(package_id)
                self.remove_from_loaded_packages(package_id)
                self.add_to_delivered(package_id)
                if package_id in self.__deadline_0900_loaded:
                    self.remove_from_0900_loaded(package_id)
                if package_id in self.__deadline_1030_loaded:
                    self.remove_from_1030_loaded(package_id)
        print()
        # Iterates through the undelivered temp set and removes each package from the Truck's undelivered set
        for package_id in undelivered_temp:
            self.remove_from_undelivered(package_id)
    
        # Pops the current address off the delivery list so the next address can be placed in front
        self.pop_front_delivery_queue()
        return 

