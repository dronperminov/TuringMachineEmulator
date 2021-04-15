from typing import Dict
from turing_machine.constants import LAMBDA, STOP_STATE, MOVE_LEFT, MOVE_NONE, MOVE_RIGHT
from turing_machine.constants import NORMAL_MODE, BY_STEP_MODE
from turing_machine.constants import SUCCESSFUL_STATUS, MAX_ITERATIONS_REACHED_STATUS, MAX_ITERATIONS
from turing_machine.tape import Tape


class TuringMachine:
    """
    Turing machine class.

    :param alphabet: the alphabet of this machine
    :type alphabet: string of characters
    :param rules: maps state, character to [symbol, move, next state]
    :type rules: {str: {str: [str]}}
    """
    def __init__(self, *, alphabet: str, rules: Dict[str, Dict[str, list]], tape: str = '', position: int = 0):
        self.alphabet = alphabet + LAMBDA
        self.rules = rules
        self.tape = Tape(tape)
        self.position = position

    def __print_line(self):
        """prints horisonatal line of the rules tabel"""
        print('+--------' * len(self.alphabet) + '+--------+')

    def __print_header(self):
        """prints header of the rules tabel"""
        print("|        |", " | ".join("%6s" % c for c in self.alphabet), "|")

    def __cell_to_str(self, q: str, c: str, prettify: bool) -> str:
        """returns string to print in corresponding cell"""

        c_next, move, q_next = self.rules[q][c]

        if prettify and c_next == c:
            if q_next == q:
                return move

            if move == MOVE_NONE:
                return q_next

        return c_next + " " + q_next + " " + move

    def __print_state(self, q: str, prettify: bool):
        """Prints whole rules tabel line corresponding to the state
        :param q: the state
        """
        cells = " | ".join("%6s" % self.__cell_to_str(q, c, prettify) for c in self.alphabet)
        print("| %6s |" % q, cells, "|")

    def print_rules(self, prettify_rules: bool = True):
        """Prints rules as plain text table.

        :param prettify_rules: whether to simplify (char,move,state)-cell when possible
        """
        print("Alphabet:", self.alphabet)
        print("Rules table:")

        self.__print_line()
        self.__print_header()
        self.__print_line()

        for q in self.rules:
            self.__print_state(q, prettify_rules)

        self.__print_line()
        print()

    def print_tape(self, with_position=True):
        """Prints current state of the tape.

        :param with_position: whether to mark current head position with brackets
        """
        tape_str = self.tape.string_with_position(self.position) if with_position else str(self.tape)
        print(tape_str or "Tape is empty")

    def set_tape_string(self, tape: str, position: int = 0):
        """Set up tape and head position

        :param tape: what is written on the new tape
        :param position: where the head is on the new tape
        """
        self.position = position
        self.tape = Tape(tape)

    def get_tape_string(self):
        """Returns the current state of the tape as a string"""
        return str(self.tape)

    def run(self, mode: str = NORMAL_MODE, max_tacts: int = MAX_ITERATIONS, initial_state: str = "q0") -> dict:
        """Emulate the Turing machine.

        :param mode: whether to include result of every step in return
        :returns: dictionary with fields:
            * status: whether the machine stoped by itself (successfully) or because of tacts limit
            * result: what is written on the tape as result
            * iterations: how many tacts it run
            * head_position: where the head is on the tape
            * steps: list of intemideate information for every step, included only for "by step" mode
        """
        q = initial_state
        tacts = 0
        steps = []

        while q != STOP_STATE and tacts < max_tacts:
            c = self.tape[self.position]
            c_next, move, q_next = self.rules[q][c]
            self.tape[self.position] = c_next

            if mode == BY_STEP_MODE:
                steps.append({
                    "curr_state": q,
                    "next_state": q_next,
                    "curr_character": c,
                    "next_character": c_next,
                    "move": move,
                    "tact": tacts
                })

            if move == MOVE_RIGHT:
                self.position += 1
            elif move == MOVE_LEFT:
                self.position -= 1

            tacts += 1
            q = q_next

        result = {
            "status": SUCCESSFUL_STATUS if tacts < max_tacts else MAX_ITERATIONS_REACHED_STATUS,
            "result": self.get_tape_string(),
            "iterations": tacts,
            "head_position": self.position
        }

        if mode == BY_STEP_MODE:
            result["steps"] = steps

        return result
