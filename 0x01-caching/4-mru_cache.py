#!/usr/bin/env python3
""" MRU Caching """


from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRU (Most Recently Used) caching system """

    def __init__(self):
        """ Initialize the MRUCache """
        super().__init()
        self.mru_list = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.mru_list.remove(key)

        if len(self.cache_data) >= self.MAX_ITEMS:
            mru_key = self.mru_list.pop()
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")

        self.cache_data[key] = item
        self.mru_list.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None

        self.mru_list.remove(key)
        self.mru_list.append(key)
        return self.cache_data[key]
