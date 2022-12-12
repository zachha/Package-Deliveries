# Zach Harmon ID#001276942
import csv
import operator
import sys
from graph import Vertex, Graph
from package import Package
from packagegroup import PackageGroup
from truck import Truck
from hub import Hub
from hashtable import HashTable

# Takes the list of new packages from the imported csv and hashes each package into the hashtable then returns the hashtable
def hash_packages(packages_list, hub):
    # Hashtable created with the same number of buckets as initial packages
    package_count = len(packages_list)
    new_hashtable = HashTable(package_count)
    # Each package in the list is hashed into the new hashtable
    for package in packages_list:
        new_hashtable.hash_insert(package)

    # Sorts package list by address to help make creating the same address package list more efficient in the 'load trucks' function
    packages_list.sort(key=operator.methodcaller('get_address'))
    for package in packages_list:
        # Package 9 has the wrong address so it won't be added to the same address package list
        if (package.get_id() != 9):
            hub.add_to_same_address_packages(package.get_id())

    # Hashed data is then cleared from the packages_list so it can't be accessed outside of the hashtable
    packages_list.clear()
    return new_hashtable

# Imports the csv location data file and parses the data, building the location graph
def import_locdata():
    # Initializes the main data list and the Graph
    file_data = []
    new_graph = Graph()

    # Opens the csv and builds the parses the data into the array
    with open("distance_table_formatted.csv", "r") as data_file:
        datareader = csv.reader(data_file, delimiter=',')

        # Reads each row of the csv file and appends it into the data list
        for row in datareader:
            filtered_row = list(filter(None, row))
            file_data.append(filtered_row)
    # Vertices and edges are created to complete the Graph and the graph is then returned
    new_graph.create_vertices(file_data)
    new_graph.create_edges(file_data)
    return new_graph

# Imports the csv package data file and parses the data, building the Package objects and hashing them
def import_packagedata():
    return_list = []
    new_hub = Hub()
    packages_temp = []

    with open("packages_formatted.csv", "r") as package_file:
        datareader = csv.reader(package_file, delimiter=',')

        # Reads and filters each row of the package csv
        for row in datareader:
            filtered_row = list(filter(None, row))
            special_notes = None
            if (len(filtered_row) > 0):

                # If package contains special instructions, this will parse them into a variable, else "none"
                if (len(filtered_row) > 7):
                    special_notes = filtered_row[7]
                else:
                    special_notes = "none"

                # New Package object created from each row of package data imported and then ids are added to the Hub
                new_package = Package(filtered_row[0], filtered_row[1], filtered_row[5], filtered_row[2] +
                                      ", " + filtered_row[3], filtered_row[4], filtered_row[6], "at the hub", special_notes)
                new_hub.add_to_all(new_package.get_id())
                new_hub.add_to_unloaded(new_package.get_id())
                packages_temp.append(new_package)
    # Each package is hashed and added to the hashtable
    new_hashtable = hash_packages(packages_temp, new_hub)
    return_list.append(new_hub)
    return_list.append(new_hashtable)
    return return_list

# Creates a PackageGroup object and fills in the different package sets to be recorded/compared against throughout the program
def create_package_sets(hub, hashtable):
    package_sets = PackageGroup()

    # Appends the package ids that must be stored on truck 2 according to special instructions to the truck 2 only list
    package_sets.add_to_truck_2_only_set(3)
    package_sets.add_to_truck_2_only_set(18)
    package_sets.add_to_truck_2_only_set(36)
    package_sets.add_to_truck_2_only_set(38)

    # Appends package ids to the list that must be picked up after 9:05 according to special instructions
    package_sets.add_to_after_0905_set(6)
    package_sets.add_to_after_0905_set(25)
    package_sets.add_to_after_0905_set(28)
    package_sets.add_to_after_0905_set(32)

    # Appends package ids to the list that must be delivered together according to special instructions
    package_sets.add_to_delivered_together_set(13)
    package_sets.add_to_delivered_together_set(14)
    package_sets.add_to_delivered_together_set(15)
    package_sets.add_to_delivered_together_set(16)
    package_sets.add_to_delivered_together_set(19)
    package_sets.add_to_delivered_together_set(20)

    # Appends package ids to the list that must be delivered by 10:30 am
    for package_id in hub.get_all_packages():
        package = hashtable.hash_search(package_id)
        if package.get_deadline() == "10:30 AM":
            package_sets.add_to_deadline_1030_set(package_id)
        elif package.get_deadline() == "9:00 AM":
            package_sets.add_to_deadline_0900_set(package_id)

    return package_sets

