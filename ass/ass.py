from typing import Union, Optional
from pathlib import Path
from io import TextIOWrapper
import re


class ASSFileError(Exception):
    pass


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


class Color:
    alpha = 0

    def __init__(self, *args):
        if (len(args) == 3 or len(args) == 4
                and isinstance(args[0], (int, float))
                and isinstance(args[1], (int, float))
                and isinstance(args[2], (int, float))
        ):
            self.red, self.green, self.blue = args[0: 3]
            if len(args) == 4 and isinstance(args[3], (int, float)):
                self.alpha = args[4]

        elif len(args) == 1 and isinstance(args[0], str):
            hex_color = args[0]
            self.red, self.green, self.blue, self.alpha = self.to_color(hex_color)

    @classmethod
    def to_color(cls, hex_color: str):
        hex_color = hex_color.lstrip('&H')
        rest = int(hex_color, 16)

        red = rest & 0xFF
        rest >>= 8
        green = rest & 0xFF
        rest >>= 8
        blue = rest & 0xFF
        if len(hex_color) == 8:
            rest >>= 8
            alpha = rest & 0xFF
        else:
            alpha = 0

        return red, green, blue, alpha

    def __str__(self):
        return "&H{:02X}{:02X}{:02X}{:02X}".format(self.alpha, self.blue, self.green, self.red)


class TimeSegment:
    start = 0.
    end = 0.
    duration = 0.

    def __init__(self, start_time, end_time):
        if isinstance(start_time, str):
            self.start = self.__to_timestamp(start_time)
        elif isinstance(start_time, (int, float)):
            self.start = float(start_time)

        if isinstance(end_time, str):
            self.end = self.__to_timestamp(end_time)
        elif isinstance(end_time, (int, float)):
            self.end = float(end_time)

        self.duration = self.end - self.start

    def to_time_str(self):
        return self.__to_time_str(self.start), self.__to_time_str(self.end)

    def interval_intersection(self, time_segment):
        intersection_start = max(self.start, time_segment.start)
        intersection_end = min(self.end, time_segment.end)

        if intersection_start <= intersection_end:
            return intersection_end - intersection_start
        else:
            return 0

    @staticmethod
    def __to_timestamp(time_str):
        time_str = time_str.split(':')
        assert len(time_str) == 3
        return int(time_str[0]) * 3600 + int(time_str[1]) * 60 + float(time_str[2])

    @staticmethod
    def __to_time_str(timestamp):
        timestamp = int(timestamp * 100)
        hour = int(timestamp / 360000)
        assert hour < 10

        minute = int(timestamp % 360000 / 6000)
        second = int(timestamp % 6000 / 100)
        mille_second = timestamp % 100
        return '{:01d}:{:02d}:{:02d}.{:02d}'.format(hour, minute, second, mille_second)


class ScaledBorderAndShadow:
    def __init__(self, text: str):
        """
        Parameters
        ----------
        text : str
            Text includes Yes or No.
        """
        if text.lower == 'yes':
            self.enabled = True
        else:
            self.enabled = False

    def __str__(self):
        return 'Yes' if self.enabled else 'No'

    def __bool__(self):
        return self.enabled

    def set(self, enable: bool) -> None:
        self.enabled = enable


class Marked:
    def __init__(self, text: str):
        """
        Parameters
        ----------
        text : str
            Text includes 0 or 1.
        """
        self.enabled = bool(int(text))

    def __str__(self):
        return '1' if self.enabled else '0'

    def __bool__(self):
        return self.enabled

    def set(self, enable: bool) -> None:
        self.enabled = enable


class Bold:
    DEFAULT = -1
    DISABLE = 0
    ENABLE = 1

    def __init__(self, text: str):
        """
        Parameters
        ----------
        text : str
            Text includes -1 0 or 1, which shows the state of bold.
        """
        self.state = int(text)
        if self.state != self.DISABLE or self.state != self.ENABLE:
            self.state = self.DEFAULT

    def __str__(self):
        return str(self.state)

    def __int__(self):
        return self.state

    def set(self, state: int) -> None:
        if state != self.DISABLE or state != self.ENABLE:
            state = self.DEFAULT
        self.state = state


class Italic(Bold):
    def __init__(self, text: str):
        super().__init__(text)


class Underline(Bold):
    def __init__(self, text: str):
        super().__init__(text)


class StrikeOut(Bold):
    def __init__(self, text: str):
        super().__init__(text)


