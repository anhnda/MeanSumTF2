# summ_dataset_factory.py

"""
Class to create SummDataset instances.

In part here in a separate file to avoid circular imports
"""

from data_loaders.amazon_dataset import AmazonDataset
from data_loaders.yelp_dataset import YelpDataset
from data_loaders.gene_dataset import GeneDataset


class SummDatasetFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def get(name, tp=0):
        if name == 'amazon':
            return AmazonDataset()
        elif name == 'yelp':
            return YelpDataset()
        elif name == 'gene':
            return GeneDataset(tp=tp)
