class Section:
    """
    Provide a readonly section class model.

    Simply you can reset '__section_name' parameter as the section name on SSA file,
    and then reset '__to_value' and '__to_text' to create a map between SSA file
    and the more comfort-used data type in python.
    """
    __section_name = ''  # label of the section
    __value = ''  # converted value

    def __init__(self, value: str):
        self.set(value)

    def __set__(self, instance, value):
        """ '__set__' function be banned in readonly class. """
        raise ValueError('{} is a readonly class.'.format(instance))

    def __str__(self):
        """
        Returns
        -------
        Out : str
            A line text can straightly write into an SSA file.
        """
        return '{}: {}'.format(self.__section_name, self.__to_text(self.__value))

    def __call__(self, *args, **kwargs):
        """
        Returns
        -------
        Out : any
            Value of the section with the more comfort-used data type in python.
        """
        return self.__value

    def __repr__(self):
        """
        Returns
        -------
        Out : str
            '{type}: {value} | {text}' formatted string.
        """
        return '{type}: {value} | {text}'.format(
            type=type(self.__value),
            value=self.__value,
            text=self.__to_text(self.__value)
        )

    def __to_value(self, text):
        """
        Convert the inputted text to the more comfort-used data type in python.

        Parameters
        ----------
        text : str
            Text on SSA file.

        Returns
        -------
        Out : any
            The more comfort-used data type in python.
        """
        return str(text)

    def __to_text(self, value):
        """
        Convert value to string text.

        Parameters
        ----------
        value : any
            Value data in python.
            Usually it is self.__value.

        Returns
        -------
        Out : str
            The SSA file text corresponding to the value.
        """
        return str(value)

    def set(self, value: str):
        """
        Set the value.

        Parameters
        ----------
        value : str
            Text on SSA file.
        """
        self.__value = self.__to_value(value)


class FloatPaser:
    __value = 0.0

    def __to_value(self, text):
        """
        Convert the inputted text to float type.

        Parameters
        ----------
        text : str
            Text on SSA file.

        Returns
        -------
        Out : any
            Float type in python.
        """
        return float(text)

    def __to_text(self, value):
        """
        Convert float value to text.

        Parameters
        ----------
        value : float
            Float type in python.

        Returns
        -------
        Out : str
            The SSA file text corresponding to the number.
        """
        return str(value)


class IntPaser:
    __value = 0

    def __to_value(self, text):
        """
        Convert the inputted text to int type.

        Parameters
        ----------
        text : str
            Text on SSA file.

        Returns
        -------
        Out : any
            Int type in python.
        """
        return int(text)

    def __to_text(self, value):
        """
        Convert float value to text.

        Parameters
        ----------
        value : int
            Int type in python.

        Returns
        -------
        Out : str
            The SSA file text corresponding to the number.
        """
        return str(value)


class ThreeOptionPaser:
    DEFAULT = -1
    DISABLED = 0
    ENABLED = 1

    __value = DEFAULT

    def __to_value(self, text):
        """
        Parameters
        ----------
        text : str
            Text includes -1 0 or 1, which shows the state of bold.

        Returns
        -------
        Out : any
            Int typed number -1 0 or 1.
        """
        # Process nonstandard value
        value = int(text)
        if value != self.DISABLED and value != self.ENABLED:
            value = self.DEFAULT

        return value

    def __to_text(self, value):
        """
            Convert int value to text.

            Parameters
            ----------
            value : int
                Int typed number -1 0 or 1.

            Returns
            -------
            Out : str
                The SSA file text corresponding to the number.
            """
        return str(value)

    def __repr__(self):
        """
        Returns
        -------
        Out : str
            '{type}: {value} | {status}' formatted string.
            status is included in 'Enabled' 'Disabled' and 'Default'
        """
        if self.__value == self.ENABLED:
            status = 'Enabled'
        elif self.__value == self.DISABLED:
            status = 'Disabled'
        else:
            status = 'Default'

        return '{type}: {value} | {status}'.format(
            type=type(self.__value),
            value=self.__value,
            status=status
        )


# TODO
class ColorPaser:
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


class NoStandardSection(Section):
    def __init__(self, section_name: str, value: str):
        self.section_name, self.__section_name = section_name
        super().__init__(value)
