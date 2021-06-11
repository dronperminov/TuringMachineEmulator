import sys
from .turing_machine import TuringMachine
import turing_machine.gui as gui
import turing_machine.web as web


def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'web':
        web.main()
    else:
        gui.main()


main()
