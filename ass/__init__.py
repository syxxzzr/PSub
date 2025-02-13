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

        section_state = 0
        for line in ass_lines:
            if re.match(r'^;|!', line):
                continue

# class ASS:
#     def __init__(
#             self,
#             ass: Union[str, pathlib.Path, _io.TextIOWrapper],
#             encoding: str = 'utf-8-sig'
#     ):
#         pass



