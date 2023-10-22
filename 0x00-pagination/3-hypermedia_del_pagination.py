#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination"""


import csv
from typing import List, Tuple, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

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

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """return the appropriate page of the dataset
        (i.e. the correct list of rows)."""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        dataset = self.dataset()
        total_rows = len(dataset)

        if (page - 1) * page_size >= total_rows:
            return []

        start, end = index_range(page, page_size)
        return dataset[start:end]

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> dict:
        """return a dictionary containing the following key-value pairs"""
        assert isinstance(index, int) and index >= 0
        assert isinstance(page_size, int) and page_size > 0

        indexed_dataset = self.indexed_dataset()
        data = []
        next_index = index

        for key in range(index, len(indexed_dataset)):
            if len(data) < page_size:
                if key in indexed_dataset:
                    data.append(indexed_dataset[key])
                    next_index = key + 1
            else:
                break

        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(data),
            'data': data
        }


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """return a tuple of size two containing start index and an end index"""
    return ((page - 1) * page_size, page * page_size)
