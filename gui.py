"""
Graphical user interface for Turing machine, using Tkinter.
"""
import tkinter as tk
from tkinter import ttk
from turing_machine.turing_machine import TuringMachine
from turing_machine.constants import LAMBDA

class View(ttk.Frame):
    """Defines graphical user interface."""
    def __init__(self, machine: TuringMachine):
        super().__init__(None)
        self.master.title('Turing Machine Emulator')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.model = machine
        self.controller = Controller(self, machine)
        self.grid(sticky="NEWS")
        self.create_widgets()
        self.set_weight(self)

    @staticmethod
    def set_weight(widget):
        """Make :param widget:'s grid stretchable."""
        for column in range(widget.grid_size()[0]):
            widget.columnconfigure(column, weight=1)
        for row in range(widget.grid_size()[1]):
            widget.rowconfigure(row, weight=1)

    def new_widget(self, cls, row, column, parent=None, **kwargs):
        """Create subwidget and place it in grid."""
        if parent is None:
            parent = self
        x = cls(parent, **kwargs)
        x.grid(row=row, column=column, sticky='NEWS')
        return x

    def create_widgets(self):
        """Create all the widgets."""

        self.tape = self.new_widget(ttk.Label, 0, 0, textvariable=self.controller.tape)

        machine_settings = self.new_widget(ttk.Frame, 1, 0)

        vc = self.register(self.controller.alphabet_check)
        self.alphabet = self.new_widget(
            ttk.Entry, 0, 0, parent=machine_settings,
            textvariable=self.controller.alphabet, validate='focusout',
            validatecommand=(vc, '%s')  # code for 'value before change'
        )

        self.tacts = self.new_widget(ttk.Label, 0, 1, parent=machine_settings, textvariable=self.controller.tacts)
        self.makestep = self.new_widget(ttk.Button, 0, 3, parent=machine_settings, text='Step', command=self.controller.step)
        self.go = self.new_widget(ttk.Button, 0, 2, parent=machine_settings, text='Go', command=self.controller.go)

        self.set_weight(machine_settings)

        self.rules = self.new_widget(ttk.Frame, 2, 0)
        self.update_rules()

        file_io = self.new_widget(ttk.Frame, 3, 0)
        self.load = self.new_widget(ttk.Button, 0, 0, parent=file_io, text='Load')
        self.save = self.new_widget(ttk.Button, 0, 1, parent=file_io, text='Save')
        self.set_weight(file_io)

    def update_rules(self):
        """Recreate the rules table."""
        self.rules.destroy()
        self.rules = self.new_widget(ttk.Frame, 2, 0)
        self.new_widget(ttk.Label, 0, 0, parent=self.rules, text='q \ a')

        for j, c in enumerate(self.model.alphabet):
            self.new_widget(ttk.Label, 0, j + 1, parent=self.rules, text=c)
        for i, s in enumerate(self.model.rules):
            self.new_widget(ttk.Label, i + 1, 0, parent=self.rules, text=s)
            for j, c in enumerate(self.model.alphabet):
                def to_reg(curr, prev, s=s, c=c):
                    return self.controller.rule_check(s, c, curr, prev)
                vc = self.register(to_reg)
                self.new_widget(
                    ttk.Entry, i + 1, j + 1, parent=self.rules,
                    textvariable=self.controller.rules[s, c], validate='focusout',
                    validatecommand=(vc, '%P', '%s')  # new val, stored val
                )
        self.set_weight(self.rules)


class Controller:
    def __init__(self, view: View, machine: TuringMachine):
        self.model = machine
        self.view = view

        self.alphabet = tk.StringVar()
        self.alphabet.set(self.model.alphabet[:-1])

        self.tape = tk.StringVar()
        self.tape.set(self.model.get_tape_string())

        self.tacts_counter = 0
        self.tacts_title = "Tacts: "
        self.tacts = tk.StringVar()
        self.tacts.set(self.tacts_title + str(self.tacts_counter))

        self.stashed = dict()
        self.update_rules('')

    def update_rules(self, remove):
        """Add or remove entries for rules."""
        def entry(s: str, c: str):
            result = tk.StringVar()
            result.set(self.model.rules.get(s, {}).get(c, '') or self.stashed.get((s, c), ''))
            return result
        self.rules = {
            (s, c): entry(s, c)
            for s in self.model.rules.keys()
            for c in self.model.alphabet
        }
        for state, line in self.model.rules.items():
            for c in remove:
                self.stashed[state, c] = line.pop(c, '')

    def rule_check(self, state: str, char: str, curr: str, prev: str):
        """Check the rule entry to be correct triple."""
        from re import split
        result = split(r'[,\s]+', curr)
        print('parsed', result)
        if len(result) != 3:
            print('wrong count')
            return False
        if result[0] not in self.model.alphabet:
            print('not in alphabet')
            return False
        if result[1] not in 'nrlNRL':
            print('not a move')
            return False
        if '!' != result[2] not in self.model.rules:
            print('not a state')
            return False
        print('is stored', self.model.rules[state].get(char, 'nothing'))
        print('at', state, char)
        self.model.rules[state][char] = result
        print('now stored', self.model.rules[state][char])
        return True

    def alphabet_check(self, prev: str):
        """Check the alphabet entry to consist of unique symbols."""
        if len(set(self.alphabet.get())) == len(self.alphabet.get()):
            new_a = self.alphabet.get() + LAMBDA
            old_a = self.model.alphabet
            self.model.alphabet = new_a
            self.update_rules([c for c in old_a if c not in new_a])
            self.view.update_rules()
            return True
        self.alphabet.set(prev)
        return False

    def step(self):
        """Advance the Turing machine one tact."""
        result = self.model.run(max_tacts=1)
        if result['iterations'] == 0:
            return  # the machine has stopped
        self.tacts_counter += 1
        self.tacts.set(self.tacts_title + str(self.tacts_counter))
        self.tape.set(self.model.get_tape_string())

    def go(self):
        """Run the Turing machine till it stops or tacts limit exceeds."""
        result = self.model.run()
        if result['iterations'] == 0:
            return  # the machine has stopped
        self.tacts_counter += result['iterations']
        self.tacts.set(self.tacts_title + str(self.tacts_counter))
        self.tape.set(self.model.get_tape_string())


if (__name__ == "__main__"):
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

    View(turing_machine).mainloop()
