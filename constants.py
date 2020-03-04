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

pixel_map = {57: {137: 117, 139: 116, 101: 149}, 58: {96: 151, 98: 150, 134: 118, 104: 148, 107: 147, 142: 115}, 59: {145: 114, 131: 119}, 60: {147: 113, 109: 146, 93: 152}, 61: {129: 120}, 62: {91: 153, 149: 112, 111: 145}, 63: {127: 121}, 64: {113: 144, 89: 154, 151: 111}, 66: {88: 124, 114: 143, 126: 122}, 67: {152: 110}, 68: {125: 123}, 69: {115: 142, 87: 125}, 70: {153: 109}, 71: {125: 93}, 72: {115: 141, 87: 126}, 73: {153: 108}, 74: {125: 94}, 75: {152: 107, 88: 127, 115: 140}, 77: {89: 128, 114: 139, 126: 95}, 78: {151: 106}, 79: {127: 96}, 80: {112: 138, 90: 129, 149: 105}, 81: {129: 97}, 82: {147: 104, 92: 130, 110: 137}, 83: {131: 98, 108: 136}, 84: {145: 103, 134: 99, 95: 131}, 85: {97: 132, 100: 133, 103: 134, 137: 100, 106: 135, 139: 101, 142: 102}, 90: {192: 55, 194: 54, 197: 53, 43: 212, 46: 211, 49: 210, 82: 179, 84: 178, 87: 177, 153: 88, 156: 87, 159: 86}, 91: {162: 85, 200: 52, 41: 213, 79: 180, 52: 209, 151: 89, 90: 176, 189: 56}, 92: {164: 84, 38: 214, 76: 181, 148: 90, 54: 208, 186: 57}, 93: {202: 51, 92: 175}, 94: {36: 215, 166: 83, 74: 182, 56: 207, 146: 91, 184: 58}, 95: {204: 50, 94: 174}, 96: {34: 216, 168: 82, 144: 92, 72: 183, 182: 59, 58: 206}, 97: {96: 173, 206: 49}, 98: {181: 60, 71: 184}, 99: {169: 81, 59: 205, 33: 186, 143: 62}, 100: {97: 172, 207: 48}, 101: {180: 61, 70: 185}, 102: {32: 187, 98: 171, 170: 80, 142: 63, 208: 47, 60: 204}, 104: {60: 203, 170: 79, 180: 31, 70: 155}, 105: {208: 46, 32: 188, 98: 170, 142: 64}, 107: {33: 189, 70: 156, 170: 78, 143: 65, 180: 32, 60: 202}, 108: {97: 169, 207: 45}, 109: {181: 33, 71: 157}, 110: {144: 66, 169: 77, 34: 190, 59: 201}, 111: {96: 168, 206: 44}, 112: {35: 191, 167: 76, 72: 158, 145: 67, 182: 34, 57: 200}, 113: {204: 43, 94: 167}, 114: {165: 75, 74: 159, 147: 68, 55: 199, 184: 35, 37: 192}, 115: {202: 42, 92: 166}, 116: {163: 74, 200: 41, 76: 160, 40: 193, 53: 198, 150: 69, 186: 36, 90: 165}, 117: {161: 73, 197: 40, 42: 194, 79: 161, 51: 197, 87: 164, 152: 70, 189: 37}, 118: {192: 38, 194: 39, 45: 195, 48: 196, 82: 162, 84: 163, 155: 71, 158: 72}, 122: {101: 335, 137: 365, 139: 364, 211: 25, 27: 241, 29: 240}, 123: {32: 239, 96: 337, 98: 336, 134: 366, 104: 334, 107: 333, 206: 27, 208: 26, 142: 363, 214: 24, 24: 242, 217: 23}, 124: {145: 362, 35: 238, 131: 367, 21: 243}, 125: {37: 237, 203: 28, 109: 332, 147: 361, 219: 22, 93: 338}, 126: {129: 368, 19: 244}, 127: {39: 236, 201: 29, 111: 331, 149: 360, 91: 339, 221: 21}, 128: {17: 245, 127: 369}, 129: {199: 30, 41: 235, 113: 330, 151: 359, 89: 340, 223: 20}, 131: {224: 19, 198: 0, 16: 246, 114: 329, 88: 310, 126: 370}, 132: {152: 358, 42: 234}, 133: {125: 371, 15: 247}, 134: {225: 18, 115: 328, 197: 1, 87: 311}, 135: {153: 357, 43: 233}, 136: {125: 341, 15: 217}, 137: {225: 17, 115: 327, 197: 2, 87: 312}, 138: {153: 356, 43: 232}, 139: {125: 342, 15: 218}, 140: {225: 16, 198: 3, 42: 231, 152: 355, 115: 326, 88: 313}, 142: {224: 15, 199: 4, 16: 219, 114: 325, 89: 314, 126: 343}, 143: {41: 230, 151: 354}, 144: {17: 220, 127: 344}, 145: {39: 229, 200: 5, 112: 324, 149: 353, 90: 315, 222: 14}, 146: {129: 345, 19: 221}, 147: {37: 228, 220: 13, 202: 6, 110: 323, 147: 352, 92: 316}, 148: {218: 12, 131: 346, 108: 322, 21: 222}, 149: {35: 227, 134: 347, 205: 7, 145: 351, 24: 223, 95: 317}, 150: {32: 226, 97: 318, 100: 319, 103: 320, 137: 348, 106: 321, 139: 349, 142: 350, 207: 8, 210: 9, 213: 10, 216: 11, 27: 224, 29: 225}, 155: {192: 427, 194: 426, 197: 425, 43: 274, 46: 273, 49: 272, 82: 303, 84: 302, 87: 301, 153: 398, 156: 397, 159: 396}, 156: {162: 395, 200: 424, 41: 275, 79: 304, 52: 271, 151: 399, 90: 300, 189: 428}, 157: {164: 394, 38: 276, 76: 305, 148: 400, 54: 270, 186: 429}, 158: {202: 423, 92: 299}, 159: {36: 277, 166: 393, 74: 306, 184: 430, 146: 401, 56: 269}, 160: {204: 422, 94: 298}, 161: {34: 278, 72: 307, 144: 402, 168: 392, 182: 431, 58: 268}, 162: {96: 297, 206: 421}, 163: {181: 432, 71: 308}, 164: {33: 248, 59: 267, 169: 391, 143: 372}, 165: {97: 296, 207: 420}, 166: {180: 433, 70: 309}, 167: {32: 249, 98: 295, 170: 390, 142: 373, 208: 419, 60: 266}, 169: {180: 403, 170: 389, 60: 265, 70: 279}, 170: {32: 250, 208: 418, 98: 294, 142: 374}, 172: {33: 251, 70: 280, 170: 388, 143: 375, 180: 404, 60: 264}, 173: {97: 293, 207: 417}, 174: {181: 405, 71: 281}, 175: {144: 376, 169: 387, 34: 252, 59: 263}, 176: {96: 292, 206: 416}, 177: {35: 253, 167: 386, 72: 282, 145: 377, 182: 406, 57: 262}, 178: {204: 415, 94: 291}, 179: {165: 385, 74: 283, 147: 378, 55: 261, 184: 407, 37: 254}, 180: {202: 414, 92: 290}, 181: {163: 384, 40: 255, 76: 284, 200: 413, 53: 260, 150: 379, 90: 289, 186: 408}, 182: {161: 383, 197: 412, 42: 256, 79: 285, 51: 259, 87: 288, 152: 380, 189: 409}, 183: {192: 410, 194: 411, 45: 257, 48: 258, 82: 286, 84: 287, 155: 381, 158: 382}}