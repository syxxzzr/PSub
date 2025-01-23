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