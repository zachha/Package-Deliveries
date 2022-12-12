class HashTable:
    # Constructor function that creates a hash table with a starting size as input or default to 40 
    def __init__(self, starting_size=40):
        self.__hashtable = []
        self.__starting_size = starting_size
        for x in range(starting_size):
            self.__hashtable.append([])

    # Methods

    # Inserts new package into the hash table  
    def hash_insert(self, package):
        # Finds bucket and bucket list by hashing package id 
        bucket = hash(package.get_id) % self.__starting_size
        bucket_list = self.__hashtable[bucket]

        # Appends package into the bucket list for that bucket
        bucket_list.append(package)

    # Remove package linked to the input package id from the hash table
    # Returns True if package was found and removed, False if package was not in table
    def hash_remove(self, package_id):
        # Finds bucket and bucket list by hashing package id
        bucket = hash(package_id) % self.__starting_size
        bucket_list = self.__hashtable[bucket]

        # If package id is found in the bucket list, removes the package from the hash table
        if package_id in bucket_list:
            bucket_list.remove(package_id)

    # Searches for hashed package linked to input package id
    # Returns package if present in hash table, returns None if package not present in hash table
    def hash_search(self, package_id):
        # Finds bucket and bucket list by hashing package id
        bucket = hash(package_id) % self.__starting_size
        bucket_list = self.__hashtable[bucket]

        # If package id is in the bucket list, returns the package, else returns None
        if package_id in bucket_list:
            return bucket_list[bucket_list.index(package_id)]
        else:
            return None
