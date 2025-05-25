import pandas as pd
import numpy as np
import logging
from typing import List, Tuple
from annoy.model import Node

from abc import ABC, abstractmethod

class Model(ABC):
    """
    Abstract base class for models.
    """
    @abstractmethod
    def train(self,root,  data: pd.DataFrame) -> None:
        """
        Train the model with the provided data.
        """
        pass
    

class AnnoyModel(Model):
    """
    Class for building and querying a KD-tree structure.
    """
    def __init__(self, K: int, imb: float) -> None:
        self.K = K
        self.imb = imb
        self.root = None

    def train(self, root):
        
        root.split(self.K, self.imb)
        if root.left :
            self.train(root.left)
        if root.right:
            self.train(root.right)



