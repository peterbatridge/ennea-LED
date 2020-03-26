import math
from PIL import Image 
import PIL
import pygame
import array
import time
DARK_GRAY = [25, 25, 25]
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
SIZE = (width, height) = (1100, 1200)
choices =[[255, 0, 0], [252, 3, 0], [249, 6, 0], [246, 9, 0], [243, 12, 0], [240, 15, 0], [237, 18, 0], [234, 21, 0], [231, 24, 0], [228, 27, 0], [225, 30, 0], [222, 33, 0], [219, 36, 0], [216, 39, 0], [213, 42, 0], [210, 45, 0], [207, 48, 0], [204, 51, 0], [201, 54, 0], [198, 57, 0], [195, 60, 0], [192, 63, 0], [189, 66, 0], [186, 69, 0], [183, 72, 0], [180, 75, 0], [177, 78, 0], [174, 81, 0], [171, 84, 0], [167, 88, 0], [164, 91, 0], [161, 94, 0], [158, 97, 0], [155, 100, 0], [152, 103, 0], [149, 106, 0], [146, 109, 0], [143, 112, 0], [140, 115, 0], [137, 118, 0], [134, 121, 0], [131, 124, 0], [128, 127, 0], [125, 130, 0], [122, 133, 0], [119, 136, 0], [116, 139, 0], [113, 142, 0], [110, 145, 0], [107, 148, 0], [104, 151, 0], [101, 154, 0], [98, 157, 0], [95, 160, 0], [92, 163, 0], [89, 166, 0], [86, 169, 0], [82, 173, 0], [79, 176, 0], [76, 179, 0], [73, 182, 0], [70, 185, 0], [67, 188, 0], [64, 191, 0], [61, 194, 0], [58, 197, 0], [55, 200, 0], [52, 203, 0], [49, 206, 0], [46, 209, 0], [43, 212, 0], [40, 215, 0], [37, 218, 0], [34, 221, 0], [31, 224, 0], [28, 227, 0], [25, 230, 0], [22, 233, 0], [19, 236, 0], [16, 239, 0], [13, 242, 0], [10, 245, 0], [7, 248, 0], [4, 251, 0], [0, 0, 0], [0, 253, 2], [0, 250, 5], [0, 247, 8], [0, 244, 11], [0, 241, 14], [0, 238, 17], [0, 235, 20], [0, 232, 23], [0, 229, 26], [0, 226, 29], [0, 223, 32], [0, 220, 35], [0, 217, 38], [0, 214, 41], [0, 211, 44], [0, 208, 47], [0, 205, 50], [0, 202, 53], [0, 199, 56], [0, 196, 59], [0, 193, 62], [0, 190, 65], [0, 187, 68], [0, 184, 71], [0, 181, 74], [0, 178, 77], [0, 175, 80], [0, 172, 83], [0, 168, 87], [0, 165, 90], [0, 162, 93], [0, 159, 96], [0, 156, 99], [0, 153, 102], [0, 150, 105], [0, 147, 108], [0, 144, 111], [0, 141, 114], [0, 138, 117], [0, 135, 120], [0, 132, 123], [0, 129, 126], [0, 126, 129], [0, 123, 132], [0, 120, 135], [0, 117, 138], [0, 114, 141], [0, 111, 144], [0, 108, 147], [0, 105, 150], [0, 102, 153], [0, 99, 156], [0, 96, 159], [0, 93, 162], [0, 90, 165], [0, 87, 168], [0, 83, 172], [0, 80, 175], [0, 77, 178], [0, 74, 181], [0, 71, 184], [0, 68, 187], [0, 65, 190], [0, 62, 193], [0, 59, 196], [0, 56, 199], [0, 53, 202], [0, 50, 205], [0, 47, 208], [0, 44, 211], [0, 41, 214], [0, 38, 217], [0, 35, 220], [0, 32, 223], [0, 29, 226], [0, 26, 229], [0, 23, 232], [0, 20, 235], [0, 17, 238], [0, 14, 241], [0, 11, 244], [0, 8, 247], [0, 5, 250], [0, 2, 253], [1, 0, 254], [4, 0, 251], [7, 0, 248], [10, 0, 245], [13, 0, 242], [16, 0, 239], [19, 0, 236], [22, 0, 233], [25, 0, 230], [28, 0, 227], [31, 0, 224], [34, 0, 221], [37, 0, 218], [40, 0, 215], [43, 0, 212], [46, 0, 209], [49, 0, 206], [52, 0, 203], [55, 0, 200], [58, 0, 197], [61, 0, 194], [64, 0, 191], [67, 0, 188], [70, 0, 185], [73, 0, 182], [76, 0, 179], [79, 0, 176], [82, 0, 173], [86, 0, 169], [89, 0, 166], [92, 0, 163], [95, 0, 160], [98, 0, 157], [101, 0, 154], [104, 0, 151], [107, 0, 148], [110, 0, 145], [113, 0, 142], [116, 0, 139], [119, 0, 136], [122, 0, 133], [125, 0, 130], [128, 0, 127], [131, 0, 124], [134, 0, 121], [137, 0, 118], [140, 0, 115], [143, 0, 112], [146, 0, 109], [149, 0, 106], [152, 0, 103], [155, 0, 100], [158, 0, 97], [161, 0, 94], [164, 0, 91], [167, 0, 88], [171, 0, 84], [174, 0, 81], [177, 0, 78], [180, 0, 75], [183, 0, 72], [186, 0, 69], [189, 0, 66], [192, 0, 63], [195, 0, 60], [198, 0, 57], [201, 0, 54], [204, 0, 51], [207, 0, 48], [210, 0, 45], [213, 0, 42], [216, 0, 39], [219, 0, 36], [222, 0, 33], [225, 0, 30], [228, 0, 27], [231, 0, 24], [234, 0, 21], [237, 0, 18], [240, 0, 15], [243, 0, 12], [246, 0, 9], [249, 0, 6], [252, 0, 3], [0, 0, 255]]
# Generated from getMapping()
pixel_map = {23: {57: 116, 58: 117, 43: 149, 42: 148}, 24: {39: 146, 40: 147, 44: 150, 45: 151, 55: 114, 56: 115, 59: 118, 60: 119}, 25: {37: 144, 38: 145, 46: 152, 53: 112, 54: 113, 61: 120}, 26: {52: 111, 37: 143, 62: 121, 47: 153}, 27: {36: 142, 47: 154, 52: 110, 63: 122}, 28: {47: 124, 36: 141, 63: 123}, 29: {48: 125, 52: 109, 63: 93}, 30: {36: 140, 52: 108, 63: 94}, 31: {36: 139, 52: 107, 47: 126}, 32: {47: 127, 52: 106, 37: 138, 63: 95}, 33: {37: 137, 46: 128, 61: 97, 62: 96, 53: 105}, 34: {38: 136, 39: 135, 45: 130, 46: 129, 54: 104, 55: 103, 60: 98}, 35: {40: 134, 41: 133, 42: 132, 44: 131, 56: 102, 57: 101, 58: 100, 59: 99}, 37: {19: 210, 65: 86, 66: 87, 67: 88, 36: 180, 16: 208, 33: 177, 18: 209, 34: 178, 79: 53, 80: 54, 81: 55, 82: 56, 35: 179, 20: 211, 21: 212, 62: 84, 63: 85}, 38: {32: 176, 68: 89, 38: 181, 77: 51, 78: 52, 15: 207, 83: 57, 22: 213, 61: 83, 31: 175}, 39: {69: 90, 38: 182, 39: 183, 76: 50, 14: 206, 84: 58, 85: 59, 23: 214, 60: 82, 30: 174}, 40: {70: 91, 40: 184, 75: 49, 14: 205, 86: 60, 24: 215, 60: 81, 29: 173}, 41: {70: 92, 75: 48, 13: 204, 24: 216, 59: 80, 29: 172}, 42: {70: 62, 40: 185, 74: 47, 13: 203, 86: 61, 25: 186, 59: 79, 29: 171}, 43: {70: 63, 40: 155, 74: 46, 13: 202, 86: 31, 25: 187, 59: 78, 29: 170}, 44: {70: 64, 40: 156, 13: 201, 86: 32, 24: 188, 59: 77}, 45: {70: 65, 40: 157, 75: 45, 14: 200, 86: 33, 24: 189, 59: 76, 29: 169}, 46: {69: 66, 39: 158, 75: 44, 14: 199, 85: 34, 24: 190, 60: 75, 29: 168}, 47: {69: 67, 38: 159, 76: 43, 77: 42, 15: 198, 84: 35, 23: 191, 61: 74, 30: 167, 31: 166}, 48: {32: 165, 33: 164, 67: 69, 68: 68, 38: 160, 78: 41, 79: 40, 16: 197, 17: 196, 82: 37, 83: 36, 21: 193, 22: 192, 36: 161, 62: 73, 63: 72}, 49: {64: 71, 65: 70, 34: 163, 35: 162, 80: 39, 81: 38, 18: 195, 20: 194}, 50: {57: 364, 42: 334, 11: 240, 87: 24}, 51: {59: 366, 39: 332, 40: 333, 9: 238, 10: 239, 43: 335, 12: 241, 45: 337, 14: 242, 15: 243, 58: 365, 85: 22, 86: 23, 55: 362, 56: 363, 89: 25, 90: 26, 91: 27, 60: 367, 44: 336}, 52: {37: 330, 38: 331, 8: 237, 46: 338, 16: 244, 83: 20, 84: 21, 54: 361, 92: 28, 61: 368}, 53: {37: 329, 6: 235, 7: 236, 47: 339, 16: 245, 83: 19, 52: 359, 53: 360, 92: 29, 62: 369}, 54: {36: 328, 47: 340, 17: 246, 82: 18, 93: 30, 63: 370}, 55: {6: 234, 47: 310, 17: 247, 52: 358, 93: 0, 63: 371}, 56: {36: 327, 6: 233, 48: 311, 17: 217, 82: 17, 52: 357, 93: 1, 63: 341}, 57: {36: 326, 6: 232, 17: 218, 82: 16, 52: 356, 63: 342}, 58: {36: 325, 6: 231, 47: 312, 82: 15, 52: 355, 93: 2}, 59: {37: 324, 6: 230, 47: 313, 17: 219, 82: 14, 52: 354, 93: 3, 63: 343}, 60: {37: 323, 7: 229, 46: 314, 16: 220, 83: 13, 53: 353, 92: 4, 62: 344}, 61: {38: 322, 39: 321, 8: 228, 45: 316, 46: 315, 15: 222, 16: 221, 84: 12, 85: 11, 54: 352, 91: 6, 60: 346, 61: 345}, 62: {40: 320, 9: 227, 10: 226, 11: 225, 12: 224, 14: 223, 44: 317, 56: 350, 57: 349, 41: 319, 86: 10, 87: 9, 88: 8, 89: 7, 58: 348, 59: 347, 42: 318, 55: 351}, 64: {33: 301, 34: 302, 35: 303, 36: 304, 65: 396, 82: 428, 67: 398, 66: 397, 79: 425, 80: 426, 81: 427, 18: 271, 19: 272, 20: 273, 21: 274, 63: 395}, 65: {32: 300, 68: 399, 38: 305, 77: 423, 78: 424, 15: 269, 16: 270, 83: 429, 22: 275, 61: 393, 62: 394, 31: 299}, 66: {69: 400, 38: 306, 76: 422, 14: 268, 84: 430, 23: 276, 60: 392, 30: 298}, 67: {70: 401, 39: 307, 75: 421, 14: 267, 85: 431, 24: 277, 60: 391, 29: 297}, 68: {70: 402, 40: 308, 75: 420, 13: 266, 86: 432, 24: 278, 59: 390, 29: 296}, 69: {70: 372, 40: 309, 74: 419, 13: 265, 86: 433, 25: 248, 59: 389, 29: 295}, 70: {70: 373, 40: 279, 74: 418, 13: 264, 86: 403, 25: 249, 59: 388, 29: 294}, 71: {70: 374, 40: 280, 13: 263, 86: 404, 24: 250, 59: 387}, 72: {70: 375, 40: 281, 75: 417, 86: 405, 24: 251, 29: 293}, 73: {69: 376, 39: 282, 75: 416, 14: 262, 85: 406, 24: 252, 59: 386, 29: 292}, 74: {69: 377, 38: 283, 76: 415, 77: 414, 14: 261, 15: 260, 84: 407, 23: 253, 60: 385, 61: 384, 30: 291, 31: 290}, 75: {32: 289, 67: 379, 36: 285, 38: 284, 78: 413, 16: 259, 17: 258, 82: 409, 83: 408, 21: 255, 22: 254, 68: 378, 62: 383, 63: 382}, 76: {64: 381, 33: 288, 34: 287, 35: 286, 65: 380, 79: 412, 80: 411, 81: 410, 18: 257, 20: 256}}
pmap = {0: [55, 93], 1: [56, 93], 2: [58, 93], 3: [59, 93], 4: [60, 92], 5: [61, 91], 6: [61, 91], 7: [62, 89], 8: [62, 88], 9: [62, 87], 10: [62, 86], 11: [61, 85], 12: [61, 84], 13: [60, 83], 14: [59, 82], 15: [58, 82], 16: [57, 82], 17: [56, 82], 18: [54, 82], 19: [53, 83], 20: [52, 83], 21: [52, 84], 22: [51, 85], 23: [51, 86], 24: [50, 87], 25: [51, 89], 26: [51, 90], 27: [51, 91], 28: [52, 92], 29: [53, 92], 30: [54, 93], 31: [43, 86], 32: [44, 86], 33: [45, 86], 34: [46, 85], 35: [47, 84], 36: [48, 83], 37: [48, 82], 38: [49, 81], 39: [49, 80], 40: [48, 79], 41: [48, 78], 42: [47, 77], 43: [47, 76], 44: [46, 75], 45: [45, 75], 46: [43, 74], 47: [42, 74], 48: [41, 75], 49: [40, 75], 50: [39, 76], 51: [38, 77], 52: [38, 78], 53: [37, 79], 54: [37, 80], 55: [37, 81], 56: [37, 82], 57: [38, 83], 58: [39, 84], 59: [39, 85], 60: [40, 86], 61: [42, 86], 62: [42, 70], 63: [43, 70], 64: [44, 70], 65: [45, 70], 66: [46, 69], 67: [47, 69], 68: [48, 68], 69: [48, 67], 70: [49, 65], 71: [49, 64], 72: [48, 63], 73: [48, 62], 74: [47, 61], 75: [46, 60], 76: [45, 59], 77: [44, 59], 78: [43, 59], 79: [42, 59], 80: [41, 59], 81: [40, 60], 82: [39, 60], 83: [38, 61], 84: [37, 62], 85: [37, 63], 86: [37, 65], 87: [37, 66], 88: [37, 67], 89: [38, 68], 90: [39, 69], 91: [40, 70], 92: [41, 70], 93: [29, 63], 94: [30, 63], 95: [32, 63], 96: [33, 62], 97: [33, 61], 98: [34, 60], 99: [35, 59], 100: [35, 58], 101: [35, 57], 102: [35, 56], 103: [34, 55], 104: [34, 54], 105: [33, 53], 106: [32, 52], 107: [31, 52], 108: [30, 52], 109: [29, 52], 110: [27, 52], 111: [26, 52], 112: [25, 53], 113: [25, 54], 114: [24, 55], 115: [24, 56], 116: [23, 57], 117: [23, 58], 118: [24, 59], 119: [24, 60], 120: [25, 61], 121: [26, 62], 122: [27, 63], 123: [28, 63], 124: [28, 47], 125: [29, 48], 126: [31, 47], 127: [32, 47], 128: [33, 46], 129: [34, 46], 130: [34, 45], 131: [35, 44], 132: [35, 42], 133: [35, 41], 134: [35, 40], 135: [34, 39], 136: [34, 38], 137: [33, 37], 138: [32, 37], 139: [31, 36], 140: [30, 36], 141: [28, 36], 142: [27, 36], 143: [26, 37], 144: [25, 37], 145: [25, 38], 146: [24, 39], 147: [24, 40], 148: [23, 42], 149: [23, 43], 150: [24, 44], 151: [24, 45], 152: [25, 46], 153: [26, 47], 154: [27, 47], 155: [43, 40], 156: [44, 40], 157: [45, 40], 158: [46, 39], 159: [47, 38], 160: [48, 38], 161: [48, 36], 162: [49, 35], 163: [49, 34], 164: [48, 33], 165: [48, 32], 166: [47, 31], 167: [47, 30], 168: [46, 29], 169: [45, 29], 170: [43, 29], 171: [42, 29], 172: [41, 29], 173: [40, 29], 174: [39, 30], 175: [38, 31], 176: [38, 32], 177: [37, 33], 178: [37, 34], 179: [37, 35], 180: [37, 36], 181: [38, 38], 182: [39, 38], 183: [39, 39], 184: [40, 40], 185: [42, 40], 186: [42, 25], 187: [43, 25], 188: [44, 24], 189: [45, 24], 190: [46, 24], 191: [47, 23], 192: [48, 22], 193: [48, 21], 194: [49, 20], 195: [49, 18], 196: [48, 17], 197: [48, 16], 198: [47, 15], 199: [46, 14], 200: [45, 14], 201: [44, 13], 202: [43, 13], 203: [42, 13], 204: [41, 13], 205: [40, 14], 206: [39, 14], 207: [38, 15], 208: [37, 16], 209: [37, 18], 210: [37, 19], 211: [37, 20], 212: [37, 21], 213: [38, 22], 214: [39, 23], 215: [40, 24], 216: [41, 24], 217: [56, 17], 218: [57, 17], 219: [59, 17], 220: [60, 16], 221: [61, 16], 222: [61, 15], 223: [62, 14], 224: [62, 12], 225: [62, 11], 226: [62, 10], 227: [62, 9], 228: [61, 8], 229: [60, 7], 230: [59, 6], 231: [58, 6], 232: [57, 6], 233: [56, 6], 234: [55, 6], 235: [53, 6], 236: [53, 7], 237: [52, 8], 238: [51, 9], 239: [51, 10], 240: [50, 11], 241: [51, 12], 242: [51, 14], 243: [51, 15], 244: [52, 16], 245: [53, 16], 246: [54, 17], 247: [55, 17], 248: [69, 25], 249: [70, 25], 250: [71, 24], 251: [72, 24], 252: [73, 24], 253: [74, 23], 254: [75, 22], 255: [75, 21], 256: [76, 20], 257: [76, 18], 258: [75, 17], 259: [75, 16], 260: [74, 15], 261: [74, 14], 262: [73, 14], 263: [71, 13], 264: [70, 13], 265: [69, 13], 266: [68, 13], 267: [67, 14], 268: [66, 14], 269: [65, 15], 270: [65, 16], 271: [64, 18], 272: [64, 19], 273: [64, 20], 274: [64, 21], 275: [65, 22], 276: [66, 23], 277: [67, 24], 278: [68, 24], 279: [70, 40], 280: [71, 40], 281: [72, 40], 282: [73, 39], 283: [74, 38], 284: [75, 38], 285: [75, 36], 286: [76, 35], 287: [76, 34], 288: [76, 33], 289: [75, 32], 290: [74, 31], 291: [74, 30], 292: [73, 29], 293: [72, 29], 294: [70, 29], 295: [69, 29], 296: [68, 29], 297: [67, 29], 298: [66, 30], 299: [65, 31], 300: [65, 32], 301: [64, 33], 302: [64, 34], 303: [64, 35], 304: [64, 36], 305: [65, 38], 306: [66, 38], 307: [67, 39], 308: [68, 40], 309: [69, 40], 310: [55, 47], 311: [56, 48], 312: [58, 47], 313: [59, 47], 314: [60, 46], 315: [61, 46], 316: [61, 45], 317: [62, 44], 318: [62, 42], 319: [62, 41], 320: [62, 40], 321: [61, 39], 322: [61, 38], 323: [60, 37], 324: [59, 37], 325: [58, 36], 326: [57, 36], 327: [56, 36], 328: [54, 36], 329: [53, 37], 330: [52, 37], 331: [52, 38], 332: [51, 39], 333: [51, 40], 334: [50, 42], 335: [51, 43], 336: [51, 44], 337: [51, 45], 338: [52, 46], 339: [53, 47], 340: [54, 47], 341: [56, 63], 342: [57, 63], 343: [59, 63], 344: [60, 62], 345: [61, 61], 346: [61, 60], 347: [62, 59], 348: [62, 58], 349: [62, 57], 350: [62, 56], 351: [62, 55], 352: [61, 54], 353: [60, 53], 354: [59, 52], 355: [58, 52], 356: [57, 52], 357: [56, 52], 358: [55, 52], 359: [53, 52], 360: [53, 53], 361: [52, 54], 362: [51, 55], 363: [51, 56], 364: [50, 57], 365: [51, 58], 366: [51, 59], 367: [51, 60], 368: [52, 61], 369: [53, 62], 370: [54, 63], 371: [55, 63], 372: [69, 70], 373: [70, 70], 374: [71, 70], 375: [72, 70], 376: [73, 69], 377: [74, 69], 378: [75, 68], 379: [75, 67], 380: [76, 65], 381: [76, 64], 382: [75, 63], 383: [75, 62], 384: [74, 61], 385: [74, 60], 386: [73, 59], 387: [71, 59], 388: [70, 59], 389: [69, 59], 390: [68, 59], 391: [67, 60], 392: [66, 60], 393: [65, 61], 394: [65, 62], 395: [64, 63], 396: [64, 65], 397: [64, 66], 398: [64, 67], 399: [65, 68], 400: [66, 69], 401: [67, 70], 402: [68, 70], 403: [70, 86], 404: [71, 86], 405: [72, 86], 406: [73, 85], 407: [74, 84], 408: [75, 83], 409: [75, 82], 410: [76, 81], 411: [76, 80], 412: [76, 79], 413: [75, 78], 414: [74, 77], 415: [74, 76], 416: [73, 75], 417: [72, 75], 418: [70, 74], 419: [69, 74], 420: [68, 75], 421: [67, 75], 422: [66, 76], 423: [65, 77], 424: [65, 78], 425: [64, 79], 426: [64, 80], 427: [64, 81], 428: [64, 82], 429: [65, 83], 430: [66, 84], 431: [67, 85], 432: [68, 86], 433: [69, 86]}

