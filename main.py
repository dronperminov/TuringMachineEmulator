from turing_machine.turing_machine import TuringMachine, NORMAL_MODE


def main():
    config = dict()
    config["alphabet"] = "ab"
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

    config["tape"] = "aabaab"
    config["mode"] = NORMAL_MODE

    turing_machine = TuringMachine(config)

    turing_machine.init_tape(config["tape"])
    turing_machine.print_tape()
    turing_machine.print_rules()

    result = turing_machine.run(config["mode"])

    turing_machine.print_tape()
    print("Result:", result)


if __name__ == '__main__':
    main()
