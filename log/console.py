#coding:gbk
from trace import *
import ctypes


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.

BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.


class ConsoleOutput(Output):
    def __init__(self):
        Output.__init__(self)
        self.std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        self.mbPrintNormalMsg = True

    def onTrace(self, msg, level):
        if level == levelTrace:
            print(msg)
        elif level == levelHintHint:
            self.print_color_text(msg, 6)
        elif level == levelHintGood:
            self.print_green_text(msg)
        elif level == levelWarning:
            self.print_red_text_with_blue_bg(msg)
        elif level == levelError:
            self.print_red_text(msg)

    def set_cmd_color(self, color):
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(self.std_out_handle, color)
        return bool

    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

    def print_red_text(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
        print print_text
        self.reset_color()

    def print_green_text(self, print_text):
        self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
        print print_text
        self.reset_color()

    def print_blue_text(self, print_text):
        self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        print print_text
        self.reset_color()

    def print_color_text(self, print_text, clr):
        self.set_cmd_color(clr | FOREGROUND_INTENSITY)
        print print_text
        self.reset_color()

    def print_red_text_with_blue_bg(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY| BACKGROUND_BLUE | BACKGROUND_INTENSITY)
        print print_text
        self.reset_color()


if __name__ == "__main__":
    from trace import Tracer

    log = Tracer()
    log.registerTrace(ConsoleOutput())
    log.output("trace", levelTrace)
    log.output("hint", levelHintHint)
    log.output("good", levelHintGood)
    log.output("warning", levelWarning)
    log.output("error", levelError)
