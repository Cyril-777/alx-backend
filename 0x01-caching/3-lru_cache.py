#!/usr/bin/env python3
""" LRUCache module
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ Inherits from BaseCaching and is a LRU cache
    """

    def __init__(self):
        super().__init__()
        self.lru_order = []

    def put(self, key, item):
        """ Add item to cache data """
        if key and item:
            if key in self.cache_data:
                self.lru_order.remove(key)
            self.lru_order.append(key)
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                print("DISCARD: {}".format(self.lru_order[0]))
                self.cache_data.pop(self.lru_order[0])
                self.lru_order.pop(0)

    def get(self, key):
        """ Get item from cache data """
        if key is None or key not in self.cache_data:
            return None
        self.lru_order.remove(key)
        self.lru_order.append(key)
        return self.cache_data[key]
