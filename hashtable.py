class EmptyBucket:
    pass

class HashTable:
    # Constructor function that creates a hash table with a starting size as input or default to 40 
    def __init__(self, starting_size=40):
        self.__starting_size = starting_size
        # Empty Since Start and Empty After Removal empty bucket types
        self.__ESS = EmptyBucket()
        self.__EAR = EmptyBucket()
        self.__hashtable = [self.__ESS] * self.__starting_size

    # Getter
    def get_hashtable(self):
        return self.__hashtable

    # Methods

    # Inserts new package into the hash table  
    # Returns True if package is inserted and False if table is full and can't be inserted
    def hash_insert(self, package):
        # Finds bucket by hashing package id and initializes buckets_searched to 0
        bucket = hash(package.get_id()) % self.__starting_size
        buckets_searched = 0

        # Linearly searches from the starting bucket through the hash table to find an open spot to insert
        while buckets_searched < self.__starting_size:
            if type(self.__hashtable[bucket]) is EmptyBucket:
                self.__hashtable[bucket] = package
                return True
            buckets_searched += 1
            bucket = (bucket + 1) % self.__starting_size

        # If no spots are available, package is not inserted and method returns False
        return False

    # Remove package linked to the input package id from the hash table
    # Returns True if package was found and removed, False if package was not in table
    def hash_remove(self, package_id):
        # Finds bucket by hashing package id and initializes buckets_searched to 0
        bucket = hash(package_id) % self.__starting_size
        buckets_searched = 0

        # Linearly checks each bucket that hasn't been empty since start from the starting bucket
        while (self.__hashtable[bucket] is not self.__ESS) and (buckets_searched < self.__starting_size):
            if self.__hashtable[bucket].get_id() == package_id:
                self.__hashtable[bucket] = self.__EAR

            # Iterates the bucket and buckets_searched variables before the while loop continues
            buckets_searched += 1
            bucket = (bucket + 1) % self.__starting_size

    # Searches for hashed package linked to input package id
    # Returns package if present in hash table, returns None if package not present in hash table
    def hash_search(self, package_id):
        # Finds bucket by hashing package id and initializes buckets_searched to 0
        bucket = hash(package_id) % self.__starting_size
        buckets_searched = 0

        # Linearly checks each bucket that hasn't been empty since start from the starting bucket
        while (self.__hashtable[bucket] is not self.__ESS) and (buckets_searched <= self.__starting_size):
            if self.__hashtable[bucket].get_id() == package_id:
                return self.__hashtable[bucket]

            # Iterates the bucket and buckets_searched variables before the while loop continues
            buckets_searched += 1
            bucket = (bucket + 1) % self.__starting_size
        # If package isn't found, returns None
        return None
