# encoding: utf-8

# Author: syxxzzr
# Email: syxxzzr@163.com / syxxzr@gmail.com
# License: Apache 2.0

from utils import *


class Title(Section):
    __section_name = 'Title'


class ScriptType(Section):
    __section_name = 'ScriptType'


class Translator(Section):
    __section_name = 'Original Translation'


class Scriptor(Section):
    __section_name = 'Original Script'


class Editor(Section):
    __section_name = 'Original Editing'


class Timeliner(Section):
    __section_name = 'Original Timing'


class Updator(Section):
    __section_name = 'Script Updated By'


class UpdateDetails(Section):
    __section_name = 'Update Details'


class Collisions(Section):
    __section_name = 'Collisions'


class ColorMatrix(Section):
    __section_name = 'YCbCr Matrix'


class PlayRate(Section, FloatPaser):
    __section_name = 'Timer'


class SynchPoint(Section, FloatPaser):
    __section_name = 'Synch Point'


class ReferenceX(Section, IntPaser):
    __section_name = 'PlayResX'


class ReferenceY(Section, IntPaser):
    __section_name = 'PlayResY'


class ColorDepth(Section, IntPaser):
    __section_name = 'PlayDepth'


class WrapStyle(Section, IntPaser):
    __section_name = 'WrapStyle'


class ScaledBorderAndShadow(Section):
    __section_name = 'ScaledBorderAndShadow'

    def __to_value(self, text):
        """
        Parameters
        ----------
        text : str
            Text includes Yes or No.
        """
        return bool(text.lower == 'yes')

    def __to_text(self, value):
        return 'Yes' if value else 'No'