# Sets the status of all loaded packages to "En route"
def package_status_enroute(truck):
    for package_id in truck.get_loaded_packages():
        package = main_hashtable.hash_search(package_id)
        package.set_status("En route")

# This function creates a list of sublists with packages that have matching addresses so packages can be shipped more efficiently
def set_same_address_list(hashtable, hub):
    # Copies the package list that was previously sorted by address and then clears that list from the hub
    sorted_address_temp = hub.get_same_address_packages().copy()
    hub.get_same_address_packages().clear()

    # While loop that continues while there are still packages in the 'sorted address' list to be checked
    while len(sorted_address_temp) > 1:
        same_address = []
        package = hashtable.hash_search(sorted_address_temp[0])

        # Compares first package's address with each successive package until it runs into a different address
        for i in range(1, len(sorted_address_temp)):
            compared_package = hashtable.hash_search(sorted_address_temp[i])
            # Package ids are added to the same address list if the addresses match
            if (package.get_address() == compared_package.get_address()):
                if len(same_address) == 0:
                    same_address.append(package.get_id())
                    same_address.append(compared_package.get_id())
                else:
                    same_address.append(compared_package.get_id())

            # If address is different, the 'same address' list (if not empty) is added to the hub and all packages with the matching address are removed
            # The loop is then started again with a different address if there are any left
            else:
                if (len(same_address) > 0):
                    hub.add_to_same_address_packages(same_address)
                    # Remove all matching packages from the sorted list so the next address can be checked
                    sorted_address_temp = sorted_address_temp[i:]
                    break
                else:
                    # Remove all matching packages from the sorted list so the next address can be checked
                    sorted_address_temp = sorted_address_temp[i:]
                    break
    return

# Checks the same address package list and adds all package_ids that share an address with a 9:05 pickup package
# This logic will later allow the program to package more efficiently, ideally not sending trucks to the same address more than once
def filter_same_address_0905(hub, packagesets):
    # If any of the multiple packages due at an address have to be picked up after 9:05, that address is added to temp_addresses list
    temp_addresses = []
    for address in hub.get_same_address_packages():
        for package_id in address:
            if package_id in packagesets.get_after_0905_set():
                temp_addresses.append(address)
                break
    # Temp addresses list is iterated over and each package is then added to the 'same address packages after 9:05' set in the hub object
    for address in temp_addresses:
        for package_id in address:
            hub.add_to_same_address_packages_after_0905(package_id)
    return

# Compares the input packages with the packages being delivered to the same address. If one matches, all packages going to that address are added to the set
def match_same_address_packages(truck, package_set, hub, is_initial=True):
    matching_addresses = []
    for address in hub.get_same_address_packages():  # O(n)
        for package_id in address:  # O(n)
            # Checks if each package is in the package set and if it should add the 9:05 packages or not
            # Doesn't add the address if its before 9:05 and one of the packages shares an address with a package that needs to be picked up after 9:05
            if package_id in package_set and (package_id not in hub.get_same_address_packages_after_0905() or hub.get_unconverted_time() >= 545):
                address.remove(package_id)
                matching_addresses.append(address)
                break
            else:
                continue

    for address in matching_addresses: 
        # Checks the length to make sure all the packages can fit on the truck
        if (len(truck.get_loaded_packages()) + len(address)) < 17:
            for package_id in address: 
                # Checks if this is an initial same address check, if not then it is adding directly to the trucks and can use the truck/hub methods
                if is_initial:
                    package_set.add(package_id)
                else:
                    truck.add_to_loaded_packages(package_id)
                    truck.add_to_undelivered(package_id)
                    hub.remove_from_unloaded(package_id)
                    hub.add_to_loaded(package_id)
            hub.get_same_address_packages().remove(address)
    return

