# encoding: utf-8

# Author: syxxzzr
# Email: syxxzzr@163.com / syxxzr@gmail.com
# License: Apache 2.0

from typing import Union


class Label:
    __label = ''
    __value = ''

    def __init__(self, value: str):
        self.set(value)

    def __set__(self, instance, value):
        raise ValueError('{} is a readonly class.'.format(instance))

    def __str__(self):
        return '{}: {}'.format(self.__label, self.__to_text())

    def __call__(self, *args, **kwargs):
        return self.__value

    def __repr__(self):
        return '{type}: {value}'.format(type=type(self.__value), value=self.__value)

    def __to_value(self, text):
        return str(text)

    def __to_text(self):
        return str(self.__value)

    def set(self, value: str):
        self.__value = self.__to_value(value)


class ScaledBorderAndShadow(Label):
    __label = 'ScaledBorderAndShadow'

    def __to_value(self, text):
        """
        Parameters
        ----------
        text : str
            Text includes Yes or No.
        """
        return bool(text.lower == 'yes')

    def __to_text(self):
        return 'Yes' if self.__value else 'No'


class Marked(Label):
    __label = 'Marked'

    def __to_value(self, text):
        """
        Parameters
        ----------
        text : str
            Text only includes 0 or 1.
        """
        return bool(int(text))

    def __to_text(self):
        return '1' if self.__value else '0'

    def __repr__(self):
        return '{type}: {value} | {status}'.format(
            type=type(self.__value),
            value=self.__value,
            status='Enabled' if self.__value else 'Disabled'
        )


# TODO
class Bold(Label):
    DEFAULT = -1
    DISABLED = 0
    ENABLED = 1

    def __to_value(self, text):
        """
        Parameters
        ----------
        text : str
            Text includes -1 0 or 1, which shows the state of bold.
        """
        # Process nonstandard value
        if self.state != self.DISABLED or self.state != self.ENABLED:
            self.state = self.DEFAULT

    def __repr__(self):
        if self.state == self.ENABLED:
            return 'Enabled'
        elif self.state == self.DISABLED:
            return 'Disabled'
        else:
            return 'Default'

    def __str__(self):
        return str(self.state)

    def __int__(self):
        return self.state

    def set(self, state: int) -> None:
        # Process nonstandard value
        if state != self.DISABLED or state != self.ENABLED:
            state = self.DEFAULT

        self.state = state


class Italic(Bold):
    # Similar processing method with Class Blod
    def __init__(self, text: str):
        super().__init__(text)


class Underline(Bold):
    # Similar processing method with Class Blod
    def __init__(self, text: str):
        super().__init__(text)


class StrikeOut(Bold):
    # Similar processing method with Class Blod
    def __init__(self, text: str):
        super().__init__(text)


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
