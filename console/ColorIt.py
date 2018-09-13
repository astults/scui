import os
import sys
import subprocess

subprocess.call('', shell=True) #magic to allow console color printing
 

class Color:
    TRANSP = -1
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    FUSCIA = 5
    TURQ = 6
    WHITE = 7

    __control_prefix = '\x1b['
    __reset_control = '\x1b[0m'
    __fg_color_base = 30
    __bg_color_base = 40
    
    @classmethod
    def It(cls, s, text_color = 7, bg_color = 0):
        control = [1, cls.__fg_color_base + text_color, cls.__bg_color_base + bg_color]
        return cls.get_color_prefix(control) + s + cls.__reset_control


    @classmethod
    def get_color_prefix(cls, color_controls):
        text_control = ";".join([str(c) for c in color_controls])        
        return '%s%sm' % (Color.__control_prefix, text_control)


    def __init__(self):
        self._bright_style = 1
        self._dim_style = 0
        self._fg_color_base = 30
        self._bg_color_base = 40
        self._prefix = '\x1b['
        self._reset_control = '\x1b[0m'
        self._current_color = [self._bright_style, self._fg_color_base, self._bg_color_base]
        self._color_command_prefix = ''

    def set_color_prefix(self):
        text_control = ";".join([str(c) for c in self._current_color])        
        self._color_command_prefix = '%s%sm' % (self._prefix, text_control)

    def reset_colors(self):
        self.__out(self._reset_control)

    def set_background_color(self, color):
        self._current_color[2] = self._bg_color_base + color
        self.set_color_prefix()

    def set_text_color(self, color):
        self._current_color[1] = self._fg_color_base + color
        self.set_color_prefix()

    def wrap_string(self, s):
        return self._color_command_prefix + s + self._reset_control

    def out(self, s):
        self.__out(s)

    def __out(self, s):
        sys.stdout.write(self.wrap_string(s))        

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__out(self._reset_control)        


# def print_format_table():
#     """
#     prints table of formatted text format options
#     """
#     for style in range(8):
#         for fg in range(30,38):
#             s1 = ''
#             for bg in range(40,48):
#                 format = ';'.join([str(style), str(fg), str(bg)])
#                 s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
#             print(s1)
#         print('\n')



def main(args):
    pass
    # for n in range(100):
    #     with ColorConsole() as c:
    #         c.set_text_color(Color.GREEN)
    #         c.out("Hello World!")
    #         c.set_background_color(Color.WHITE)
    #         print("Inside World.")
    #         c.out("Goodby World!")

if __name__ == "__main__":
    main(sys.argv[1:])