def isGray(color):
    return (color[0]*color[1]*color[2] < 2097152 and color[0] > color[1]-10 and color[0] < color[1]+10 and color[1] > color[2] - 10 and color[1] < color[2]+10)

def isWhite(color):
    return (color[0]*color[1]*color[2] >= 2097152 and color[0] > color[1]-10 and color[0] < color[1]+10 and color[1] > color[2] - 10 and color[1] < color[2]+10)

def remapToLarge(value):
    return int((value / 253.0)*768)

def remapToSmall(value):
    return int((value / 768)* 253)

def wheel(num):
    if num == 255:
        return [255,255,255]
    elif num == 254:
        return [0,0,0]
    r =0
    g =0
    b = 0
    c = int(num/256)
    if c == 0:
        r = 255 - (num%256)
        g = num % 256
        b = 0
    elif c == 1:
        g = 255 - (num%256)
        b = num % 256
        r = 0
    else:
        b = 255 - (num%256)
        r = num % 256
        g = 0
    return [r,g,b]


def closest(color):
    selection = BLANK 
    d=200000
    if isGray(color):
        print("return 254")
        return 254
    if isWhite(color):
        return 255
    for i in range(0, len(choices)):
        n = (color[0]-choices[i][0])**2 + (color[1]-choices[i][1])**2 + (color[2]-choices[i][2])**2
        if n < d:
            d = n
            selection = i
    return selection

