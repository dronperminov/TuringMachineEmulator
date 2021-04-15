"""
Example using :class:`turing_machine.turing_machine.TuringMachine`.
"""

from turing_machine.turing_machine import TuringMachine


def main():
    """
    main function does main things.
    """
    config = {
        'alphabet': 'ab',
        'tape': 'aabaab',
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

    turing_machine = TuringMachine(**config)

    turing_machine.print_tape()
    turing_machine.print_rules()

    result = turing_machine.run()

    turing_machine.print_tape()
    print("Result:", result)


if __name__ == '__main__':
    main()
