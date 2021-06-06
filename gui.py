"""
Graphical user interface for Turing machine, using Tkinter.
"""
import tkinter as tk
from tkinter import ttk
from turing_machine.turing_machine import TuringMachine


class View(ttk.Frame):
    """Defines graphical user interface."""
    def __init__(self, machine: TuringMachine):
        super().__init__(None)
        self.master.title('Turing Machine Emulator')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.model = machine
        self.controller = Controller(machine)
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
        for i, q in enumerate(self.model.rules.keys()):
            self.new_widget(ttk.Label, i + 1, 0, parent=self.rules, text=q)

        for j, c in enumerate(self.model.alphabet[:-1]):  # XXX get_alphabet will remove LAMBDA?
            self.new_widget(ttk.Label, 0, j + 1, parent=self.rules, text=c)
        for i, s in enumerate(self.model.rules):
            for j, c in enumerate(self.model.alphabet[:-1]):
                self.new_widget(ttk.Label, i + 1, j + 1, parent=self.rules, text=self.model.rules[s][c])
        self.set_weight(self.rules)


class Controller:
    def __init__(self, machine: TuringMachine):
        self.model = machine

        self.alphabet = tk.StringVar()
        self.alphabet.set(self.model.alphabet[:-1])

        self.tape = tk.StringVar()
        self.tape.set(self.model.get_tape_string())

        self.tacts_counter = 0
        self.tacts_title = "Tacts: "
        self.tacts = tk.StringVar()
        self.tacts.set(self.tacts_title + str(self.tacts_counter))

    def alphabet_check(self, prev: str):
        """Check the alphabet entry to consist of unique symbols."""
        if len(set(self.alphabet.get())) == len(self.alphabet.get()):
            # self.update_rules()
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
