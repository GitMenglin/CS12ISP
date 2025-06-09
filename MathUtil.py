from math import *
import numpy as np

def getTranslationMatrix(tX, tY, tZ):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tX, tY, tZ, 1]
    ])

def getRotationMatrix(rX, rY, rZ):
    mX = np.array([
        [1, 0, 0, 0],
        [0, cos(rX), -sin(rX), 0],
        [0, sin(rX), cos(rX), 0],
        [0, 0, 0, 1]
    ])
    mY = np.array([
        [cos(rY), 0, sin(rY), 0],
        [0, 1, 0, 0],
        [-sin(rY), 0, cos(rY), 0],
        [0, 0, 0, 1]
    ])
    mZ = np.array([
        [cos(rZ), -sin(rZ), 0, 0],
        [sin(rZ), cos(rZ), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return mX @ mY @ mZ

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

def scale(vertices, sX, sY, sZ):
    transformation = getScalingMatrix(sX, sY, sZ)
    return vertices @ transformation
