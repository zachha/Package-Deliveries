from queue import PriorityQueue
import operator

# The Vertex class represents each location node in the Graph class where packages need to be delivered
class Vertex:
    def __init__(self, title, address, zipcode):
        self.title = title
        self.address = address
        self.zipcode = zipcode
        # distance and previous vertex are used in Dijkstra's algorithm
        self.distance = float('inf')
        self.previous_vertex = None

# The Graph class allows the connection of all connected vertices and keeps track of edge weights and djikstra's algorithm
class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}
        self.vertices = []
        
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []
        
    def add_directed_edge(self, from_vertex, to_vertex, weight=1):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        if to_vertex not in self.adjacency_list[from_vertex]:
            self.adjacency_list[from_vertex].append(to_vertex)
        
    def add_undirected_edge(self, vertex_a, vertex_b, weight=1):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    # Loops through the first list element, which is the addresses, and creates a Vertex for each location, adding each to new_graph
    def create_vertices(self, file_data):
        for i in range(len(file_data[0])):
            for element in file_data[0][i]:
                if (element.isdigit()):
                    # Elements indices are found to help slice the full address into chunks
                    address_start = file_data[0][i].find(element)
                    address_end = file_data[0][i].find("(")
                    zipcode_end = file_data[0][i].find(")")

                    # Full address is sliced using the found indices into title, address, and zipcode
                    title_slice = slice(0, (address_start - 1))
                    address_slice = slice(address_start, (address_end - 1))
                    zipcode_slice = slice(address_end + 1, zipcode_end)
                    title = file_data[0][i][title_slice]
                    address = file_data[0][i][address_slice]
                    zipcode = file_data[0][i][zipcode_slice]

                    # Vertices are then created and added to new_graph
                    new_vertex = None
                    new_vertex = Vertex(title, address, zipcode)
                    self.add_vertex(new_vertex)
                    self.vertices.append(new_vertex)
                    break
        return

    # Loops through each of the distance list elements, which will then be used to build the edge-weights of the graph
    def create_edges(self, file_data):
        for i in range(1, len(file_data[0]) + 1):
            start_vertex = self.vertices[i - 1]
            for j in range(1, len(file_data[i])):
                if (file_data[i][j] == "0"):
                    break
                else:
                    end_vertex = self.vertices[j - 1]
                    self.add_undirected_edge(start_vertex, end_vertex, file_data[i][j])
                    continue
        return

    # I incorporated a Priority Queue into Dijkstra's Shortest Path algorithm to increase the efficiency a bit
    def dijkstra_algorithm(self, location_vertex, truck):
        # Priority Queue is created using a max size equal to the number of locations in the graph
        unvisited_queue = PriorityQueue(maxsize = len(self.vertices))

        counter = 1
        # Adds each vertex into the Priority Queue
        # This part of the algo is O (n log n)
        for vertex in self.adjacency_list:
            # resets attributes so that the calculations don't get messed up after more than one run of the algorithm
            vertex.previous_vertex = None
            vertex.distance = float('inf')
            unvisited_queue.put((vertex.distance, counter, vertex)) 
            counter += 1

        location_vertex.distance = 0

        # Loops while the Priority Queue isn't empty, checks the distances of each path and finds the shortest distance
        # This part of the algo is O(n log n) + O(n ^ 2)
        while not unvisited_queue.empty(): 

            # Each vertex in the Priority Queue is retrieved 
            dist, count, current_vertex = unvisited_queue.get(vertex) 

            # Distances are checked from each potential pathway
            for adj_vertex in self.adjacency_list[current_vertex]: 
                distance = self.edge_weights[(current_vertex, adj_vertex)] 
                alt_distance = current_vertex.distance + float(distance)
                # Checks for shorter path and updates if appropriate
                if alt_distance < adj_vertex.distance:
                    adj_vertex.distance = alt_distance
                    adj_vertex.previous_vertex = current_vertex
        return
    
    # Method checks to see if Truck needs to return to the Hub, if not it runs Dijkstra's algorithm to calculate next address
    def run_shortest_path_algo(self, truck, hashtable, hub, truck_calc_time):
        
        # Checks to see if any other Trucks are already heading to the Hub to pickup more packages 
        # This prevents multiple Trucks from going to pickup packages when only 1 needs to
        hub_pickup_already_occuring = False
        for t in hub.get_trucks():
            if t.get_is_going_to_hub():
                hub_pickup_already_occuring = True

        # If the main hub has undelivered packages, the truck has at least 8 free spots, and its past 9:05, the truck goes to the hub to pick up more packages
        if (hub.get_unloaded()) and (len(truck.get_loaded_packages()) < 9) and (truck_calc_time >= 545) and (not hub_pickup_already_occuring):
            truck.add_to_delivery_queue(self.vertices[0])
            truck.change_destination(self.vertices[0])
            truck.change_is_going_to_hub()

        # Else if the truck is out of packages and there are none to pick up, it returns to the Hub
        elif not truck.get_loaded_packages():
            truck.add_to_delivery_queue(self.vertices[0])
            truck.change_destination(self.vertices[0])
            truck.change_is_done_delivering()
            print(truck.get_name() + " has finished delivering all packages!")
            print()

        # Dijkstra's algorithm runs to find the shortest distances to each vertex from the location in the parameter
        self.dijkstra_algorithm(truck.get_location(), truck)  # O(n log n)

        # If going to hub, skips the sort and sets destination attributes to the hub
        if truck.get_destination() == self.vertices[0]:
            truck.change_destination_distance(self.vertices[0].distance)
            return

        # Sort 9:00 AM deadline packages if there are any, then 10:30 deadline, then End of Day packages
        elif truck.get_loaded_0900_vertices_set():
            vertices_to_sort = truck.get_loaded_0900_vertices_set()
        elif truck.get_loaded_1030_vertices_set():
            vertices_to_sort = truck.get_loaded_1030_vertices_set()
        else:
            vertices_to_sort = truck.get_loaded_eod_vertices_set()
        
        # Sorts the list of the most appropriate set of package delivery addresses then iterates through each vertex from closest to furthest
        for vertex in sorted(vertices_to_sort, key=operator.attrgetter("distance")): # truck.get_loaded_vertices_set()   
            # This excludes the vertex matching this location
            if vertex.distance > 0:
                # Sets the closest vertex to the truck's destination and adds to delivery queue
                if truck.get_delivery_queue():
                    truck.pop_front_delivery_queue()
                truck.add_to_delivery_queue(vertex)
                truck.change_destination(vertex)
                truck.change_destination_distance(vertex.distance)
                break
            else:
                continue
        return
