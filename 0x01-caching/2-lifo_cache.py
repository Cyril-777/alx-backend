#!/usr/bin/env python3
""" LIFOCache module
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ Inherits from BaseCaching and is a LIFO cache """

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """ Add item to cache data """
        if key and item:
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                print("DISCARD: {}".format(list(self.cache_data)[-2]))
                self.cache_data.pop(list(self.cache_data)[-2])

    def get(self, key):
        """ Get item from cache data """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
