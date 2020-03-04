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

pixel_map = {57: {138: 101, 100: 134, 141: 100, 103: 133}, 58: {144: 99, 105: 132, 97: 135, 135: 102}, 59: {146: 98, 108: 131, 133: 103, 94: 136}, 60: {130: 104}, 61: {92: 137, 148: 97, 110: 130}, 62: {128: 105}, 63: {112: 129, 90: 138, 150: 96}, 64: {127: 106}, 65: {89: 139, 114: 128}, 66: {152: 95}, 67: {125: 107}, 68: {152: 94, 88: 140, 115: 127}, 70: {115: 126, 125: 108}, 71: {153: 93, 87: 141}, 73: {115: 125, 125: 109, 87: 142}, 74: {152: 123}, 75: {125: 110}, 76: {88: 143, 114: 124}, 77: {152: 122}, 78: {127: 111}, 79: {89: 144, 150: 121, 113: 154}, 80: {128: 112}, 81: {91: 145, 148: 120, 111: 153}, 82: {130: 113}, 83: {146: 119, 93: 146, 109: 152}, 84: {144: 118, 96: 147, 107: 151, 133: 114}, 85: {98: 148, 101: 149, 135: 115, 104: 150, 138: 116, 141: 117}, 90: {160: 70, 193: 39, 196: 38, 48: 195, 42: 197, 45: 196, 80: 164, 50: 194, 83: 163, 190: 40, 86: 162, 152: 73, 155: 72, 158: 71}, 91: {163: 69, 199: 37, 78: 165, 53: 193, 89: 161, 188: 41}, 92: {201: 36, 91: 160, 149: 74, 39: 198}, 93: {37: 199, 75: 166, 147: 75, 55: 192, 185: 42, 165: 68}, 94: {203: 35, 93: 159}, 95: {35: 200, 167: 67, 73: 167, 145: 76, 183: 43, 57: 191}, 96: {205: 34, 95: 158}, 97: {72: 168, 182: 44}, 98: {97: 157, 34: 201, 169: 66, 207: 33, 144: 77, 59: 190}, 100: {33: 202, 70: 169, 170: 65, 143: 78, 180: 45, 60: 189}, 101: {97: 156, 207: 32}, 102: {180: 46, 70: 170}, 103: {32: 203, 170: 64, 60: 188, 142: 79}, 104: {208: 31, 98: 155}, 105: {180: 47, 70: 171}, 106: {32: 204, 170: 63, 60: 187, 142: 80}, 107: {97: 185, 207: 61}, 108: {180: 48, 70: 172}, 109: {97: 184, 33: 205, 169: 62, 207: 60, 143: 81, 59: 186}, 111: {34: 206, 168: 92, 144: 82, 72: 173, 182: 49, 58: 216}, 112: {205: 59, 95: 183}, 113: {36: 207, 166: 91, 73: 174, 146: 83, 183: 50, 56: 215}, 114: {203: 58, 93: 182}, 115: {164: 90, 38: 208, 75: 175, 148: 84, 54: 214, 185: 51}, 116: {201: 57, 91: 181, 188: 52, 78: 176}, 117: {162: 89, 199: 56, 41: 209, 43: 210, 80: 177, 49: 212, 52: 213, 151: 85, 89: 180, 154: 86, 190: 53, 159: 88}, 118: {193: 54, 196: 55, 46: 211, 83: 178, 86: 179, 156: 87}, 122: {100: 320, 103: 319, 138: 349, 141: 348, 210: 10, 213: 9, 28: 225, 31: 224}, 123: {97: 321, 34: 223, 135: 350, 105: 318, 207: 11, 144: 347, 215: 8, 25: 226}, 124: {36: 222, 133: 351, 108: 317, 204: 12, 146: 346, 23: 227, 218: 7, 94: 322}, 125: {130: 352, 20: 228}, 126: {38: 221, 220: 6, 202: 13, 110: 316, 148: 345, 92: 323}, 127: {128: 353, 18: 229}, 128: {200: 14, 112: 315, 40: 220, 150: 344, 90: 324, 222: 5}, 129: {16: 230, 127: 354}, 130: {224: 4, 89: 325, 114: 314, 199: 15}, 131: {152: 343, 42: 219}, 132: {125: 355, 15: 231}, 133: {225: 3, 198: 16, 42: 218, 152: 342, 115: 313, 88: 326}, 135: {225: 2, 115: 312, 125: 356, 15: 232}, 136: {153: 341, 43: 217, 197: 17, 87: 327}, 138: {225: 1, 197: 18, 15: 233, 115: 311, 87: 328, 125: 357}, 139: {152: 371, 42: 247}, 140: {125: 358, 15: 234}, 141: {224: 0, 88: 329, 114: 310, 198: 19}, 142: {152: 370, 42: 246}, 143: {16: 235, 127: 359}, 144: {199: 20, 40: 245, 113: 340, 150: 369, 89: 330, 223: 30}, 145: {128: 360, 18: 236}, 146: {38: 244, 201: 21, 111: 339, 148: 368, 91: 331, 221: 29}, 147: {130: 361, 20: 237}, 148: {36: 243, 203: 22, 109: 338, 146: 367, 219: 28, 93: 332}, 149: {96: 333, 34: 242, 133: 362, 107: 337, 206: 23, 144: 366, 23: 238, 217: 27}, 150: {98: 334, 101: 335, 135: 363, 104: 336, 138: 364, 141: 365, 209: 24, 211: 25, 214: 26, 25: 239, 28: 240, 31: 241}, 155: {160: 380, 80: 288, 196: 410, 193: 411, 42: 259, 45: 258, 48: 257, 50: 256, 83: 287, 190: 412, 86: 286, 152: 383, 155: 382, 158: 381}, 156: {163: 379, 199: 409, 78: 289, 53: 255, 89: 285, 188: 413}, 157: {201: 408, 91: 284, 149: 384, 39: 260}, 158: {165: 378, 75: 290, 147: 385, 55: 254, 185: 414, 37: 261}, 159: {203: 407, 93: 283}, 160: {35: 262, 167: 377, 73: 291, 145: 386, 183: 415, 57: 253}, 161: {205: 406, 95: 282}, 162: {72: 292, 182: 416}, 163: {97: 281, 34: 263, 169: 376, 207: 405, 144: 387, 59: 252}, 165: {33: 264, 70: 293, 170: 375, 143: 388, 180: 417, 60: 251}, 166: {97: 280, 207: 404}, 167: {180: 418, 70: 294}, 168: {32: 265, 170: 374, 60: 250, 142: 389}, 169: {208: 403, 98: 279}, 170: {180: 419, 70: 295}, 171: {32: 266, 170: 373, 60: 249, 142: 390}, 172: {97: 309, 207: 433}, 173: {180: 420, 70: 296}, 174: {33: 267, 97: 308, 169: 372, 207: 432, 143: 391, 59: 248}, 176: {34: 268, 72: 297, 144: 392, 168: 402, 182: 421, 58: 278}, 177: {205: 431, 95: 307}, 178: {36: 269, 166: 401, 73: 298, 146: 393, 183: 422, 56: 277}, 179: {203: 430, 93: 306}, 180: {164: 400, 38: 270, 75: 299, 148: 394, 54: 276, 185: 423}, 181: {201: 429, 91: 305, 188: 424, 78: 300}, 182: {162: 399, 199: 428, 41: 271, 43: 272, 80: 301, 49: 274, 52: 275, 151: 395, 89: 304, 154: 396, 190: 425, 159: 398}, 183: {193: 426, 196: 427, 46: 273, 83: 302, 86: 303, 156: 397}}