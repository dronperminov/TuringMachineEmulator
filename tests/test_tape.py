import unittest

from turing_machine.tape import Tape
from turing_machine.constants import LAMBDA


class TestTape(unittest.TestCase):
    def test_empty_tape(self):
        tape = Tape()
        self.assertEqual(tape[0], LAMBDA)
        self.assertEqual(tape[-10], LAMBDA)
        self.assertEqual(tape[1000], LAMBDA)
        self.assertEqual(str(tape), "")

    def test_init_tape(self):
        test_string = "simple string for tape"
        tape = Tape(test_string)

        for i, c in enumerate(test_string):
            self.assertEqual(tape[i], c)

        self.assertEqual(str(tape), test_string)
        self.assertEqual(tape.string_with_position(5), "simpl[e] string for tape")

    def test_tape_change(self):
        tape = Tape()
        tape[5] = 't'
        tape[7] = 's'
        tape[6] = 'e'
        tape[8] = 't'
        self.assertEqual(str(tape), 'test')

        tape[5] = LAMBDA
        self.assertEqual(str(tape), 'est')

        tape[3] = 'w'
        self.assertEqual(str(tape), 'w' + LAMBDA + LAMBDA + 'est')

    def test_tape_change_negative(self):
        tape = Tape()
        tape[0] = 't'
        tape[-1] = 's'
        tape[-2] = 'e'
        tape[-3] = 't'
        self.assertEqual(str(tape), 'test')

        tape[-3] = LAMBDA
        self.assertEqual(str(tape), 'est')

        tape[-5] = 'w'
        self.assertEqual(str(tape), 'w' + LAMBDA + LAMBDA + 'est')