class Event:
    def __init__(
            self,
            event_content: Union[str, None] = None,
            event_format: Union[list, tuple, None] = None,
            event_index: Optional[int] = 0
    ):
        if event_content is None:
            return

        if event_format is None:
            event_content = [
                'layer', 'start', 'end', 'style', 'name', 'marginl', 'marginr', 'marginv', 'effect', 'text'
            ]

        event_content = re.split(r'\s*,\s*', event_content, maxsplit=len(event_format) - 1)
        assert len(event_content) == len(event_format)

        for index, param_name in enumerate(event_format):
            param = event_content[index]
            mappings = Mappings['event_format']

            if param_name in mappings.keys():
                mapping = mappings[param_name]
                setattr(self, mapping[0], mapping[1](param))

            else:
                if not hasattr(self, 'nonstandard_event'):
                    setattr(self, 'nonstandard_event', {})

                self.nonstandard_event[param_name] = param

        setattr(self, 'index', event_index)
        setattr(self, 'time_segment', TimeSegment(self.start, self.end))
        delattr(self, 'start')
        delattr(self, 'end')


class Dialogue(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Comment(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Picture(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Sound(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Movie(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Command(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Style:
    name = 'Default'
    font_name = 'Arial'
    font_size = 48.0
    primary_colour = Color()

    # TODO: fill it

    def __init__(
            self,
            style_content: Union[str, None] = None,
            style_format: Union[list, tuple, None] = None
    ):
        if style_content is None:
            return

        if style_format is None:
            style_format = [
                'name', 'fontname', 'fontsize', 'primarycolour', 'secondarycolour',
                'outlinecolour', 'backcolour', 'bold', 'italic', 'underline', 'strikeout',
                'scalex', 'scaley', 'spacing', 'angle', 'borderstyle', 'outline', 'shadow',
                'alignment', 'marginl', 'marginr', 'marginv', 'encoding'
            ]

        style_content = re.split(r'\s*,\s*', style_content, maxsplit=len(style_format) - 1)
        assert len(style_content) == len(style_format)

        for index, param_name in enumerate(style_format):
            param = style_content[index]
            mappings = Mappings['style_format']

            if param_name in mappings.keys():
                mapping = mappings[param_name]
                setattr(self, mapping[0], mapping[1](param))

            else:
                if not hasattr(self, 'nonstandard_style'):
                    setattr(self, 'nonstandard_style', {})

                self.nonstandard_style[param_name] = param


Mappings = {
    'script_info': {
        'title': ('title', str),
        'scripttype': ('type', str),
        'originalscript': ('scriptor', str),
        'originaltranslation': ('translator', str),
        'originalediting': ('editor', str),
        'originaltiming': ('timeliner', str),
        'scriptupdatedby': ('updator', str),
        'updatedetails': ('update_details', str),
        'collisions': ('collisions', str),
        'ycbcrmatrix': ('color_matrix', str),
        'timer': ('play_rate', float),
        'synchpoint': ('synch_point', float),
        'playresx': ('reference_x', int),
        'playresy': ('reference_y', int),
        'playdepth': ('color_depth', int),
        'wrapstyle': ('wrap_style', int),
        'scaledborderandshadow': (
            'scale_border_and_shadow', ScaledBorderAndShadow
        )
    },

    'style_format': {
        'name': ('name', str),
        'fontname': ('font_name', str),
        'borderstyle': ('border_style', int),
        'alignment': ('alignment', int),
        'marginl': ('margin_l', int),
        'marginr': ('margin_r', int),
        'marginv': ('margin_v', int),
        'encoding': ('encoding', int),
        'fontsize': ('font_size', float),
        'scalex': ('scale_x', float),
        'scaley': ('scale_y', float),
        'spacing': ('spacing', float),
        'angle': ('angle', float),
        'outline': ('outline', float),
        'shadow': ('shadow', float),
        'bold': ('bold', Bold),
        'italic': ('italic', Italic),
        'underline': ('underline', Underline),
        'strikeout': ('strike_out', StrikeOut),
        'primarycolour': ('primary_color', Color),
        'secondarycolour': ('secondary_color', Color),
        'outlinecolour': ('outline_color', Color),
        'backcolour': ('background_color', Color)
    },

    'event_format': {
        'start': ('start', str),
        'end': ('end', str),
        'style': ('style', str),
        'name': ('speaker_name', str),
        'effect': ('effect', str),
        'text': ('text', str),
        'layer': ('layer', int),
        'marginl': ('margin_l', int),
        'marginr': ('margin_r', int),
        'marginv': ('margin_v', int),
        'marked': ('marked', Marked)
    },

    'event_tag': {
        'dialogue': Dialogue,
        'comment': Comment,
        'picture': Picture,
        'sound': Sound,
        'movie': Movie,
        'command': Command
    }
}


class Paser:
    __standard_block_name = ['scriptinfo', 'v4+styles', 'events', 'fonts', 'graphics']

    title = None
    content = 'v4.00+'
    collisions = Collisions.NORMAL
    reference_x = 1920
    reference_y = 1080
    wrap_style = WrapStyle.AUTO_RELINE
    scale_border_and_shadow = False
    color_matrix = ColorMatrix.TV_709

    styles = {
        'Default': Style()
    }
    events = []

    def __init__(
            self,
            ass_file: Union[str, Path, TextIOWrapper],
            encoding: str = 'utf-8-sig'
    ):
        # load ass file
        if isinstance(ass_file, (str, Path)):
            ass_file = open(ass_file, 'r', encoding=encoding)

        self.ass_text = ass_file.read()
        ass_file.close()

        # split each block
        self.__ass_split_content = {}
        for block_name, block_content in re.findall(
                r'^\[(.*?)]$(.*?)(?=^\[|\Z)',
                self.ass_text,
                re.DOTALL | re.MULTILINE
        ):
            fmt_block_name = re.sub(r'\s', '', block_name.lower())
            if fmt_block_name not in self.__standard_block_name:
                block_content = [
                    line
                    for line in re.split('\\s*\n\\s*', block_content) if line
                ]

                if not hasattr(self, 'nonstandard_block'):
                    self.nonstandard_block = {}

                if block_name not in self.nonstandard_block.keys():
                    self.nonstandard_block[block_name] = []

                self.nonstandard_block[block_name].extend(block_content)
                continue

            # ignore script annotation line
            block_content = [
                re.split(r'\s*:\s*', line, maxsplit=1)
                for line in re.split('\\s*[!|;][^\n]+\n\\s*|\\s*\n\\s*', block_content)
                if self.__format_text(line)
            ]

            if fmt_block_name not in self.__ass_split_content.keys():
                self.__ass_split_content[fmt_block_name] = []

            self.__ass_split_content[fmt_block_name].extend(block_content)

        self.__load_script_info()
        self.__load_styles()
        self.__load_events()
        print()

    @staticmethod
    def __format_text(text):
        return re.sub(r'\s', '', text.lower())

    def __load_script_info(self):
        if 'scriptinfo' not in self.__ass_split_content.keys():
            return

        for line_content in self.__ass_split_content['scriptinfo']:
            if len(line_content) != 2:
                continue

            tag, line_content = line_content
            fmt_tag = self.__format_text(tag)

            mappings = Mappings['script_info']
            if fmt_tag in mappings.keys():
                mapping = mappings[fmt_tag]
                setattr(self, mapping[0], mapping[1](line_content))

            else:
                if not hasattr(self, 'nonstandard_script_info'):
                    setattr(self, 'nonstandard_script_info', {})

                self.nonstandard_script_info[tag] = line_content

    def __load_styles(self):
        if 'v4+styles' not in self.__ass_split_content.keys():
            return

        style_format = None
        for line_content in self.__ass_split_content['v4+styles']:
            if len(line_content) != 2:
                continue

            tag, line_content = line_content
            fmt_tag = self.__format_text(tag)

            if fmt_tag == 'format':
                style_format = re.split(r'\s*,\s*', line_content)
                style_format = [
                    fmt_format_key if fmt_format_key in Mappings['style_format'].keys() else format_key
                    for format_key in style_format
                    for fmt_format_key in [self.__format_text(format_key)]
                ]

            elif fmt_tag == 'style':
                style = Style(line_content, style_format)
                self.styles[style.name] = style

    def __load_events(self):
        if 'events' not in self.__ass_split_content.keys():
            return

        event_format = None
        line_index = 1
        for line_content in self.__ass_split_content['events']:
            if len(line_content) != 2:
                continue

            tag, line_content = line_content
            fmt_tag = self.__format_text(tag)
            mappings = Mappings['event_tag']

            if fmt_tag == 'format':
                event_format = re.split(r'\s*,\s*', line_content)
                event_format = [
                    fmt_format_key if fmt_format_key in Mappings['event_format'].keys() else format_key
                    for format_key in event_format
                    for fmt_format_key in [self.__format_text(format_key)]
                ]

            elif fmt_tag in mappings.keys():
                event = mappings[fmt_tag](line_content, event_format, line_index)
                self.events.append(event)
                line_index += 1

    def to_text(self):
        pass


# TODO: Class Color TimeSegment etc.
# TODO: Class Event and any other children Class
# TODO: Fill some default values
# TODO: Finish comments and function documents
# TODO: Classify functions and definitions


if __name__ == '__main__':
    ass = Paser('../../test/test.ass')
