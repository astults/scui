from enum import Enum

class Color(Enum):
    BLACK = 0
    RED = 1
    BLUE = 2
    GREEN = 3

class TextUtils(object):

    @staticmethod
    def wrap_line(line, max_line_length):
        if max_line_length < 0:
            raise Exception("Max line length must be greater than 0.")
        lines = []
        i,j = 0, max_line_length
        while i <= len(line):
            lines.append(line[i:j])
            i,j = j, j + max_line_length
        return lines

    @staticmethod
    def is_newline(c):
        if c.isdigit():
            key_code = int(c)
            return key_code == 10 or key_code == 13
        return c == '\n' or c == '\r'
