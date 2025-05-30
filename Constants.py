from math import *
import numpy as np

WIDTH, HEIGHT = 600, 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)

horizontalFieldOfView = pi / 2
verticalFieldOfView = horizontalFieldOfView * (HEIGHT / WIDTH)
nearClippingPlane = 0.1
farClippingPlane = 100
right = tan(horizontalFieldOfView / 2)
top = tan(verticalFieldOfView / 2)

projectionMatrix = np.array([
    [1 / right, 0, 0, 0],
    [0, 1 / top, 0, 0],
    [0, 0, (farClippingPlane + nearClippingPlane) / (farClippingPlane - nearClippingPlane), 1],
    [0, 0, -2 * farClippingPlane * nearClippingPlane / (farClippingPlane - nearClippingPlane), 0]
    ])

screenTransformation = np.array([
            [WIDTH / 2, 0, 0, 0],
            [0, -HEIGHT / 2, 0, 0],
            [0, 0, 1, 0],
            [WIDTH / 2, HEIGHT / 2, 0, 1]
        ])
