LAMBDA = 'λ'
STOP_STATE = '!'

MOVE_LEFT = 'L'
MOVE_NONE = 'N'
MOVE_RIGHT = 'R'

SUCCESSFUL_STATUS = "successful"
MAX_ITERATIONS_REACHED_STATUS = "max iterations reached"

NORMAL_MODE = "normal"
BY_STEP_MODE = "by step"


class TuringMachine:
    def __init__(self, config: dict, tape_size=10000):
        self.alphabet = config["alphabet"] + LAMBDA
        self.rules = config["rules"]
        self.tape = [LAMBDA for _ in range(tape_size)]  # TODO: replace with normal tape class
        self.position = tape_size // 2

    def __print_line(self):
        print("+----------" * (len(self.alphabet) + 1) + '+')

    def __print_header(self):
        print("|          |", " | ".join(["%8s" % c for c in self.alphabet]), "|")

    def __cell_to_str(self, q: str, c: str, prettify: bool) -> str:
        c_next, action, q_next = self.rules[q][c]

        if prettify:
            if c_next == c and q_next == q:
                return action

            if c_next == c and action == MOVE_NONE:
                return q_next

        return c_next + " " + q_next + " " + action

    def __get_borders(self):
        left = None
        right = len(self.tape) - 1

        for i, c in enumerate(self.tape):
            if c != LAMBDA:
                if left is None:
                    left = i

                right = i

        return left, right

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
        left, right = self.__get_borders()

        print("Tape: ", end='')

        if left is None:
            print("empty")
            return

        result = "".join([self.tape[i] for i in range(left, right + 1)])

        if with_position:
            left = min(left, self.position)
            right = max(right, self.position)

            print("".join(["[" + self.tape[i] + "]" if i == self.position else self.tape[i] for i in range(left, right + 1)]))
        else:
            print(result)

    def init_tape(self, word: str):
        self.position = len(self.tape) // 2

        for i, c in enumerate(word):
            self.tape[self.position + i] = c

    def get_tape_word(self):
        left, right = self.__get_borders()

        if left is None:
            return ""

        return "".join(self.tape[left:right + 1])

    def run(self, mode: str = "normal", max_tacts: int = 9999, initial_state: str = "q0") -> dict:
        q = initial_state
        tacts = 0
        steps = []

        while q != STOP_STATE and tacts < max_tacts:
            c = self.tape[self.position]
            c_next, action, q_next = self.rules[q][c]
            self.tape[self.position] = c_next

            if mode == BY_STEP_MODE:
                steps.append({
                    "curr_state": q,
                    "next_state": q_next,
                    "curr_character": c,
                    "next_character": c_next,
                    "action": action,
                    "tact": tacts
                })

            if action == MOVE_RIGHT:
                self.position += 1
            elif action == MOVE_LEFT:
                self.position -= 1

            tacts += 1
            q = q_next

        result = {
            "status": SUCCESSFUL_STATUS if tacts < max_tacts else MAX_ITERATIONS_REACHED_STATUS,
            "result": self.get_tape_word(),
            "iterations": tacts,
            "head_position": self.position
        }

        if mode == BY_STEP_MODE:
            result["steps"] = steps

        return result
