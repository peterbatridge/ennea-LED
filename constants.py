RED = [255, 0, 0]
YELLOW = [255, 150, 0]
ORANGE = [255, 40, 0]
GREEN = [0, 255, 0]
TEAL = [0, 255, 120]
CYAN = [0, 255, 255]
BLUE = [0, 0, 255]
PURPLE = [180, 0, 255]
MAGENTA = [255, 0, 20]
WHITE = [255, 255, 255]
BLANK = [0, 0, 0]
colors = [RED, ORANGE, YELLOW, GREEN, TEAL, CYAN,  BLUE, PURPLE, MAGENTA]
colorsDict = {
    'Red': RED,
    'Yellow': YELLOW,
    'Orange': ORANGE,
    'Green': GREEN,
    'Teal': TEAL,
    'Cyan': CYAN,
    'Blue': BLUE,
    'Purple': PURPLE,
    'Magenta': MAGENTA,
    'White': WHITE,
    'Blank': BLANK
}
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

###
# Audio Mappings
###
individualLeds = [[50,75], [75, 250], [250, 400], [1024, 433]] 
verticalSides = [[50,25], [75, 30], [250, 35], [1024, 39]] 
verticalNonagons = [[50,4], [75, 5], [250, 6], [1024, 7]] 

audioMappings = {
    'individualLeds': individualLeds,
    'verticalSides': verticalSides,
    'verticalNonagons': verticalNonagons
}

