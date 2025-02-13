# encoding: utf-8

# Author: syxxzzr
# Email: syxxzzr@163.com / syxxzr@gmail.com
# License: Apache 2.0

from typing import Union, Optional
from pathlib import Path
from io import TextIOWrapper
from definitions import *
import re


class ASSFileError(Exception):
    pass


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
        # load archive file
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
    ass = Paser('../test.py')
    print()