# Similar to the 'match same address packages' function, except this function isnt comparing to a package set, just loading matching sets
# onto the truck if there is room and all of the packages are at the hub (or its past 9:05 when all late packages arrive at the hub)
def load_same_address_packages(truck, hub, packagesets, temp_addresses=[]):
    # If the 'temp addresses' list is not empty, iterates through the same address packages
    if not len(temp_addresses):
        for address in hub.get_same_address_packages():
            for package_id in address:
                # If none of the packages at a specific address need to be picked up after 9:05 (or it is already past 9:05) adds address to temp addresses
                if (package_id not in hub.get_same_address_packages_after_0905()) or (hub.get_unconverted_time() >= 545):
                    if package_id == address[len(address) - 1]:
                        temp_addresses.append(address)
                else:
                    break

    # Creates a copy of temp_addresses to modify during iteration
    leftover_addresses = temp_addresses.copy()
    for address in temp_addresses:
        address_length = len(address)
        # If the truck can hold all of the packages for a specific address, they are added to the truck
        if (address_length + len(truck.get_loaded_packages())) < 17:
            for package_id in address:
                if package_id in packagesets.get_deadline_1030_copy():
                    truck.add_to_loaded_packages(package_id)
                    truck.add_to_1030_loaded(package_id)
                    truck.add_to_undelivered(package_id)
                    hub.remove_from_unloaded(package_id)
                    hub.add_to_loaded(package_id)
                    packagesets.remove_from_deadline_1030_copy(package_id)
                else:
                    truck.add_to_loaded_packages(package_id)
                    truck.add_to_undelivered(package_id)
                    hub.remove_from_unloaded(package_id)
                    hub.add_to_loaded(package_id)
            leftover_addresses.remove(address)
            hub.get_same_address_packages().remove(address)
        else:
            continue
    # If there are addresses that still have packages (if this truck ran out of room, etc) The other truck can take the list and attempt to load them
    return leftover_addresses

# The initial loading phase for the Trucks, loads the initial packages and checks to see which need to be delivered by 10:30
def initial_load_truck(hub, truck, packages_to_load, packagesets):
    for package in packages_to_load:
        # Adds/removes package to the appropriate object sets
        truck.add_to_loaded_packages(package)
        truck.add_to_undelivered(package)
        hub.remove_from_unloaded(package)
        hub.add_to_loaded(package)

        # If it needs to be delivered by 10:30, will be added to the truck's 10:30 set and removed from the copy 10:30 set
        if package in packagesets.get_deadline_1030_copy():
            truck.add_to_1030_loaded(package)
            packagesets.remove_from_deadline_1030_copy(package)

        # Same for the 9:00 package deadlines
        if package in packagesets.get_deadline_0900_copy():
            truck.add_to_0900_loaded(package)
            packagesets.remove_from_deadline_0900_copy(package)
    return

# After loading all special packages, loads the packages with no special instructions
def load_normal_packages(hub, truck_1, truck_2, packagesets, is_truck1_present=True, is_truck2_present=True):
    temp_packages = []
    for package_id in hub.get_unloaded():
        # Package count for each truck, if present at the hub, is kept in variable to make sure they're loaded evenly and under load
        if is_truck1_present:
            truck_1_count = len(truck_1.get_loaded_packages())
        if is_truck2_present:
            truck_2_count = len(truck_2.get_loaded_packages())

        # Each package is checked to make sure it isn't from the late packages list or sharing an address with a late package
        if (package_id not in packagesets.get_after_0905_set()) and (package_id not in hub.get_same_address_packages_after_0905()):
            # If both trucks are present, fills them evenly until they are fully loaded or all unloaded packages are loaded on the trucks
            if is_truck1_present and is_truck2_present:
                if (truck_1_count <= truck_2_count) and (truck_1_count < 16):
                    truck_1.add_to_loaded_packages(package_id)
                    truck_1.add_to_undelivered(package_id)
                    temp_packages.append(package_id)
                    hub.add_to_loaded(package_id)
                elif (truck_2_count < truck_1_count) and (truck_2_count < 16):
                    truck_2.add_to_loaded_packages(package_id)
                    truck_2.add_to_undelivered(package_id)
                    temp_packages.append(package_id)
                    hub.add_to_loaded(package_id)
            # If only truck 1 is present, fills it until full or all unloaded packages are loaded on the trucks
            elif is_truck1_present and not is_truck2_present:
                if truck_1_count < 16:
                    truck_1.add_to_loaded_packages(package_id)
                    truck_1.add_to_undelivered(package_id)
                    temp_packages.append(package_id)
                    hub.add_to_loaded(package_id)
            # If only truck 2 is present, fills it until full or all unloaded packages are loaded on the trucks
            elif is_truck2_present and not is_truck1_present:
                if truck_2_count < 16:
                    truck_2.add_to_loaded_packages(package_id)
                    truck_2.add_to_undelivered(package_id)
                    temp_packages.append(package_id)
                    hub.add_to_loaded(package_id)

    # Loaded packages are removed from the hub's 'unloaded' list after the iteration is done
    for package_id in temp_packages:
        hub.remove_from_unloaded(package_id)
    return

