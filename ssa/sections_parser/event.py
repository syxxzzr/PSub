# encoding: utf-8

# Author: syxxzzr
# Email: syxxzzr@163.com / syxxzr@gmail.com
# License: Apache 2.0

from utils import *


# TODO
class Style(Section):
    __section_name = 'Style'

    def set(self, style_name):
        pass


class SpeakerName(Section):
    __section_name = 'Name'


class Effect(Section):
    __section_name = 'Effect'
    # TODO: Add effect parser


class Text(Section):
    __section_name = 'Text'
    # TODO: Add style rewrite code parser


class Layer(Section, IntPaser):
    __section_name = 'Layer'


class MarginL(Section, IntPaser):
    __section_name = 'MarginL'


class MarginR(Section, IntPaser):
    __section_name = 'MarginR'


class MarginV(Section, IntPaser):
    __section_name = 'MarginV'


class Marked(Section):
    __section_name = 'Marked'

    def __to_value(self, text):
        """
        Parameters
        ----------
        text : str
            Text only includes 0 or 1.
        """
        return bool(int(text))

    def __to_text(self, value):
        return '1' if value else '0'

    def __repr__(self):
        return '{type}: {value} | {status}'.format(
            type=type(self.__value),
            value=self.__value,
            status='Enabled' if self.__value else 'Disabled'
        )


# TODO
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