def convertGifToAnimation():
    newImages = []
    f = open("gif.txt", "w")
    im = Image.open("rainbowaligningcircles.gif")
    print(im.n_frames)
    animation = []
    for z in range(im.n_frames):
        strip = [254] * 434
        im.seek(z) 
        rgb_im = im.convert('RGB')
        rgb_im = rgb_im.resize((100,100), PIL.Image.LANCZOS)
        # new = Image.new( 'RGB', (rgb_im.size[0],rgb_im.size[1]), "black")
        # newMap = new.load()
        # for x in range(rgb_im.size[0]):
        #     for y in range(rgb_im.size[1]):
        #         newMap[x, y] = tuple(wheel(remapToLarge(closest(rgb_im.getpixel((x,y))))))
        # newImages.append(new)
        for x in pixel_map:
            for y in pixel_map[x]:
                p = pixel_map[x][y]
                color = closest(rgb_im.getpixel((x, y)))
                strip[p] = color
        animation.append(array.array('B', strip))
    # newImages[0].save('redraw.gif',
    #            save_all=True, append_images=newImages[1:], optimize=False, duration=20, loop=0)
    f.write(str(animation))
    f.close()
    return animation

def drawImage():
    im = Image.open("cube.png") 
    px = im.load() 
    for x in pixel_map:
        for y in pixel_map[x]:
            color = px[x,y]
            drawCircle((x,y), px[x,y])
    pygame.display.update()

