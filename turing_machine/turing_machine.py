LAMBDA = 'λ'
STOP_STATE = '!'

MOVE_LEFT = 'L'
MOVE_NONE = 'N'
MOVE_RIGHT = 'R'

SUCCESSFUL_STATUS = "successful"
MAX_ITERATIONS_REACHED_STATUS = "max iterations reached"

NORMAL_MODE = "normal"
BY_STEP_MODE = "by step"


class Tape:
    """Infinite tape of characters."""
    def __init__(self, input: str = ''):
        from collections import defaultdict
        self._chars = defaultdict(lambda: LAMBDA)
        self._chars.update(enumerate(input))
        self._left = 0
        self._right = len(input)

    def __getitem__(self, key):
        return self._chars[key]

    def __setitem__(self, key, value):
        if value != LAMBDA:
            if key >= self._right:
                self._right = key + 1
            elif key < self._left and value != LAMBDA:
                self._left = key
            self._chars[key] = value
        elif key in self._chars:
            self._chars.pop(key)
            if key == self._right - 1:
                self._right = max(self._chars.keys())
            elif key == self._left and value != LAMBDA:
                self._left = min(self._chars.keys())

    def __str__(self):
        return ''.join(self._chars[i] for i in range(self._left, self._right))

    def string_with_position(self, head: int):
        """String representation with head position marked in []"""
        if head < self._left:
            return f'[{LAMBDA}]' + LAMBDA * (self._left - head - 1) + str(self)
        if head >= self._right:
            return str(self) + LAMBDA * (head - self._right) + f'[{LAMBDA}]'
        return ''.join(
            self._chars[i] for i in range(self._left, head)
        ) + f'[{self._chars[head]}]' + ''.join(
            self._chars[i] for i in range(head + 1, self._right)
        )


class TuringMachine:
    def __init__(self, *, alphabet: str, rules: dict[str, dict], tape: str = '', position: int = 0):
        self.alphabet = alphabet + LAMBDA
        self.rules = rules
        self.tape = Tape(tape)
        self.position = position

    def __print_line(self):
        print('+----------' * len(self.alphabet) + '+----------+')

    def __print_header(self):
        print("|          |", " | ".join("%8s" % c for c in self.alphabet), "|")

    def __cell_to_str(self, q: str, c: str, prettify: bool) -> str:
        c_next, move, q_next = self.rules[q][c]
        if prettify and c_next == c:
            if q_next == q: return move
            if move == MOVE_NONE: return q_next
        return c_next + " " + q_next + " " + move

    def __print_state(self, q: str, prettify: bool):
        print("| %8s |" % q, " | ".join(["%8s" % self.__cell_to_str(q, c, prettify) for c in self.alphabet]), "|")

    def print_rules(self, prettify_rules: bool = True):
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
        """Print current state of the tape."""
        string = self.tape.string_with_position(self.position) if with_position else str(self.tape)
        print(string or "Tape is empty")

    def reset(self, tape: str, position: int = 0):
        """Set up tape and head position"""
        self.position = position
        self.tape = Tape(tape)

    def get_tape_string(self):
        """Return the current state of the tape as a string"""
        return str(self.tape)

    def run(self, mode: str = NORMAL_MODE, max_tacts: int = 9999, initial_state: str = "q0") -> dict:
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