# Completes the initial loading of both Trucks and sets Status of all loaded packages to 'En route'
def finish_initial_loading(hub, truck_1, truck_2, packagesets):
    # Creates a set of deadline 10:30 packages to remove after this loop
    deadline_1030_to_remove = set()
    for package_id in packagesets.get_deadline_1030_copy():
        # Counts are kept in variables to check truck sizes and amounts of 10:30 deadline packages to keep them even and under load
        truck_1_1030_count = len(truck_1.get_deadline_1030_loaded())
        truck_2_1030_count = len(truck_2.get_deadline_1030_loaded())
        truck_1_package_count = len(truck_1.get_loaded_packages())
        truck_2_package_count = len(truck_2.get_loaded_packages())
        # Some packages have to be picked up from the hub after 9:05 AM, they can't be loaded initially so this must be checked for
        if (package_id in packagesets.get_after_0905_set()) or (package_id in hub.get_same_address_packages_after_0905()):
            continue
        else:
            # Fills up the trucks evenly so that they both can deliver the packages due at 10:30 more efficiently
            if (truck_1_1030_count <= truck_2_1030_count) and (truck_1_package_count < 16):
                truck_1.add_to_undelivered(package_id)
                truck_1.add_to_loaded_packages(package_id)
                truck_1.add_to_1030_loaded(package_id)
                hub.remove_from_unloaded(package_id)
                hub.add_to_loaded(package_id)
                deadline_1030_to_remove.add(package_id)
            elif (truck_2_1030_count < truck_1_1030_count) and (truck_2_package_count < 16):
                truck_2.add_to_undelivered(package_id)
                truck_2.add_to_loaded_packages(package_id)
                truck_2.add_to_1030_loaded(package_id)
                hub.remove_from_unloaded(package_id)
                hub.add_to_loaded(package_id)
                deadline_1030_to_remove.add(package_id)
            else:
                print("Error: Trucks are full please deliver some packages before attempting to add any more.")
                print()
    # Each deadline 10:30 package that was loaded is then removed from the appropriate package set so that the hub can keep track of which ones have yet
    # to be loaded
    for package_id in deadline_1030_to_remove:
        if package_id in packagesets.get_deadline_1030_copy():
            packagesets.remove_from_deadline_1030_copy(package_id)

    # Then checks to see if any of the newly added packages have packages with matching addresses and adds them if possible
    match_same_address_packages(
        truck_1, truck_1.get_loaded_packages(), hub, False)
    match_same_address_packages(
        truck_2, truck_2.get_loaded_packages(), hub, False)

    # Adds the remaining groups of same-address packages if they will fit on the trucks
    leftover_temp_addresses = load_same_address_packages(truck_1, hub, packagesets)
    if leftover_temp_addresses:
        load_same_address_packages(truck_2, hub, packagesets, leftover_temp_addresses)

    # Fills the rest of the truck space with normal packages
    load_normal_packages(hub, truck_1, truck_2, packagesets)
    return

