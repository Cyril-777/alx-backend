#!/usr/bin/env python3
""" LFU Caching """

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFU (Least Frequently Used) caching system """

    def __init__(self):
        """ Initialize the LFUCache """
        super().__init()
        self.frequency = {}  # Keeps track of frequency of each key
        self.lru_list = []   # Tracks the order of access for keys

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Key exists, increase its frequency and update access order
            self.frequency[key] += 1
            self.lru_list.remove(key)
        else:
            # Key is new, initialize its frequency
            self.frequency[key] = 1

        if len(self.cache_data) >= self.MAX_ITEMS:
            # Find the least frequent key(s), and in case of a tie, use LRU
            lfu_keys = [key for key in self.cache_data
                        if self.frequency[key] == min(self.frequency
                                                      .values())]
            lru_key = min(self.lru_list, key=self.lru_list.index)
            if len(lfu_keys) > 1:
                key_to_discard = min(lfu_keys, key=self.lru_list.index)
            else:
                key_to_discard = lfu_keys[0]

            del self.cache_data[key_to_discard]
            del self.frequency[key_to_discard]
            self.lru_list.remove(key_to_discard)
            print(f"DISCARD: {key_to_discard}")

        self.cache_data[key] = item
        self.lru_list.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and access order
        self.frequency[key] += 1
        self.lru_list.remove(key)
        self.lru_list.append(key)

        return self.cache_data[key]
