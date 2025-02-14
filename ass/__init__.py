from typing import Union
import pathlib
import _io
import os.path
import re


class ASS:
    def __init__(
            self,
            ass: Union[str, pathlib.Path, _io.TextIOWrapper],
            encoding: str = 'utf-8-sig'
    ):
        if isinstance(ass, str):
            if os.path.exists(ass):
                ass = pathlib.Path(ass)
            else:
                ass_content = ass
        if isinstance(ass, pathlib.Path):
            ass = open(ass, 'r', encoding=encoding)
        if isinstance(ass, _io.TextIOWrapper):
            ass_content = ass.read()
            ass.close()
        ass_lines = iter(re.split(r'\r?\n', ass_content))

        # for line in iter(re.split(r'\r?\n', ass_content)):
        #     line = line.strip()
        #     section_name = re.findall(r'^\[(.*)]$', line)
        #     if section_name:
        #         section_name = section_name[0]
        #         continue

        section_name = re.findall(r'^\[(.*)]$', next(ass_lines))
        while True:
            if section_name:
                section_name = section_name[0]
                if section_name == 'Script Info':
                    section_name = self.__parse_script_info(ass_lines)
                elif re.match(r'V4\+? Styles', section_name):
                    section_name = self.__parse_styles(ass_lines)
                elif section_name == 'Events':
                    section_name = self.__parse_events(ass_lines)
            try:
                line = next(ass_lines)
            except StopIteration:
                break
            section_name = re.findall(r'^\[(.*)]$', line)

    def __parse_script_info(self, ass_lines: iter) -> Union[str, None]:
        for line in ass_lines:
            line = line.strip()
            if re.match(r'^[;|!]|^\s*$', line):
                continue
            section_name = re.findall(r'^\[(.*)]$', line)
            if section_name:
                return section_name[0]

            header, value = re.split(r'\s*:\s*', line, maxsplit=1)
            self.__setattr__(header, value)

        return None

    def __parse_styles(self, ass_lines: iter) -> Union[str, None]:
        for line in ass_lines:
            line = line.strip()
            if re.match(r'^[;|!]|^\s*$', line):
                continue
            section_name = re.findall(r'^\[(.*)]$', line)
            if section_name:
                return section_name[0]

            pass  # TODO

        return None

    def __parse_events(self, ass_lines: iter) -> Union[str, None]:
        for line in ass_lines:
            line = line.strip()
            if re.match(r'^[;|!]|^\s*$', line):
                continue
            section_name = re.findall(r'^\[(.*)]$', line)
            if section_name:
                return section_name[0]

            pass  # TODO

        return None


if __name__ == '__main__':
    ass_parser = ASS(r'../test.ass')
    print()
