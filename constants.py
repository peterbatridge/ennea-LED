RED = (255, 0, 0)
YELLOW = (255, 150, 0)
ORANGE = (255, 40, 0)
GREEN = (0, 255, 0)
TEAL = (0, 255, 120)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)
WHITE = (255, 255, 255)
BLANK = (0, 0, 0)
colors = [RED, ORANGE, YELLOW, GREEN, TEAL, CYAN,  BLUE, PURPLE, MAGENTA]

###
# Groups Of Nonagons
###

everyNonagon = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13]]

columnsLeftToRight = [[3,4],[1,2,5,6],[7,10, 11, 0],[8, 9, 12, 13]]
columnsRightToLeft= columnsLeftToRight[::-1]
rowsBottomToTop = [[0],[1,13],[2,12],[3,11],[4,10],[5,9],[6,8],[7]]
rowsTopToBottom = rowsBottomToTop[::-1]

bottomLeftToTopRightDiagonal = [[0,1],[2,3,13],[4,11,12],[5,10],[6,9],[7,8]]
bottomLeftToTopRightSharpDiagonal = [[1,3],[0,2,4],[5,11,13],[6,10,12],[7,9],[8]]
topRightToBottomLeftDiagonal = bottomLeftToTopRightDiagonal[::-1]
topRightToBottomLeftSharpDiagonal = bottomLeftToTopRightSharpDiagonal[::-1]

bottomRightToTopLeftDiagonal = [[0,13],[1,12],[2,11],[3,9,10],[4,5,8],[6,7]]
bottomRightToTopLeftSharpDiagonal = [[13],[0,12],[1,11,9],[2,10,8],[3,5,7],[4,6]]
topLeftToBottomRightDiagonal = bottomRightToTopLeftDiagonal[::-1]
topLeftToBottomRightSharpDiagonal = bottomRightToTopLeftSharpDiagonal[::-1]

triangles = [[0,2,4,6,8,10,12], [1,3,5,7,9,11,13]]

groupsOfNonagons = {
    'everyNonagon' : everyNonagon,
    'columnsLeftToRight': columnsLeftToRight,
    'columnsRightToLeft': columnsRightToLeft,
    'rowsBottomToTop': rowsBottomToTop,
    'rowsTopToBottom': rowsTopToBottom,
    'bottomLeftToTopRightDiagonal': bottomLeftToTopRightDiagonal,
    'bottomLeftToTopRightSharpDiagonal': bottomLeftToTopRightSharpDiagonal,
    'topRightToBottomLeftDiagonal': topRightToBottomLeftDiagonal,
    'topRightToBottomLeftSharpDiagonal': topRightToBottomLeftSharpDiagonal,
    'bottomRightToTopLeftDiagonal':  bottomRightToTopLeftDiagonal,
    'bottomRightToTopLeftSharpDiagonal': bottomRightToTopLeftSharpDiagonal,
    'topLeftToBottomRightDiagonal':topLeftToBottomRightDiagonal,
    'topLeftToBottomRightSharpDiagonal': topLeftToBottomRightSharpDiagonal,
    'triangles': triangles
}

###
# Sets of Groups of Nonagons
###
eightDirectionGroups = [
    rowsTopToBottom,
    topLeftToBottomRightDiagonal,
    columnsLeftToRight,
    bottomLeftToTopRightDiagonal,
    rowsBottomToTop,
    bottomRightToTopLeftDiagonal,
    columnsRightToLeft,
    topRightToBottomLeftDiagonal
]

setsOfGroupsOfNonagons = {
    'eightDirectionGroups': eightDirectionGroups
}

###
# Color Sequences
###
redAndBlue = [RED,BLUE]
redToBlueEight = [RED, RED, ORANGE, ORANGE, CYAN, BLUE, MAGENTA, MAGENTA]
cyanBlueFour = [CYAN,CYAN, BLUE, BLUE]
coldFour = [BLUE, PURPLE, BLUE, CYAN]
coldToWarmSixteen = [BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, MAGENTA, RED, RED, RED, RED, RED, RED, RED, MAGENTA]
rainbowTwelve = [RED, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, PURPLE, BLUE, GREEN, YELLOW, ORANGE]
rainbowNine = [RED, ORANGE, YELLOW, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA]
rainbowEight = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, MAGENTA]

colorSequences = {
    'redAndBlue': redAndBlue,
    'redToBlueEight': redToBlueEight,
    'cyanBlueFour': cyanBlueFour,
    'coldFour': coldFour,
    'coldToWarmSixteen': coldToWarmSixteen,
    'rainbowTwelve':rainbowTwelve,
    'rainbowNine': rainbowNine,
    'rainbowEight': rainbowEight
}
