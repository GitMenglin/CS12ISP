import numpy as np
from Constants import *

class Geometry:
    camera = [
        np.array([
            np.array([0.0, 0.0, 0.0, 1.0]),
            np.array([-0.25, -0.25, 0.5, 1.0]),
            np.array([-0.25, 0.25, 0.5, 1.0]),
            np.array([0.25, 0.25, 0.5, 1.0]),
            np.array([0.25, -0.25, 0.5, 1.0])
            ]), [
                [0, 1, 2], 
                [0, 2, 3],
                [0, 3, 4],
                [0, 4, 1],
                [1, 4, 3, 2]
            ]]
    
    grassBlock = [
        np.array([
            np.array([0, 0, 0, 1]),
            np.array([0, 1, 0, 1]),
            np.array([1, 1, 0, 1]),
            np.array([1, 0, 0, 1]),
            np.array([0, 0, 1, 1]),
            np.array([0, 1, 1, 1]),
            np.array([1, 1, 1, 1]),
            np.array([1, 0, 1, 1])
            ]), [
                [0, 1, 2, 3],
                [4, 7, 6, 5],
                [0, 4, 5, 1],
                [2, 6, 7, 3],
                [1, 5, 6, 2],
                [0, 3, 7, 4]
            ], [
                dirt,
                dirt,
                dirt,
                dirt,
                grass,
                dirt
            ]]
