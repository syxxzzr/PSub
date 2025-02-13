# encoding: utf-8

# Author: syxxzzr
# Email: syxxzzr@163.com / syxxzr@gmail.com
# License: Apache 2.0

from utils import *


class Name(Section):
    __section_name = 'Name'


class FontName(Section):
    __section_name = 'Fontname'


class BorderStyle(Section, IntPaser):
    __section_name = 'BorderStyle'


class Alignment(Section, IntPaser):
    __section_name = 'Alignment'


class MarginL(Section, IntPaser):
    __section_name = 'MarginL'


class MarginR(Section, IntPaser):
    __section_name = 'MarginR'


class MarginV(Section, IntPaser):
    __section_name = 'MarginV'


class Encoding(Section, IntPaser):
    __section_name = 'Encoding'


class FontSize(Section, FloatPaser):
    __section_name = 'Fontsize'


class ScaleX(Section, FloatPaser):
    __section_name = 'ScaleX'


class ScaleY(Section, FloatPaser):
    __section_name = 'ScaleY'


class Spacing(Section, FloatPaser):
    __section_name = 'Spacing'


class Angle(Section, FloatPaser):
    __section_name = 'Angle'


class Outline(Section, FloatPaser):
    __section_name = 'Outline'


class Shadow(Section, FloatPaser):
    __section_name = 'Shadow'


class Bold(Section, ThreeOptionPaser):
    __section_name = 'Bold'


class Italic(Section, ThreeOptionPaser):
    __section_name = 'Italic'


class Underline(Section, ThreeOptionPaser):
    __section_name = 'Underline'


class StrikeOut(Section, ThreeOptionPaser):
    __section_name = 'StrikeOut'


class PrimaryColor(Section, ColorPaser):
    __section_name = 'PrimaryColor'


class SecondaryColor(Section, ColorPaser):
    __section_name = 'SecondaryColor'


class OutlineColor(Section, ColorPaser):
    __section_name = 'OutlineColor'


class BackgroundColor(Section, ColorPaser):
    __section_name = 'BackColor'
