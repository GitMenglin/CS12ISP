from math import *
import numpy as np

WIDTH, HEIGHT = 800, 600

black = (0, 0, 0)
gray = (134, 134, 134)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grass = (127, 178, 56)
dirt = (151, 109, 77)
stone = (112, 112, 112)
logStriped = (247, 233, 163)
logBark = (102, 76, 51)
leaves = (0, 124, 0)
void = (0, 191, 191)

steveSkin = (169, 125, 100)
steveShirt = (0, 175, 175)
stevePant = (73, 70, 151)
steveEye = (73, 70, 151)
steveHair = (49, 48, 43)
steveShoe = (107, 107, 107)

alexSkin = (242, 218, 186)
alexShirt = (140, 190, 138)
alexPant = (104, 69, 48)
alexEye = (140, 190, 138)
alexHair = (229, 153, 71)
alexShoe = (107, 107, 107)

debug = False
profile = False
worldSize = 20 * 16
renderingRadius = 6
renderingRange = 2 * renderingRadius + 1

cameraBasisVectors = np.array([
    np.array([0., 0., 1., 1.]),
    np.array([0., 1., 0., 1.]),
    np.array([1., 0., 0., 1.])
    ])

cameraBasisVelocities = np.array([
    np.array([0., 0., 1., 1.]),
    np.array([1., 0., 0., 1.])
    ])

horizontalFieldOfView = pi / 2
verticalFieldOfView = horizontalFieldOfView * (HEIGHT / WIDTH)
nearClippingPlane = 0.01
farClippingPlane = 100
right = tan(horizontalFieldOfView / 2)
top = tan(verticalFieldOfView / 2)

projectionMatrix = np.array([
    [1 / right, 0, 0, 0],
    [0, 1 / top, 0, 0],
    [0, 0, (farClippingPlane + nearClippingPlane) / (farClippingPlane - nearClippingPlane), 0],
    [0, 0, 0, 1]
    ])

screenTransformation = np.array([
    [WIDTH / 2, 0, 0, 0],
    [0, -HEIGHT / 2, 0, 0],
    [0, 0, 1, 0],
    [WIDTH / 2, HEIGHT / 2, 0, 1]
    ])

cameraToClippingToScreenTransformation = projectionMatrix @ screenTransformation
