from math import *
import numpy as np

def getTranslationMatrix(tX, tY, tZ):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tX, tY, tZ, 1]
    ])

def getRotationX(rX):
    return np.array([
        [1, 0, 0, 0],
        [0, cos(rX), -sin(rX), 0],
        [0, sin(rX), cos(rX), 0],
        [0, 0, 0, 1]
        ])

def getRotationY(rY):
    return np.array([
        [cos(rY), 0, sin(rY), 0],
        [0, 1, 0, 0],
        [-sin(rY), 0, cos(rY), 0],
        [0, 0, 0, 1]
        ])

def getRotationZ(rZ):
    return np.array([
        [cos(rZ), -sin(rZ), 0, 0],
        [sin(rZ), cos(rZ), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ])

def getRotationMatrix(rX, rY, rZ):
    return getRotationX(rX) @ getRotationY(rY) @ getRotationZ(rZ)

def getScalingMatrix(sX, sY, sZ):
    return np.array([
        [sX, 0, 0, 0],
        [0, sY, 0, 0],
        [0, 0, sZ, 0],
        [0, 0, 0, 1]
    ])

def translate(vertices, tX, tY, tZ):
    transformation = getTranslationMatrix(tX, tY, tZ)
    return vertices @ transformation

def rotate(vertices, rX, rY, rZ):
    transformation = getRotationMatrix(rX, rY, rZ)
    return vertices @ transformation

def rotateX(vertices, rX):
    transformation = getRotationX(rX)
    return vertices @ transformation

def rotateY(vertices, rY):
    transformation = getRotationY(rY)
    return vertices @ transformation

def rotateZ(vertices, rZ):
    transformation = getRotationZ(rZ)
    return vertices @ transformation

def scale(vertices, sX, sY, sZ):
    transformation = getScalingMatrix(sX, sY, sZ)
    return vertices @ transformation
