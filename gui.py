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

    def new_widget(self, cls, row, column, rowspan=1, colspan=1, parent=None, **kwargs):
        """Create subwidget and place it in grid."""
        if parent is None:
            parent = self
        x = cls(parent, **kwargs)
        x.grid(row=row, column=column, rowspan=rowspan, columnspan=colspan, sticky='NEWS')
        return x

    def create_widgets(self):
        """Create all the widgets."""

        self.tape = self.new_widget(ttk.Label, 0, 0, textvariable=self.controller.tape)

        machine_settings = self.new_widget(ttk.Frame, 1, 0)

        vc = self.register(self.controller.alphabet_check)
        self.alphabet = self.new_widget(
            ttk.Entry, 0, 0, parent=machine_settings,
            textvariable=self.controller.alphabet, validate='focusout',
            validatecommand=vc
        )

        self.tacts = self.new_widget(ttk.Label, 0, 1, parent=machine_settings, textvariable=self.controller.tacts)
        self.makestep = self.new_widget(ttk.Button, 0, 3, parent=machine_settings, text='Step', command=self.controller.step)
        self.go = self.new_widget(ttk.Button, 0, 2, parent=machine_settings, text='Go', command=self.controller.go)

        self.set_weight(machine_settings)

        self.rules = self.new_widget(ttk.Frame, 2, 0)
        self.controller.update_rules()

        file_io = self.new_widget(ttk.Frame, 3, 0)
        self.load = self.new_widget(ttk.Button, 0, 0, parent=file_io, text='Load')
        self.save = self.new_widget(ttk.Button, 0, 1, parent=file_io, text='Save')
        self.set_weight(file_io)

    def update_rules(self):
        """Recreate the rules table."""
        self.rules.destroy()
        self.rules = self.new_widget(ttk.Frame, 2, 0)
        self.new_widget(ttk.Label, 0, 0, colspan=2, parent=self.rules, text='q \ a')

        for j, c in enumerate(self.model.alphabet):
            self.new_widget(ttk.Label, 0, j + 2, parent=self.rules, text=c)
        for i, s in enumerate(self.model.rules):
            def to_reg1(s=s):
                return self.controller.delete_state(s)
            vc = self.register(to_reg1)
            self.new_widget(ttk.Button, i + 1, 0, parent=self.rules, text='x', command=vc)
            def to_reg(s=s):
                return self.controller.state_check(s)
            vc = self.register(to_reg)
            self.new_widget(
                ttk.Entry, i + 1, 1, parent=self.rules,
                textvariable=self.controller.rules[s], validate='focusout',
                validatecommand=vc
            )
            for j, c in enumerate(self.model.alphabet):
                def to_reg(s=s, c=c):
                    return self.controller.rule_check(s, c)
                vc = self.register(to_reg)
                self.new_widget(
                    ttk.Entry, i + 1, j + 2, parent=self.rules,
                    textvariable=self.controller.rules[s, c], validate='focusout',
                    validatecommand=vc
                )
        lll = len(self.model.rules)
        def to_reg(s=''):
            return self.controller.state_check(s)
        vc = self.register(to_reg)
        self.new_widget(
            ttk.Entry, 1 + lll, 1, parent=self.rules,
            textvariable=self.controller.rules[''], validate='focusout',
            validatecommand=vc
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

    def update_rules(self, remove=''):
        """Add or remove entries for rules."""

        def new_var(s: str, c: str):
            result = tk.StringVar()
            if c is None:
                result.set(s)
                return result
            result.set(self.model.rules.get(s, {}).get(c, '') or self.stashed.get((s, c), ''))
            return result

        self.rules = {
            (s, c): new_var(s, c)
            for s in self.model.rules.keys()
            for c in self.model.alphabet
        }
        self.rules.update({
            s: new_var(s, None)
            for s in self.model.rules
        })
        self.rules[''] = tk.StringVar()  # for new state

        for state, line in self.model.rules.items():
            for c in remove:
                self.stashed[state, c] = line.pop(c, '')

        self.view.update_rules()

    def delete_state(self, s: str):
        """Remove the state from the machine."""
        self.model.rules.pop(s)
        self.update_rules()

    def state_check(self, s: str):
        """Check state name to be unique."""
        old = s
        new = self.rules[s].get()
        if new == old:
            return False
        if new in self.model.rules:
            self.rules[s].set(s)
            return False
        assert(old == '' or old in self.model.rules)
        line = self.model.rules.pop(old, dict())
        self.model.rules[new] = line
        self.update_rules()
        return True

    def rule_check(self, state: str, char: str):
        """Check the rule entry to be correct triple."""
        from re import split
        result = split(r'[,\s]+', self.rules[state, char].get())
        if len(result) != 3 \
            or result[0] not in self.model.alphabet \
            or result[1] not in 'nrlNRL' \
            or '!' != result[2] not in self.model.rules:
            self.rules[state, char].set(self.model.rules[state][char])
            return False
        self.model.rules[state][char] = result
        return True

    def alphabet_check(self):
        """Check the alphabet entry to consist of unique symbols."""
        old = self.model.alphabet
        new = self.alphabet.get()
        if old[:-1] == new:
            return False
        if len(set(new)) == len(new):
            new += LAMBDA
            self.model.alphabet = new
            self.update_rules([c for c in old if c not in new])
            return True
        self.alphabet.set(old[:-1])
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
