# encoding: utf-8

# Author: syxxzzr
# Email: syxxzzr@163.com / syxxzr@gmail.com
# License: Apache 2.0

# Offer some alias of special values.
# So that can help make your code more readable when set values which has its special meanings.


class Collisions:
    NORMAL = 'Normal'
    REVERSE = 'Reverse'


class WrapStyle:
    AUTO_RELINE = 0
    ENDING_RELINE = 1
    NO_RELINE = 2
    AUTO_RELINE_UPPER_SHORTER = 3


class ColorMatrix:
    NONE = 'None'
    TV_601 = 'TV.601'
    PC_601 = 'PC.601'
    PC_709 = 'PC.709'
    TV_709 = 'TV.709'
    PC_FCC = 'PC.FCC'
    TV_FCC = 'TV.FCC'
    PC_240M = 'PC.240M'
    TV_240M = 'TV.240M'


class BorderStyle:
    BORDER_AND_SHADOW = 1
    SOLID = 3


class Alignment:
    BOTTOM_LEFT = 1
    BOTTOM = 2
    BOTTOM_RIGHT = 3
    CENTER_LEFT = 4
    CENTER = 5
    CENTER_RIGHT = 6
    TOP_LEFT = 7
    TOP = 8
    TOP_RIGHT = 9


class Encoding:
    ANSI = 0
    DEFAULT = 1
    SYMBOL = 2
    MAC = 77
    SHIFT_JIS = 128
    HANGUL = 129
    GB2312 = 134
    BIG5 = 136
    GREEK = 161
    TURKISH = 162
    VIETNAMESE = 163
    HEBREW = 177
    ARABIC = 178
    BALTIC = 186
    RUSSIAN = 284
    THAI = 222
    EAST_EUROPEAN = 238
    OEM = 255

    JAPANESE = SHIFT_JIS
    KOREAN = HANGUL
    CHINESE = GB2312
    SIMPLIFIED_CHINESE = GB2312
    TRADITIONAL_CHINESE = BIG5
    CYRILLIC = RUSSIAN