# Creates the Truck objects, creates package sets used for sorting packages, and begins loading packages into the Trucks
def prepare_trucks(hashtable, hub):
    # Creates the Truck objects and appends them to the trucks list and then creates a PackageGroup object
    truck_1 = Truck("Truck 1", address_graph.vertices[0])
    truck_2 = Truck("Truck 2", address_graph.vertices[0])
    hub.add_truck(truck_1)
    hub.add_truck(truck_2)

    # PackageGroup object is created and sets are filled with the various types of packages
    package_sets = create_package_sets(hub, hashtable)

    # Searches the hashtable for which packages are being delivered to the same address and appends each sublist to the list in the hub
    set_same_address_list(hashtable, hub)
    filter_same_address_0905(hub, package_sets)

    # Checks the parameter set of packages to see if there are any addresses that have multiple deliveries, if so they are added to the set
    match_same_address_packages(truck_1, package_sets.get_delivered_together_set(), hub)
    match_same_address_packages(truck_2, package_sets.get_truck_2_only_set(), hub)

    # 10:30 and 9:00 deadline sets have copies created so that modifications can be done to the copy while still having access to the unmodified list if needed
    package_sets.set_1030_copy()
    package_sets.set_0900_copy()

    # Initial loading fills up both trucks by loading the appropriate sets to each truck
    initial_load_truck(hub, truck_1, package_sets.get_delivered_together_set(), package_sets)
    initial_load_truck(hub, truck_2, package_sets.get_truck_2_only_set(), package_sets)

    # Initial loading is then finished by adding all of the remaining 10:30 deadline packages to each truck evenly, checking for matching address packages,
    # adding all possible remaining sets of same-address packages, then filling the rest of the trucks with normal packages
    finish_initial_loading(hub, truck_1, truck_2, package_sets)
    return package_sets

# Loads all remaining packages onto Truck after 9:05 AM if there is enough space
def after_0905_load_remaining(truck, distance):
    # If there are no more packages to load, this Truck is finished for the day
    if not len(main_hub.get_unloaded()):
        print(truck.get_name() + " has finished delivering all packages!")
        print()
    # Else if the Truck has spaces for the remaining 8 packages, it will laod them all
    elif len(truck.get_loaded_packages()) < 9:
        print(truck.get_name() + " has returned to the hub to load more packages")
        print()
        deadline_1030_temp = set()
        hub_temp = set()
        # Loads each package from the main hub into the truck and adds/removes from the appropriate sets and lists
        for package_id in main_hub.get_unloaded():
            truck.add_to_loaded_packages(package_id)
            truck.add_to_undelivered(package_id)
            hub_temp.add(package_id)
            main_hub.add_to_loaded(package_id)
            if package_id in main_package_sets.get_deadline_1030_copy():
                deadline_1030_temp.add(package_id)
                truck.add_to_1030_loaded(package_id)
        # Iterates through the temp deadline set and removes each package_id from the deadline 10:30 copy set
        for package_id in hub_temp:
            main_hub.remove_from_unloaded(package_id)
        for package_id in deadline_1030_temp:
            main_package_sets.remove_from_deadline_1030_copy(package_id)
    return

