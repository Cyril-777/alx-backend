#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination"""


import csv
import math
from typing import List, Tuple


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by row number"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> dict:
        """return a dictionary containing the following key-value pairs"""
        assert index is None or (isinstance(index, int) and index >= 0)
        assert isinstance(page_size, int) and page_size > 0

        indexed_dataset = self.indexed_dataset()
        max_index = len(indexed_dataset) - 1

        if index is None:
            # Set index to 0 if it's None
            index = 0
        elif index > max_index:
            raise AssertionError("Index is out of range")

        data = []
        next_index = index
        for _ in range(page_size):
            if next_index in indexed_dataset:
                data.append(indexed_dataset[next_index])
                next_index += 1
            elif next_index <= max_index:
                next_index += 1

        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": next_index if next_index <= max_index else None
        }


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """return a tuple of size two containing start index and an end index"""
    return ((page - 1) * page_size, page * page_size)
