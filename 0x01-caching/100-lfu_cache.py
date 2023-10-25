#!/usr/bin/env python3
""" LFU Caching """

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFU (Least Frequently Used) caching system """

    def __init__(self):
        """ Initialize the LFUCache """
        super().__init__()
        self.frequency = {}  # Keeps track of frequency of each key
        self.lru_list = []   # Tracks the order of access for keys

    def put(self, key, item):
        """ Add an item in the cache """
        if key and item:
            if (len(self.lru_list) >= self.MAX_ITEMS and
                    not self.cache_data.get(key)):
                delete = self.lru_list.pop(0)
                self.frequency.pop(delete)
                self.cache_data.pop(delete)
                print('DISCARD: {}'.format(delete))

            if self.cache_data.get(key):
                self.lru_list.remove(key)
                self.frequency[key] += 1
            else:
                self.frequency[key] = 0

            insert_index = 0
            while (insert_index < len(self.lru_list) and
                   not self.frequency[self.lru_list[insert_index]]):
                insert_index += 1
            self.lru_list.insert(insert_index, key)
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and access order
        self.frequency[key] += 1
        self.lru_list.remove(key)
        self.lru_list.append(key)

        return self.cache_data[key]