def drawAnimation(animation):
    for s in range(0,len(animation)):
        for p in range(0, 434):
            drawCircle(pmap[p], animation[s][p])
        pygame.display.update()
        time.sleep(0.1)

def drawCircle(position, color):
    pygame.draw.circle(screen, color, position, 1)

def main():
    global screen, height, width
    pygame.init()
    pygame.display.set_caption("CTA")
    
    screen = pygame.display.set_mode(SIZE)    

    for x in range(1,149):
        pygame.draw.line(screen, DARK_GRAY, (0, (x*10)+5), (1499, (x*10)+5))
        pygame.draw.line(screen, DARK_GRAY, ((x*10)+5, 0), ((x*10)+5, 1499))

    running = True
    anim = convertGifToAnimation()
    print(anim)
    while running:
        drawAnimation(anim)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
     

def getMapping():
    pixel_map = {}
    pmap = {}

    #Center of LED circles in inches from the bottom left of the board.
    centers = {
        0: [13.625, 2.874],
        1: [10.375, 4.624],
        2: [10.375, 8.375],
        3: [7.125, 10.125],
        4: [7.125, 13.876],
        5: [10.375, 15.625],
        6: [10.375, 19.376],
        7: [13.625, 21.126],
        8: [16.875, 19.376],
        9: [16.875, 15.625],
        10: [13.625, 13.876],
        11: [13.625, 10.125],
        12: [16.875, 8.375],
        13: [16.875, 4.624]
    }

    # Radius in inches
    radius = 1.4

    for c in centers:
        for i in range(0, 31):
            offset = 0 
            if c % 2 == 0:
                offset = -(1.0/18) * math.pi
            xpos = int(round((25.0/6 * (centers[c][0] + radius * math.sin((2*i*math.pi/31)+offset))), 1))
            ypos = int(round((25.0/6 * (24.0 - centers[c][1] + radius * math.cos((2*i*math.pi/31)+offset))),1))
            pmap[c*31+i] = [xpos, ypos]
            print(c*31+i, round(xpos,3), round(ypos,3))
            try:
                pixel_map[xpos][ypos] = c*31+i
            except KeyError:
                pixel_map[xpos] = {ypos: c*31+i}
    print(pixel_map)
    print(pmap)
#getMapping()
convertGifToAnimation()
# mapped = []
# for i in range(253):
#     mapped.append(wheel(remapToLarge(i)))
#     print(remapToLarge(i), i)
# print(mapped)
# if __name__=="__main__":
#     main()

