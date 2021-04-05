from turing_machine.turing_machine import TuringMachine, NORMAL_MODE


def main():
    config = {
        'alphabet': 'ab',
        'tape': 'aabaab'
    }
    config["rules"] = {
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

    turing_machine = TuringMachine(**config)

    turing_machine.print_tape()
    turing_machine.print_rules()

    result = turing_machine.run()

    turing_machine.print_tape()
    print("Result:", result)


if __name__ == '__main__':
    main()