# Begins delivering packages from both trucks, increments time based on user input
def start_delivering(input_time_increment):
    truck_1 = main_hub.get_trucks()[0]
    truck_2 = main_hub.get_trucks()[1]

    if input_time_increment == "full":
        time_increment = 540
    else:
        time_increment = input_time_increment

    # While loop continues while at least one Truck is able to get to it's next destination before the new calculated time
    while True:
        
        # truck_1_distance = address_graph.edge_weights[(truck_1.get_location(), truck_1.get_destination())]
        truck_1_distance = truck_1.get_destination_distance()
        truck_1_new_mileage = truck_1.get_mileage() + float(truck_1_distance)
        truck_1_calc_time = truck_1.mileage_into_minutes(truck_1_new_mileage) + 480
        # truck_2_distance = address_graph.edge_weights[(truck_2.get_location(), truck_2.get_destination())]
        truck_2_distance = truck_2.get_destination_distance()
        truck_2_new_mileage = truck_2.get_mileage() + float(truck_2_distance)
        truck_2_calc_time = truck_2.mileage_into_minutes(truck_2_new_mileage) + 480
       
        # If both Trucks are done delivering, stops the loop and prints out a message saying deliveries are done and the Time
        if truck_1.get_is_done_delivering() and truck_2.get_is_done_delivering():
            print(" " * 6, "--ALL PACKAGES HAVE BEEN DELIVERED!--")

            # Finds time from the mileage of the last used Truck 
            if truck_1.get_mileage() >= truck_2.get_mileage():
                print(" " * 12, "--Finished at " + str(main_hub.get_time_with_mileage(truck_1.mileage_into_minutes(truck_1.get_mileage()))) + "--")
            else:
                print(" " * 12, "--Finished at " + str(main_hub.get_time_with_mileage(truck_2.mileage_into_minutes(truck_2.get_mileage()))) + "--")
            print()
            break

        # If the mileage of both truck's next delivery would take them past the time increment, the while loop ends since no more deliveries can be made
        if (not truck_1_calc_time <= (main_hub.get_unconverted_time() + time_increment)) and (not truck_2_calc_time <= (main_hub.get_unconverted_time() + time_increment)):
            break

        # If the mileage of Truck 1's next delivery would be past the time increment and Truck 2 is done delivering, no more deliveries can be made this increment
        elif (not truck_1_calc_time <= (main_hub.get_unconverted_time() + time_increment)) and truck_2.get_is_done_delivering():
            break

        # If the mileage of Truck 1\2's next delivery would be past the time increment and Truck 1 is done delivering, no more deliveries can be made this increment
        elif truck_1.get_is_done_delivering() and (not truck_2_calc_time <= (main_hub.get_unconverted_time() + time_increment)):
            break

        else:
            # Checks if Truck 1's delivery would occur first and then if Truck 2 is done delivering but not Truck 1
            if (truck_1_new_mileage <= truck_2_new_mileage) or ((not truck_1.get_is_done_delivering()) and (truck_2.get_is_done_delivering())):
                # Checks to see if the truck is returning to the hub for more packages
                if truck_1.get_destination() == address_graph.vertices[0]:
                    # pops delivery list, adds mileage, and changes location to new location
                    truck_1.pop_front_delivery_queue()
                    truck_1.add_to_mileage(float(truck_1_distance), main_hashtable, address_graph)
                    truck_1.change_location(truck_1.get_destination())
                    truck_1.change_destination(None)

                    # Loads remaining packages onto truck if there is space
                    after_0905_load_remaining(truck_1, float(truck_1_distance))

                    # Fills the loade d vertices set with all loaded package locations then runs Dijkstra's algorithm for next shortest destination
                    truck_1.fill_loaded_vertices(address_graph, main_hashtable)
                    address_graph.run_shortest_path_algo(truck_1, main_hashtable, main_hub, truck_1_calc_time)
                    continue
                # Else, truck continues to the destination vertex and delivers all appropriate packages, then runs Dijkstra's algorithm for next shortest destination
                else:
                    truck_1.deliver_packages(address_graph, main_hub, main_hashtable)
                    address_graph.run_shortest_path_algo(truck_1, main_hashtable, main_hub, truck_1_calc_time)
                    continue
            # Checks if Truck 2's delivery would occur first and then if Truck 1 is done delivering but not Truck 2
            elif truck_2_new_mileage < truck_1_new_mileage or ((not truck_2.get_is_done_delivering()) and (truck_1.get_is_done_delivering())):
                # Checks to see if the truck is returning to the hub for more packages
                if truck_2.get_destination() == address_graph.vertices[0]:
                    truck_2.pop_front_delivery_queue()
                    truck_2.add_to_mileage(float(truck_2_distance), main_hashtable, address_graph)
                    truck_2.change_location(truck_2.get_destination())
                    truck_2.change_destination(None)

                    # Loads remaining packages onto truck if there is space
                    after_0905_load_remaining(truck_2, float(truck_2_distance))

                    # Fills the loade d vertices set with all loaded package locations then runs Dijkstra's algorithm for next shortest destination
                    truck_2.fill_loaded_vertices(address_graph, main_hashtable)
                    address_graph.run_shortest_path_algo(truck_2, main_hashtable, main_hub, truck_2_calc_time)
                    continue
                # Else, truck continues to the destination vertex and delivers all appropriate packages, then runs Dijkstra's algorithm for next shortest destination
                else:
                    truck_2.deliver_packages(address_graph, main_hub, main_hashtable)
                    address_graph.run_shortest_path_algo(truck_2, main_hashtable, main_hub, truck_2_calc_time)
                    continue
    # Increases time based on the input increment
    if time_increment == 30:
        if main_hub.proceed_30_minutes():
            print(" " * 4 + "--Packages delivered up to " + str(main_hub.get_time()) + "--")
            print()
            return
    elif time_increment == 60:
        if main_hub.proceed_1_hour():
            print(" " * 4 + "--Packages delivered up to " + str(main_hub.get_time()) + "--")
            print()
            return
    elif time_increment == 120:
        if main_hub.proceed_2_hours():
            print(" " * 4 + "--Packages delivered up to " + str(main_hub.get_time()) + "--")
            print()
            return
    else:
        main_hub.set_time_to_end_day()
    return

