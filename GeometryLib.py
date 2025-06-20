import numpy as np
from math import *
from MathUtil import *
from Constants import *

class Geometry:
    head = np.array([
        np.array([-0.25, 0., -0.25, 1.]),
        np.array([-0.25, 0.5, -0.25, 1.]),
        np.array([0.25, 0.5, -0.25, 1.]),
        np.array([0.25, 0., -0.25, 1.]),
        np.array([-0.25, 0., 0.25, 1.]),
        np.array([-0.25, 0.5, 0.25, 1.]),
        np.array([0.25, 0.5, 0.25, 1.]),
        np.array([0.25, 0., 0.25, 1.]),
        np.array([-0.25, 0.35, 0.25, 1.]),
        np.array([-0.15, 0.35, 0.25, 1.]),
        np.array([-0.15, 0.4, 0.25, 1.]),
        np.array([0.15, 0.4, 0.25, 1.]),
        np.array([0.15, 0.35, 0.25, 1.]),
        np.array([0.25, 0.35, 0.25, 1.]),
        
        np.array([-0.1875, 0.21875, 0.25, 1.]),
        np.array([-0.1875, 0.28125, 0.25, 1.]),
        np.array([-0.125, 0.21875, 0.25, 1.]),
        np.array([-0.125, 0.28125, 0.25, 1.]),
        np.array([-0.0625, 0.21875, 0.25, 1.]),
        np.array([-0.0625, 0.28125, 0.25, 1.]),
        
        np.array([0.0625, 0.21875, 0.25, 1.]),
        np.array([0.0625, 0.28125, 0.25, 1.]),
        np.array([0.125, 0.21875, 0.25, 1.]),
        np.array([0.125, 0.28125, 0.25, 1.]),
        np.array([0.1875, 0.21875, 0.25, 1.]),
        np.array([0.1875, 0.28125, 0.25, 1.])
        ])
    
    body = np.array([
        np.array([-0.25, -0.7, -0.125, 1.]),
        np.array([-0.25, 0., -0.125, 1.]),
        np.array([0.25, 0., -0.125, 1.]),
        np.array([0.25, -0.7, -0.125, 1.]),
        np.array([-0.25, -0.7, 0.125, 1.]),
        np.array([-0.25, 0., 0.125, 1.]),
        np.array([0.25, 0., 0.125, 1.]),
        np.array([0.25, -0.7, 0.125, 1.])
        ])
    
    arms = [
        np.array([
            np.array([-0.5, -0.575, -0.125, 1.]),
            np.array([-0.5, 0.125, -0.125, 1.]),
            np.array([-0.25, 0.125, -0.125, 1.]),
            np.array([-0.25, -0.575, -0.125, 1.]),
            np.array([-0.5, -0.575, 0.125, 1.]),
            np.array([-0.5, 0.125, 0.125, 1.]),
            np.array([-0.25, 0.125, 0.125, 1.]),
            np.array([-0.25, -0.575, 0.125, 1.]),
            
            np.array([-0.5, -0.125, -0.125, 1.]),
            np.array([-0.25, -0.125, -0.125, 1.]),
            np.array([-0.5, -0.125, 0.125, 1.]),
            np.array([-0.25, -0.125, 0.125, 1.])
            ]),
        np.array([
            np.array([0.25, -0.575, -0.125, 1.]),
            np.array([0.25, 0.125, -0.125, 1.]),
            np.array([0.5, 0.125, -0.125, 1.]),
            np.array([0.5, -0.575, -0.125, 1.]),
            np.array([0.25, -0.575, 0.125, 1.]),
            np.array([0.25, 0.125, 0.125, 1.]),
            np.array([0.5, 0.125, 0.125, 1.]),
            np.array([0.5, -0.575, 0.125, 1.]),
            
            np.array([0.25, -0.125, -0.125, 1.]),
            np.array([0.5, -0.125, -0.125, 1.]),
            np.array([0.25, -0.125, 0.125, 1.]),
            np.array([0.5, -0.125, 0.125, 1.])
            ])
        ]
    
    legs = [
        np.array([
            np.array([-0.25, -0.7, -0.125, 1.]),
            np.array([-0.25, 0., -0.125, 1.]),
            np.array([0., 0., -0.125, 1.]),
            np.array([0., -0.7, -0.125, 1.]),
            np.array([-0.25, -0.7, 0.125, 1.]),
            np.array([-0.25, 0., 0.125, 1.]),
            np.array([0., 0., 0.125, 1.]),
            np.array([0., -0.7, 0.125, 1.]),
            
            np.array([-0.25, -0.55, -0.125, 1.]),
            np.array([0., -0.55, -0.125, 1.]),
            np.array([-0.25, -0.55, 0.125, 1.]),
            np.array([0., -0.55, 0.125, 1.])
            ]),
        np.array([
            np.array([0., -0.7, -0.125, 1.]),
            np.array([0., 0., -0.125, 1.]),
            np.array([0.25, 0., -0.125, 1.]),
            np.array([0.25, -0.7, -0.125, 1.]),
            np.array([0., -0.7, 0.125, 1.]),
            np.array([0., 0., 0.125, 1.]),
            np.array([0.25, 0., 0.125, 1.]),
            np.array([0.25, -0.7, 0.125, 1.]),
            
            np.array([0., -0.55, -0.125, 1.]),
            np.array([0.25, -0.55, -0.125, 1.]),
            np.array([0., -0.55, 0.125, 1.]),
            np.array([0.25, -0.55, 0.125, 1.])
            ])
        ]
    
    steve = [
        [
            head, [
                [0, 1, 2, 3],
                [4, 7, 6, 5],
                [0, 8, 5, 1],
                [0, 4, 8],
                [2, 6, 13, 3],
                [3, 13, 7],
                [1, 5, 6, 2],
                [0, 3, 7, 4],
                [5, 8, 9, 10, 11, 12, 13, 6],
                
                [14, 16, 17, 15],
                [16, 18, 19, 17],
                [20, 22, 23, 21],
                [22, 24, 25, 23]
                ], [
                    steveHair,
                    steveSkin,
                    steveHair,
                    steveSkin,
                    steveHair,
                    steveSkin,
                    steveHair,
                    steveSkin,
                    steveHair,
                    
                    white,
                    steveEye,
                    steveEye,
                    white
                    ]
        ],
        [
            body, [
                [0, 1, 2, 3],
                [4, 7, 6, 5],
                [0, 4, 5, 1],
                [2, 6, 7, 3],
                [1, 5, 6, 2],
                [0, 3, 7, 4]
                ], [
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt
                    ]
        ],
        [
            arms[0], [
                [1, 5, 6, 2],
                [1, 2, 9, 8],
                [5, 10, 11, 6],
                [1, 8, 10, 5],
                [2, 6, 11, 9],
                
                [0, 8, 9, 3],
                [4, 7, 11, 10],
                [0, 4, 10, 8],
                [3, 9, 11, 7],
                [0, 3, 7, 4]
                ], [
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    
                    steveSkin,
                    steveSkin,
                    steveSkin,
                    steveSkin,
                    steveSkin
                    ]
        ],
        [
            arms[1], [
                [1, 5, 6, 2],
                [1, 2, 9, 8],
                [5, 10, 11, 6],
                [1, 8, 10, 5],
                [2, 6, 11, 9],
                
                [0, 8, 9, 3],
                [4, 7, 11, 10],
                [0, 4, 10, 8],
                [3, 9, 11, 7],
                [0, 3, 7, 4]
                ], [
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    
                    steveSkin,
                    steveSkin,
                    steveSkin,
                    steveSkin,
                    steveSkin
                    ]
        ],
        [
            legs[0], [
                [1, 5, 6, 2],
                [1, 2, 9, 8],
                [5, 10, 11, 6],
                [1, 8, 10, 5],
                [2, 6, 11, 9],
                
                [0, 8, 9, 3],
                [4, 7, 11, 10],
                [0, 4, 10, 8],
                [3, 9, 11, 7],
                [0, 3, 7, 4]
                ], [
                    stevePant,
                    stevePant,
                    stevePant,
                    stevePant,
                    stevePant,
                    
                    steveShoe,
                    steveShoe,
                    steveShoe,
                    steveShoe,
                    steveShoe
                    ]
        ],
        [
            legs[1], [
                [1, 5, 6, 2],
                [1, 2, 9, 8],
                [5, 10, 11, 6],
                [1, 8, 10, 5],
                [2, 6, 11, 9],
                
                [0, 8, 9, 3],
                [4, 7, 11, 10],
                [0, 4, 10, 8],
                [3, 9, 11, 7],
                [0, 3, 7, 4]
                ], [
                    stevePant,
                    stevePant,
                    stevePant,
                    stevePant,
                    stevePant,
                    
                    steveShoe,
                    steveShoe,
                    steveShoe,
                    steveShoe,
                    steveShoe
                    ]
        ]
        ]
    
    alex = [
        [
            head, [
                [0, 1, 2, 3],
                [4, 7, 6, 5],
                [0, 8, 5, 1],
                [0, 4, 8],
                [2, 6, 13, 3],
                [3, 13, 7],
                [1, 5, 6, 2],
                [0, 3, 7, 4],
                [5, 8, 9, 10, 11, 12, 13, 6],
                
                [14, 16, 17, 15],
                [16, 18, 19, 17],
                [20, 22, 23, 21],
                [22, 24, 25, 23]
                ], [
                    alexHair,
                    alexSkin,
                    alexHair,
                    alexSkin,
                    alexHair,
                    alexSkin,
                    alexHair,
                    alexSkin,
                    alexHair,
                    
                    white,
                    [0.5 * color for color in alexEye],
                    [0.5 * color for color in alexEye],
                    white
                    ]
        ],
        [
            body, [
                [0, 1, 2, 3],
                [4, 7, 6, 5],
                [0, 4, 5, 1],
                [2, 6, 7, 3],
                [1, 5, 6, 2],
                [0, 3, 7, 4]
                ], [
                    alexShirt,
                    alexShirt,
                    alexShirt,
                    alexShirt,
                    alexShirt,
                    alexShirt
                    ]
        ],
        [
            arms[0], [
                [1, 5, 6, 2],
                [1, 2, 9, 8],
                [5, 10, 11, 6],
                [1, 8, 10, 5],
                [2, 6, 11, 9],
                
                [0, 8, 9, 3],
                [4, 7, 11, 10],
                [0, 4, 10, 8],
                [3, 9, 11, 7],
                [0, 3, 7, 4]
                ], [
                    alexShirt,
                    alexShirt,
                    alexShirt,
                    alexShirt,
                    alexShirt,
                    
                    alexSkin,
                    alexSkin,
                    alexSkin,
                    alexSkin,
                    alexSkin
                    ]
        ],
        [
            arms[1], [
                [1, 5, 6, 2],
                [1, 2, 9, 8],
                [5, 10, 11, 6],
                [1, 8, 10, 5],
                [2, 6, 11, 9],
                
                [0, 8, 9, 3],
                [4, 7, 11, 10],
                [0, 4, 10, 8],
                [3, 9, 11, 7],
                [0, 3, 7, 4]
                ], [
                    alexShirt,
                    alexShirt,
                    alexShirt,
                    alexShirt,
                    alexShirt,
                    
                    alexSkin,
                    alexSkin,
                    alexSkin,
                    alexSkin,
                    alexSkin
                    ]
        ],
        [
            [
                *legs[0][:8],
                np.array([-0.25, -0.4, -0.125, 1.]),
                np.array([0., -0.4, -0.125, 1.]),
                np.array([-0.25, -0.4, 0.125, 1.]),
                np.array([0., -0.4, 0.125, 1.])
                ], [
                    [1, 5, 6, 2],
                    [1, 2, 9, 8],
                    [5, 10, 11, 6],
                    [1, 8, 10, 5],
                    [2, 6, 11, 9],
                    
                    [0, 8, 9, 3],
                    [4, 7, 11, 10],
                    [0, 4, 10, 8],
                    [3, 9, 11, 7],
                    [0, 3, 7, 4]
                    ], [
                        alexPant,
                        alexPant,
                        alexPant,
                        alexPant,
                        alexPant,
                        
                        alexShoe,
                        alexShoe,
                        alexShoe,
                        alexShoe,
                        alexShoe
                        ]
        ],
        [
            [
                *legs[1][:8],
                np.array([0., -0.4, -0.125, 1.]),
                np.array([0.25, -0.4, -0.125, 1.]),
                np.array([0., -0.4, 0.125, 1.]),
                np.array([0.25, -0.4, 0.125, 1.])
                ], [
                    [1, 5, 6, 2],
                    [1, 2, 9, 8],
                    [5, 10, 11, 6],
                    [1, 8, 10, 5],
                    [2, 6, 11, 9],
                    
                    [0, 8, 9, 3],
                    [4, 7, 11, 10],
                    [0, 4, 10, 8],
                    [3, 9, 11, 7],
                    [0, 3, 7, 4]
                    ], [
                        alexPant,
                        alexPant,
                        alexPant,
                        alexPant,
                        alexPant,
                        
                        alexShoe,
                        alexShoe,
                        alexShoe,
                        alexShoe,
                        alexShoe
                        ]
        ]
        ]
    
    herobrine = [
        [
            np.array([
                np.array([-0.25, 0., -0.25, 1.]),
                np.array([-0.25, 0.5, -0.25, 1.]),
                np.array([0.25, 0.5, -0.25, 1.]),
                np.array([0.25, 0., -0.25, 1.]),
                np.array([-0.25, 0., 0.25, 1.]),
                np.array([-0.25, 0.5, 0.25, 1.]),
                np.array([0.25, 0.5, 0.25, 1.]),
                np.array([0.25, 0., 0.25, 1.]),
                np.array([-0.25, 0.35, 0.25, 1.]),
                np.array([-0.15, 0.35, 0.25, 1.]),
                np.array([-0.15, 0.4, 0.25, 1.]),
                np.array([0.15, 0.4, 0.25, 1.]),
                np.array([0.15, 0.35, 0.25, 1.]),
                np.array([0.25, 0.35, 0.25, 1.]),
                
                np.array([-0.1875, 0.21875, 0.25, 1.]),
                np.array([-0.0625, 0.21875, 0.25, 1.]),
                np.array([-0.0625, 0.28125, 0.25, 1.]),
                np.array([-0.1875, 0.28125, 0.25, 1.]),
                
                np.array([0.0625, 0.21875, 0.25, 1.]),
                np.array([0.1875, 0.21875, 0.25, 1.]),
                np.array([0.1875, 0.28125, 0.25, 1.]),
                np.array([0.0625, 0.28125, 0.25, 1.])
                ]), [
                    [0, 1, 2, 3],
                    [4, 7, 6, 5],
                    [0, 8, 5, 1],
                    [0, 4, 8],
                    [2, 6, 13, 3],
                    [3, 13, 7],
                    [1, 5, 6, 2],
                    [0, 3, 7, 4],
                    [5, 8, 9, 10, 11, 12, 13, 6],
                    
                    [14, 15, 16, 17],
                    [18, 19, 20, 21]
                    ], [
                        steveHair,
                        steveSkin,
                        steveHair,
                        steveSkin,
                        steveHair,
                        steveSkin,
                        steveHair,
                        steveSkin,
                        steveHair,
                        
                        white,
                        white
                        ]
        ],
        [
            body, [
                [0, 1, 2, 3],
                [4, 7, 6, 5],
                [0, 4, 5, 1],
                [2, 6, 7, 3],
                [1, 5, 6, 2],
                [0, 3, 7, 4]
                ], [
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt
                    ]
        ],
        [
            arms[0], [
                [1, 5, 6, 2],
                [1, 2, 9, 8],
                [5, 10, 11, 6],
                [1, 8, 10, 5],
                [2, 6, 11, 9],
                
                [0, 8, 9, 3],
                [4, 7, 11, 10],
                [0, 4, 10, 8],
                [3, 9, 11, 7],
                [0, 3, 7, 4]
                ], [
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    
                    steveSkin,
                    steveSkin,
                    steveSkin,
                    steveSkin,
                    steveSkin
                    ]
        ],
        [
            arms[1], [
                [1, 5, 6, 2],
                [1, 2, 9, 8],
                [5, 10, 11, 6],
                [1, 8, 10, 5],
                [2, 6, 11, 9],
                
                [0, 8, 9, 3],
                [4, 7, 11, 10],
                [0, 4, 10, 8],
                [3, 9, 11, 7],
                [0, 3, 7, 4]
                ], [
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    steveShirt,
                    
                    steveSkin,
                    steveSkin,
                    steveSkin,
                    steveSkin,
                    steveSkin
                    ]
        ],
        [
            legs[0], [
                [1, 5, 6, 2],
                [1, 2, 9, 8],
                [5, 10, 11, 6],
                [1, 8, 10, 5],
                [2, 6, 11, 9],
                
                [0, 8, 9, 3],
                [4, 7, 11, 10],
                [0, 4, 10, 8],
                [3, 9, 11, 7],
                [0, 3, 7, 4]
                ], [
                    stevePant,
                    stevePant,
                    stevePant,
                    stevePant,
                    stevePant,
                    
                    steveShoe,
                    steveShoe,
                    steveShoe,
                    steveShoe,
                    steveShoe
                    ]
        ],
        [
            legs[1], [
                [1, 5, 6, 2],
                [1, 2, 9, 8],
                [5, 10, 11, 6],
                [1, 8, 10, 5],
                [2, 6, 11, 9],
                
                [0, 8, 9, 3],
                [4, 7, 11, 10],
                [0, 4, 10, 8],
                [3, 9, 11, 7],
                [0, 3, 7, 4]
                ], [
                    stevePant,
                    stevePant,
                    stevePant,
                    stevePant,
                    stevePant,
                    
                    steveShoe,
                    steveShoe,
                    steveShoe,
                    steveShoe,
                    steveShoe
                    ]
        ]
        ]
    
    players = {
        "steve": steve,
        "alex": alex,
        "herobrine": herobrine
        }
    
    block = [
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
                ]
            ]
    
    grassBlock = [*block, [dirt, dirt, dirt, dirt, grass, dirt]]
    
    dirt = [*block, [dirt, dirt, dirt, dirt, dirt, dirt]]
    
    stone = [*block, [stone, stone, stone, stone, stone, stone]]
    
    log = [
        np.array([
            *block[0],
            np.array([0.1, 0., 0.1, 1.]),
            np.array([0.1, 0., 0.9, 1.]),
            np.array([0.9, 0., 0.9, 1.]),
            np.array([0.9, 0., 0.1, 1.]),
            np.array([0.1, 1., 0.1, 1.]),
            np.array([0.1, 1., 0.9, 1.]),
            np.array([0.9, 1., 0.9, 1.]),
            np.array([0.9, 1., 0.1, 1.])
            ]), [
                *block[1],
                [11, 10, 9, 8],
                [12, 13, 14, 15]
                ], [
                    logBark,
                    logBark,
                    logBark,
                    logBark,
                    logBark,
                    logBark,
                    logStriped,
                    logStriped
                    ]
                ]
    
    leavesFront = np.array([
        np.array([0., 0., 0., 1.]),
        np.array([0., 1 / 3, 0., 1.]),
        np.array([1 / 3, 1 / 3, 0., 1.]),
        np.array([1 / 3, 2 / 3, 0., 1.]),
        np.array([0., 2 / 3, 0., 1.]),
        np.array([0., 1., 0., 1.]),
        np.array([1 / 3, 1., 0., 1.]),
        np.array([1 / 3, 2 / 3, 0., 1.]),
        np.array([2 / 3, 2 / 3, 0., 1.]),
        np.array([2 / 3, 1., 0., 1.]),
        np.array([1., 1., 0., 1.]),
        np.array([1., 2 / 3, 0., 1.]),
        np.array([2 / 3, 2 / 3, 0., 1.]),
        np.array([2 / 3, 1 / 3, 0., 1.]),
        np.array([1., 1 / 3, 0., 1.]),
        np.array([1., 0., 0., 1.]),
        np.array([2 / 3, 0., 0., 1.]),
        np.array([2 / 3, 1 / 3, 0., 1.]),
        np.array([1 / 3, 1 / 3, 0., 1.]),
        np.array([1 / 3, 0., 0., 1.])
        ])
    
    leaves = [
        np.array([
            *leavesFront,
            *translate(rotate(leavesFront, 0, pi, 0), 1, 0, 1),
            *translate(rotate(leavesFront, 0, -pi / 2, 0), 0, 0, 1),
            *translate(rotate(leavesFront, 0, pi / 2, 0), 1, 0, 0),
            *translate(rotate(leavesFront, -pi / 2, 0, 0), 0, 1, 0),
            *translate(rotate(leavesFront, pi / 2, 0, 0), 0, 0, 1)
            ]), [
                [j + 20 * i for j in range(20)] for i in range(6)
                ], [leaves for _ in range(6)]
            ]
    
    blocks = {
        "grassBlock": grassBlock,
        "dirt": dirt,
        "stone": stone,
        "log": log,
        "leaves": leaves
    }
    
    hotBarTransformation = getTranslationMatrix(-0.5, -0.5, -0.5) @ getScalingMatrix(20, 20, 20) @ getRotationX(-5 * pi / 6) @ getRotationY(-pi / 4)
    hotBar = {
        "grassBlock": [grassBlock[0] @ hotBarTransformation, grassBlock[1], grassBlock[2]],
        "dirt": [dirt[0] @ hotBarTransformation, dirt[1], dirt[2]],
        "stone": [stone[0] @ hotBarTransformation, stone[1], stone[2]],
        "log": [log[0] @ hotBarTransformation, log[1], log[2]],
        "leaves": [leaves[0] @ hotBarTransformation, leaves[1], leaves[2]]
    }
