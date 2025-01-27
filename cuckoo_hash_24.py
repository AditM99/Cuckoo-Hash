# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24:
    def __init__(self, init_size: int):
        self.__num_rehashes = 0
        self.bucket_size = 4
        self.CYCLE_THRESHOLD = 10

        self.table_size = init_size
        self.tables = [[None]*init_size for _ in range(2)]

    def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
        # you must use this function when you need to displace a random key from a bucket during insertion (see the description in requirements.py). 
        # this function randomly chooses an index from a given bucket for a given table. this ensures that the random 
        # index chosen by your code and our test script match.
        # 
        # for example, if you are inserting some key x into table 0, and hash_func(x, 0) returns 5, and the bucket in index 5 of table 0 already has 4 elements,
        # you will call get_rand_bucket_index(5, 0) to determine which key from that bucket to displace, i.e. if get_random_bucket_index(5, 0) returns 2, you
        # will displace the key at index 2 in that bucket.
        rand.seed(int(str(bucket_idx) + str(table_id)))
        return rand.randint(0, self.bucket_size-1)

    def hash_func(self, key: int, table_id: int) -> int:
        key = int(str(key) + str(self.__num_rehashes) + str(table_id))
        rand.seed(key)
        return rand.randint(0, self.table_size-1)

    def get_table_contents(self) -> List[List[Optional[List[int]]]]:
        # the buckets should be implemented as lists. Table cells with no elements should still have None entries.
        return self.tables

    # you should *NOT* change any of the existing code above this line
    # you may however define additional instance variables inside the __init__ method.

    def insert(self, key: int) -> bool:
        num_cycles = 0
        current_table = 0
        while num_cycles <= self.CYCLE_THRESHOLD:
            index = self.hash_func(key, current_table)
            if self.tables[current_table][index] == None:
                self.tables[current_table][index] = [key]
                return True
            if self.check_length(current_table, index) < 4:
                self.tables[current_table][index].append(key)
                return True
            else: 
                remove_index = self.get_rand_idx_from_bucket(bucket_idx=index, table_id=current_table)
                temp = self.tables[current_table][index][remove_index]
                self.tables[current_table][index][remove_index] = key
                key = temp
                current_table = int(not current_table)
                num_cycles+=1
        return False

    def lookup(self, key: int) -> bool:
        index_0 = self.hash_func(key, 0)
        index_1 = self.hash_func(key, 1)
        table_0_length = self.check_length(tableID=0, index=index_0)
        table_1_length = self.check_length(tableID=1, index=index_1)
        for i in range(table_0_length):
            if self.tables[0][index_0][i] == key:
                return True
        for j in range(table_1_length):
            if self.tables[1][index_1][j] == key:
                return True
        return False
        

    def delete(self, key: int) -> None:
        index_0 = self.hash_func(key=key, table_id=0)
        index_1 = self.hash_func(key=key, table_id=1)
        table_0_length = self.check_length(tableID=0, index=index_0)
        table_1_length = self.check_length(tableID=1, index=index_1)
        if table_0_length == 1 and self.tables[0][index_0][0] == key:
            self.tables[0][index_0] = None
            return
        for i in range(table_0_length):
            if self.tables[0][index_0][i] == key:
                self.tables[0][index_0][i] = None
                self.tables[0][index_0] = [x for x in self.tables[0][index_0] if x is not None]
                return
        if table_1_length == 1 and self.tables[1][index_1][0] == key:
            self.tables[1][index_1] = None
            return
        for j in range(table_1_length):
           if self.tables[1][index_1][j] == key:
                self.tables[1][index_1][j] = None
                self.tables[1][index_1] = [x for x in self.tables[1][index_1] if x is not None]
                return

    def rehash(self, new_table_size: int) -> None:
        self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
        old_tables = self.tables
        self.tables = [[None]*self.table_size for _ in range(2)]
        for table in old_tables:
            for bucket in table:
                if bucket is not None:
                    for key in bucket:
                        if key is not None:
                            self.insert(key)

    def check_length(self, tableID: int, index: int) -> int:
        if self.tables[tableID][index] == None:
            return 0
        else:
            return len(self.tables[tableID][index])

    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define


