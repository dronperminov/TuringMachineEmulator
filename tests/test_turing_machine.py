import unittest

from turing_machine.turing_machine import TuringMachine
from turing_machine.constants import NORMAL_MODE, BY_STEP_MODE, STOP_STATE
from turing_machine.constants import MAX_ITERATIONS_REACHED_STATUS, SUCCESSFUL_STATUS, MAX_ITERATIONS


class TestTape(unittest.TestCase):
    def test_empty_machine(self):
        config = {
            "alphabet": "",
            "rules": {}
        }

        machine = TuringMachine(**config, initial_state=STOP_STATE)
        result = machine.run(NORMAL_MODE)

        self.assertEqual(result["status"], SUCCESSFUL_STATUS)
        self.assertEqual(result["iterations"], 0)
        self.assertEqual(result["result"], "")
        self.assertEqual(result["head_position"], 0)

    def test_step_move(self):
        config = {
            'alphabet': 'ab',
            'tape': 'aabbaba',
            'rules': {
                "q0": {
                    "a": ["b", "R", "q0"],
                    "b": ["a", "R", "q0"],
                    "λ": ["λ", "N", "!"]
                },
            }
        }

        machine = TuringMachine(**config)
        result = machine.run(BY_STEP_MODE)

        self.assertEqual(result["status"], SUCCESSFUL_STATUS)
        self.assertEqual(result["iterations"], 8)
        self.assertEqual(result["result"], "bbaabab")
        self.assertEqual(result["head_position"], 7)

        steps = result["steps"]
        self.assertEqual(len(steps), 8)
        self.assertEqual(steps[0]["curr_state"], "q0")
        self.assertEqual(steps[0]["next_state"], "q0")
        self.assertEqual(steps[0]["curr_character"], "a")
        self.assertEqual(steps[0]["next_character"], "b")
        self.assertEqual(steps[0]["move"], "R")

        self.assertEqual(steps[7]["curr_state"], "q0")
        self.assertEqual(steps[7]["next_state"], "!")
        self.assertEqual(steps[7]["curr_character"], "λ")
        self.assertEqual(steps[7]["next_character"], "λ")
        self.assertEqual(steps[7]["move"], "N")

    def test_initial_state(self):
        config = {
            'alphabet': 'ab',
            'tape': 'aabaab',
            'position': 1,
            'initial_state': "q1",
            'rules': {
                "q0": {
                    "a": ["a", "R", "q1"],
                    "b": ["b", "R", "q1"],
                    "λ": ["λ", "N", "!"]
                },
                "q1": {
                    "a": ["b", "R", "q0"],
                    "b": ["a", "R", "q0"],
                    "λ": ["λ", "N", "!"]
                }
            }
        }

        machine = TuringMachine(**config)
        result = machine.run()

        self.assertEqual(result["status"], SUCCESSFUL_STATUS)
        self.assertEqual(result["iterations"], 6)
        self.assertEqual(result["result"], "abbbaa")
        self.assertEqual(result["head_position"], 6)

    def test_max_iterations(self):
        config = {
            "alphabet": "01",
            "tape": "abba",
            "rules": {
                "q0": {
                    "a": ["a", "R", "q0"],
                    "b": ["b", "R", "q0"],
                    "λ": ["λ", "R", "q0"],
                }
            }
        }

        machine = TuringMachine(**config)
        result = machine.run()

        self.assertEqual(result["status"], MAX_ITERATIONS_REACHED_STATUS)
        self.assertEqual(result["iterations"], MAX_ITERATIONS)
        self.assertEqual(result["result"], "abba")
        self.assertEqual(result["head_position"], MAX_ITERATIONS)