pixel_map = {57: {104: 149, 138: 116, 141: 117, 101: 148}, 58: {144: 118, 98: 147, 106: 150, 135: 115}, 59: {146: 119, 133: 114, 95: 146}, 60: {130: 113, 93: 145, 109: 151}, 61: {148: 120, 111: 152}, 62: {128: 112, 91: 144}, 63: {150: 121}, 64: {89: 143, 113: 153, 127: 111}, 66: {152: 122, 114: 154}, 67: {88: 142, 125: 110}, 68: {152: 123}, 69: {115: 124, 87: 141}, 70: {125: 109}, 71: {153: 93}, 72: {115: 125, 87: 140}, 73: {125: 108}, 74: {152: 94, 115: 126}, 75: {88: 139, 125: 107}, 77: {152: 95, 114: 127}, 78: {89: 138, 127: 106}, 79: {150: 96}, 80: {128: 105, 113: 128, 90: 137}, 81: {148: 97}, 82: {130: 104, 92: 136, 111: 129}, 83: {146: 98, 108: 130}, 84: {144: 99, 133: 103, 95: 135}, 85: {97: 134, 100: 133, 103: 132, 138: 101, 135: 102, 141: 100, 106: 131}, 90: {193: 54, 196: 55, 43: 209, 46: 210, 80: 177, 49: 211, 83: 178, 86: 179, 153: 85, 156: 86, 190: 53, 159: 87}, 91: {161: 88, 199: 56, 40: 208, 78: 176, 51: 212, 150: 84, 89: 180, 188: 52}, 92: {164: 89, 38: 207, 201: 57, 148: 83, 54: 213, 91: 181}, 93: {185: 51, 75: 175}, 94: {36: 206, 166: 90, 203: 58, 146: 82, 56: 214, 93: 182}, 95: {73: 174, 183: 50}, 96: {168: 91, 58: 215, 205: 59, 95: 183}, 97: {144: 81, 72: 173, 34: 205, 182: 49}, 98: {97: 184, 207: 60}, 99: {169: 92, 59: 216, 33: 204, 143: 80}, 100: {180: 48, 70: 172}, 101: {97: 185, 170: 62, 60: 186, 207: 61}, 102: {32: 203, 180: 47, 70: 171, 142: 79}, 104: {208: 31, 170: 63, 60: 187, 98: 155}, 105: {32: 202, 180: 46, 70: 170, 142: 78}, 107: {97: 156, 170: 64, 60: 188, 207: 32}, 108: {33: 201, 180: 45, 70: 169, 143: 77}, 109: {97: 157, 207: 33}, 110: {144: 76, 169: 65, 34: 200, 59: 189}, 111: {72: 168, 182: 44}, 112: {168: 66, 58: 190, 205: 34, 95: 158}, 113: {145: 75, 35: 199, 73: 167, 183: 43}, 114: {56: 191, 203: 35, 93: 159, 166: 67}, 115: {185: 42, 75: 166, 147: 74, 37: 198}, 116: {163: 68, 40: 197, 201: 36, 78: 165, 53: 192, 150: 73, 91: 160, 188: 41}, 117: {161: 69, 199: 37, 42: 196, 80: 164, 51: 193, 152: 72, 89: 161, 190: 40}, 118: {193: 39, 196: 38, 45: 195, 48: 194, 83: 163, 86: 162, 155: 71, 158: 70}, 122: {101: 334, 104: 335, 138: 364, 141: 365, 211: 24, 214: 25, 28: 240, 31: 241}, 123: {144: 366, 34: 242, 135: 363, 106: 336, 98: 333, 208: 23, 216: 26, 25: 239}, 124: {36: 243, 133: 362, 205: 22, 146: 367, 23: 238, 95: 332}, 125: {130: 361, 203: 21, 109: 337, 20: 237, 219: 27, 93: 331}, 126: {148: 368, 221: 28, 38: 244, 111: 338}, 127: {128: 360, 201: 20, 18: 236, 91: 330}, 128: {40: 245, 150: 369}, 129: {199: 19, 16: 235, 113: 339, 89: 329, 127: 359, 223: 29}, 131: {224: 30, 152: 370, 42: 246, 114: 340}, 132: {88: 328, 125: 358, 198: 18, 15: 234}, 133: {152: 371, 42: 247}, 134: {225: 0, 115: 310, 197: 17, 87: 327}, 135: {125: 357, 15: 233}, 136: {153: 341, 43: 217}, 137: {225: 1, 115: 311, 197: 16, 87: 326}, 138: {125: 356, 15: 232}, 139: {152: 342, 225: 2, 42: 218, 115: 312}, 140: {88: 325, 125: 355, 198: 15, 15: 231}, 142: {224: 3, 152: 343, 42: 219, 114: 313}, 143: {16: 230, 89: 324, 127: 354, 199: 14}, 144: {40: 220, 150: 344}, 145: {128: 353, 200: 13, 113: 314, 18: 229, 90: 323, 223: 4}, 146: {148: 345, 38: 221}, 147: {130: 352, 202: 12, 111: 315, 20: 228, 92: 322, 221: 5}, 148: {108: 316, 218: 6, 36: 222, 146: 346}, 149: {34: 223, 133: 351, 205: 11, 144: 347, 23: 227, 95: 321}, 150: {97: 320, 100: 319, 103: 318, 106: 317, 135: 350, 141: 348, 207: 10, 210: 9, 213: 8, 216: 7, 25: 226, 28: 225, 138: 349, 31: 224}, 155: {193: 426, 196: 427, 43: 271, 46: 272, 80: 301, 49: 273, 83: 302, 86: 303, 153: 395, 156: 396, 190: 425, 159: 397}, 156: {161: 398, 199: 428, 40: 270, 78: 300, 51: 274, 150: 394, 89: 304, 188: 424}, 157: {164: 399, 38: 269, 201: 429, 148: 393, 54: 275, 91: 305}, 158: {185: 423, 75: 299}, 159: {36: 268, 166: 400, 203: 430, 146: 392, 56: 276, 93: 306}, 160: {73: 298, 183: 422}, 161: {168: 401, 58: 277, 205: 431, 95: 307}, 162: {72: 297, 144: 391, 34: 267, 182: 421}, 163: {97: 308, 207: 432}, 164: {33: 266, 59: 278, 169: 402, 143: 390}, 165: {180: 420, 70: 296}, 166: {97: 309, 170: 372, 60: 248, 207: 433}, 167: {32: 265, 180: 419, 142: 389, 70: 295}, 169: {208: 403, 98: 279, 60: 249, 170: 373}, 170: {32: 264, 180: 418, 142: 388, 70: 294}, 172: {97: 280, 170: 374, 60: 250, 207: 404}, 173: {33: 263, 180: 417, 70: 293, 143: 387}, 174: {97: 281, 207: 405}, 175: {144: 386, 169: 375, 34: 262, 59: 251}, 176: {72: 292, 182: 416}, 177: {168: 376, 58: 252, 205: 406, 95: 282}, 178: {73: 291, 35: 261, 183: 415, 145: 385}, 179: {56: 253, 203: 407, 93: 283, 166: 377}, 180: {185: 414, 75: 290, 147: 384, 37: 260}, 181: {163: 378, 40: 259, 201: 408, 78: 289, 53: 254, 150: 383, 91: 284, 188: 413}, 182: {161: 379, 199: 409, 42: 258, 80: 288, 51: 255, 152: 382, 89: 285, 190: 412}, 183: {193: 411, 196: 410, 45: 257, 48: 256, 83: 287, 86: 286, 155: 381, 158: 380}}
