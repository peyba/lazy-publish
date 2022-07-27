BLACK = "\33[1;30m"
RED = "\33[1;31m"
GREEN = "\33[1;32m"
YELLOW = "\33[1;33m"
BLUE = "\33[1;34m"
MAGENTA = "\33[1;35m"
CYAN = "\33[1;36m"
WHITE = "\33[1;37m"
DEFAULT = "\33[1;39m"
RESET = "\33[1;0m"

BLACK_BG  = '\33[1;40m'
RED_BG    = '\33[1;41m'
GREEN_BG  = '\33[1;42m'
YELLOW_BG = "\33[1;43m"
BLUE_BG   = '\33[1;44m'
MAGENTA_BG = '\33[1;45m'
CYAN_BG  = '\33[1;46m'
WHITE_BG  = '\33[1;47m'
DEFAULT_BG = "\33[1;49m"

def paint(text:str, color:str) -> str:
    return color + text + RESET

def paint_black(text:str) -> str:
    return paint(text, BLACK)
def paint_red(text:str) -> str:
    return paint(text, RED)
def paint_green(text:str) -> str:
    return paint(text, GREEN)
def paint_yellow(text:str) -> str:
    return paint(text, YELLOW)
def paint_blue(text:str) -> str:
    return paint(text, BLUE)
def paint_magenta(text:str) -> str:
    return paint(text, MAGENTA)
def paint_cyan(text:str) -> str:
    return paint(text, CYAN)
def paint_white(text:str) -> str:
    return paint(text, WHITE)