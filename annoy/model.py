import pandas as pd
import numpy as np
import logging
from typing import List, Tuple, Optional
from random import random

logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(levelname)s - %(message)s')

# This function calculates the cosine similarity between two vectors
def cosine_similarity(v1 : np.ndarray, v2 : np.ndarray):
    return np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))


# This class represents a node in the KD-tree structure
# Each node contains a hyperplane that divides the data into two parts
# and a list of songs that belong to that node
# The node also has left and right children, which are also nodes in the tree
# The hyperplane is defined by a normal vector and an intercept
# The normal vector is perpendicular to the hyperplane and the intercept is the distance from the origin to the hyperplane

class Node(object):
    
    def __init__(self, hyperplane: Tuple, songs: List[Tuple]):
        self._hyperplane = hyperplane
        self._songs = songs
        self._left: Optional['Node'] = None
        self._right: Optional['Node'] = None

    @property
    def hyperplane(self) -> Optional[Tuple]:
        return self._hyperplane

    @property
    def songs(self) -> List[Tuple[object, np.ndarray]]:
        return self._songs

    @property
    def left(self) -> Optional['Node']:
        return self._left

    @property
    def right(self) -> Optional['Node']:
        return self._right

    #find the hyper plane equation 
    def hyperplane_equation(self, v1 : np.ndarray, v2 : np.ndarray) -> Tuple:
        normal = (v1 - v2)
        mid_point = (v1+v2)/2
        intercept = np.dot(normal , mid_point)
        return normal , intercept


    def split(self, K: int, imb: float) -> bool:
        if len(self._songs) <= K:
            return False

        # Randomly sample two references
        left_ref = self._songs[np.random.randint(len(self.songs)-1)][1]
        right_ref = self._songs[np.random.randint(len(self.songs)-1)][1]

        for _ in range(5):
            left = []
            right = []

            for song in self._songs:
                vec = song[1]
                dist_left = cosine_similarity(vec , left_ref)
                dist_right = cosine_similarity(vec , right_ref)

                if dist_left > dist_right:
                    left.append(song)
                else:
                    right.append(song)

            r = len(left) / len(self._songs)

            # Accept if reasonably balanced
            if r < imb and r > (1 - imb):
                # Set current node's hyperplane
                self._hyperplane = self.hyperplane_equation(right_ref ,left_ref)
                # Create child nodes
                self._left = Node(None, left)
                self._right = Node(None, right)
                self._songs = []  # clear songs at current node
                return True

        return False
    