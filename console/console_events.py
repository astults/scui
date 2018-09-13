from enum import Enum

class KeyTag(Enum):
    PRINT = 0
    CONTROL = 1

class KeyCommands(Enum):
    NEWLINE = 0


class KeyPressEvent(object):
    CAR_RETURN = 13
    NEWLINE = 10

    def __init__(self, key_code):
        self.key_code = key_code
        self.tag = self.set_tag(self.key_code)
        self.key_char = None
        self.key_command = self.set_command(self.key_code)
        if self.tag == KeyTag.PRINT:
            self.key_char = chr(self.key_code)


    def set_tag(self, key_code):
        if 32 <= key_code <= 126:
            return KeyTag.PRINT
        if key_code == 8:
            return KeyTag.PRINT
        return KeyTag.CONTROL

    def set_command(self, key_code):
        if key_code == KeyPressEvent.CAR_RETURN or key_code == KeyPressEvent.NEWLINE:
            return KeyCommands.NEWLINE
        return None