# Gets package location vertices for all Trucks and runs Djikstra's algorithm to find the shortest location to deliver for each
def get_starting_locations():
    for truck in main_hub.get_trucks():
        truck.fill_loaded_vertices(address_graph, main_hashtable)
        truck_temp_time = 480
        address_graph.run_shortest_path_algo(truck, main_hashtable, main_hub, truck_temp_time)
        # Changes status of all truck packages to 'en route' as they prepare to start delivering
        package_status_enroute(truck)
    return

# Allows the user to progress the time by 30/60/120 minute increments or to run through the whole program until all packages are delivered
# Also allows user to get all info about any individual package or the status of all packages in order of ID
def get_user_input():
    print("To progress time thirty minutes, type 'thirty' then hit enter")
    print("To progress time an hour, type 'hour' then hit enter")
    print("To progress time two hours, type 'hours' then hit enter")
    print("To progress time until all packages are delivered, type 'completion' then hit enter")
    print("To get the mileage of each truck and the total mileage, type 'miles' then hit enter")
    print("To get all package information for a specific package, type a package ID number (0 - 40) then hit enter")
    print("To get the status of all packages in order of ID, type 'status' then hit enter")
    print("To exit the program, type 'exit' then")
    print()
    user_input = input()

    if user_input == 'thirty':
        print()
        print("Progresing time by thirty minutes")
        print()
        start_delivering(30)
        get_user_input()
    elif user_input == 'hour':
        print()
        print("Progressing time by one hour")
        print()
        start_delivering(60)
        get_user_input()
    elif user_input == 'hours':
        print()
        print("Progressing time by two hours")
        print()
        start_delivering(120)
        get_user_input()
    elif user_input == 'completion':
        print()
        print("Progressing time until end of day")
        print()
        temp_mins = 1020 - main_hub.get_unconverted_time()
        start_delivering(temp_mins)
        main_hub.all_truck_mileage()
        main_hub.status_of_all(main_hashtable)
        get_user_input()
    elif user_input == 'miles':
        print()
        main_hub.all_truck_mileage()
        get_user_input()
    elif user_input == 'status':
        print()
        main_hub.status_of_ordered_packages(main_hashtable)
        get_user_input()
    elif user_input == 'exit':
        print()
        sys.exit("Exiting Program")
    else:
        package = main_hashtable.hash_search(int(user_input))
        if package:
            print()
            main_hub.status_of_one(main_hashtable, int(user_input))
            get_user_input()
        else:
            print("User Input Error: Please enter one of the listed commands or a package ID")
            print()
            get_user_input()
    return

print()
address_graph = import_locdata()
main_list = import_packagedata()
main_hub = main_list[0]
main_hashtable = main_list[1]
main_package_sets = prepare_trucks(main_hashtable, main_hub)
main_hub.status_of_all(main_hashtable)
get_starting_locations()
print(" --TRUCKS NOW LEAVING FOR DELIVERY AT 08:00:00--")
print()
get_user_input()



