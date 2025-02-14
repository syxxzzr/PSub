from typing import Union
import pathlib
import _io
import os.path
import re


def parse(
        ass: Union[str, pathlib.Path, _io.TextIOWrapper],
        encoding: str = 'utf-8-sig'
):
    if isinstance(ass, str):
        if os.path.exists(ass):
            ass = pathlib.Path(ass)
        else:
            ass_lines = re.split(r'\r?\n', ass)
    if isinstance(ass, pathlib.Path):
        ass = open(ass, 'r', encoding=encoding)
    if isinstance(ass, _io.TextIOWrapper):
        ass_lines = ass.readlines()
    ass_lines = iter(ass_lines)

    section_state = 0
    for line in ass_lines:
        if re.match(r'^;|!', line):
            continue
        section_name = re.match(r'^\[(.*)]$', line)
        if section_name:
            section_name = section_name.group()
            pass


# class ASS:
#     def __init__(
#             self,
#             ass: Union[str, pathlib.Path, _io.TextIOWrapper],
#             encoding: str = 'utf-8-sig'
#     ):
#         pass

if __name__ == '__main__':
    ass_parser = parse(r'./test.ass')
