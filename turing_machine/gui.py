"""
Graphical user interface for Turing machine, using Tkinter.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import font
from .turing_machine import TuringMachine
from .constants import LAMBDA
import os
import gettext


class View(ttk.Frame):
    """Defines graphical user interface."""
    def __init__(self, machine: TuringMachine):
        super().__init__(None)
        self.master.title(_('Turing Machine Emulator'))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.tape_size = 17

        self.model = machine
        self.controller = Controller(self, machine)

        self.grid(sticky="NEWS")
        self.__create_widgets()
        self.__set_weight(self)

    @staticmethod
    def __set_weight(widget):
        """Make widget's grid stretchable."""
        for column in range(widget.grid_size()[0]):
            widget.columnconfigure(column, weight=1)
        for row in range(widget.grid_size()[1]):
            widget.rowconfigure(row, weight=1)

    def __new_widget(self, cls, row: int, column: int, rowspan: int = 1, colspan: int = 1, parent=None, **kwargs):
        """Create subwidget and place it in grid.

        :param cls: a `tkinter` widget class to construct
        :param parent: the parent widget
        :param kwargs: arguments for constructor
        """
        if parent is None:
            parent = self
        x = cls(parent, **kwargs)
        x.grid(row=row, column=column, rowspan=rowspan, columnspan=colspan, sticky='NEWS')
        return x

    def __create_widgets(self):
        """Create all the widgets."""
        self.bold = font.Font(weight='bold')

        self.tape_frame = self.__new_widget(ttk.Frame, 0, 0)
        self.tape = []
        for i in range(self.tape_size):
            def to_reg(i=i):
                return self.controller._tape_check(i)
            vc = self.register(to_reg)
            a = self.__new_widget(
                ttk.Entry, 0, i, parent=self.tape_frame,
                width=1, justify='center',
                textvariable=self.controller.tape[i],
                validate='focusout', validatecommand=vc
            )
            self.tape.append(a)
        i = self.model.position - self.controller.tape_start
        if 0 <= i < self.tape_size:
            self.tape[i]['font'] = self.bold
        self.__set_weight(self.tape_frame)

        machine_settings = self.__new_widget(ttk.Frame, 1, 0)

        vc = self.register(self.controller._alphabet_check)
        self.alphabet = self.__new_widget(
            ttk.Entry, 0, 0, parent=machine_settings,
            textvariable=self.controller.alphabet, validate='focusout',
            validatecommand=vc
        )

        self.tacts = self.__new_widget(ttk.Label, 0, 1, parent=machine_settings, textvariable=self.controller.tacts)
        self.make_step = self.__new_widget(ttk.Button, 0, 3, parent=machine_settings, text=_('Step'), command=self.controller._step)
        self.go = self.__new_widget(ttk.Button, 0, 2, parent=machine_settings, text=_('Go'), command=self.controller._go)

        self.__set_weight(machine_settings)

        self.rules = self.__new_widget(ttk.Frame, 2, 0)
        self.controller._update_rules()

        file_io = self.__new_widget(ttk.Frame, 3, 0)
        self.load = self.__new_widget(ttk.Button, 0, 0, parent=file_io, text=_('Load'))
        self.save = self.__new_widget(ttk.Button, 0, 1, parent=file_io, text=_('Save'))
        self.__set_weight(file_io)

    def _update_rules(self):
        """Recreate the rules table."""
        self.rules.destroy()
        self.rules = self.__new_widget(ttk.Frame, 2, 0)
        self.__new_widget(ttk.Label, 0, 0, colspan=2, parent=self.rules, text=_('States \\ Chars'))

        for j, c in enumerate(self.model.alphabet):
            self.__new_widget(ttk.Label, 0, j + 2, parent=self.rules, text=c)
        for i, s in enumerate(self.model.rules):
            def to_reg1(s=s):
                return self.controller._delete_state(s)
            vc = self.register(to_reg1)
            self.__new_widget(ttk.Button, i + 1, 0, parent=self.rules, text='x', command=vc)

            def to_reg(s=s):
                return self.controller._state_check(s)

            vc = self.register(to_reg)
            self.__new_widget(
                ttk.Entry, i + 1, 1, parent=self.rules,
                width=5, justify='center',
                textvariable=self.controller.rules[s],
                validate='focusout',
                validatecommand=vc
            )
            for j, c in enumerate(self.model.alphabet):
                def to_reg(s=s, c=c):
                    return self.controller._rule_check(s, c)
                vc = self.register(to_reg)
                self.__new_widget(
                    ttk.Entry, i + 1, j + 2, parent=self.rules,
                    textvariable=self.controller.rules[s, c], validate='focusout',
                    validatecommand=vc
                )

        lll = len(self.model.rules)

        def to_reg(s=''):
            return self.controller._state_check(s)

        vc = self.register(to_reg)
        self.__new_widget(
            ttk.Entry, 1 + lll, 1, parent=self.rules,
            textvariable=self.controller.rules[''], validate='focusout',
            validatecommand=vc
        )
        self.__set_weight(self.rules)


class Controller:
    """Stores and manipulates control variables for view–model communication."""
    def __init__(self, view: View, machine: TuringMachine):
        """
        :param view: widgets to work with
        :param machine: the model of Turing machine to work with
        """
        self.model = machine
        self.view = view

        self.alphabet = tk.StringVar()
        self.alphabet.set(self.model.alphabet[:-1])

        self.radius = self.view.tape_size // 2
        self.tape_start = self.model.position - self.radius

        self.tape = {}
        for i in range(self.view.tape_size):
            self.tape[self.model.position + i] = tk.StringVar()
            self.tape[self.model.position + i].set(self.model.tape[self.tape_start + i])

        self.tacts_counter = 0
        self.tacts_title = _("Tacts: ")
        self.tacts = tk.StringVar()
        self.tacts.set(self.tacts_title + str(self.tacts_counter))

        self.stashed = dict()

    def _tape_check(self, i: int):
        """Check change to the tape.

        :param i: index of changed cell
        """
        old = self.model.tape[self.tape_start + i]
        new = self.tape[i].get()
        if new == old:
            return False
        if len(new) == 0:  # XXX keep this feature?
            self.model.tape[self.tape_start + i] = LAMBDA
            self.tape[i].set(LAMBDA)
            return True
        if len(new) != 1 or new not in self.model.alphabet:
            self.tape[i].set(old)
            return False
        self.model.tape[self.tape_start + i] = new
        return True

    def _update_rules(self, remove=''):
        """Add or remove entries for rules.

        :param remove: characters to remove from machine model as they are removed from the alphabet
        :type remove: container of characters
        """

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

        self.view._update_rules()

    def _delete_state(self, s: str):
        """Remove the state from the machine."""
        self.model.rules.pop(s)
        self._update_rules()

    def _state_check(self, s: str):
        """Check state name to be unique.

        :param s: the state that is renamed or '' in case of adding a new state
        """
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
        self._update_rules()
        return True

    def _rule_check(self, state: str, char: str):
        """Check the rule entry to be correct triple.

        :param state: state
        """
        from re import split
        result = split(r'[,\s]+', self.rules[state, char].get())
        if len(result) != 3 or result[0] not in self.model.alphabet or result[1] not in 'nrlNRL' or '!' != result[2] not in self.model.rules:
            old = self.model.rules[state].get(char, '')
            if old:
                self.rules[state, char].set(old)
            return False
        self.model.rules[state][char] = result
        return True

    def _alphabet_check(self):
        """Check the alphabet entry to consist of unique symbols."""
        old = self.model.alphabet
        new = self.alphabet.get()
        if old[:-1] == new:
            return False
        if len(set(new)) == len(new):
            new += LAMBDA
            self.model.alphabet = new
            self.model.tape.filter(new)
            self._update_rules([c for c in old if c not in new])
            self.tape_start = self.model.position - self.radius
            for i, v in self.tape.items():
                v.set(self.model.tape[self.tape_start + i])
            return True
        self.alphabet.set(old[:-1])
        return False

    def _step(self):
        """Advance the Turing machine one tact."""
        result = self.model.run(max_tacts=1)
        self.__update_tape(result)

    def _go(self):
        """Run the Turing machine till it stops or tacts limit exceeds."""
        result = self.model.run()
        self.__update_tape(result)

    def __update_tape(self, result):
        """Update the tape."""
        if result['iterations'] == 0:
            return  # the machine has stopped
        self.tacts_counter += result['iterations']
        self.tacts.set(self.tacts_title + str(self.tacts_counter))
        self.tape_start = self.model.position - self.radius
        for i, v in self.tape.items():
            v.set(self.model.tape[self.tape_start + i])


def main():
    gettext.install('turing_machine', localedir=os.path.dirname(__file__))

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


if __name__ == "__main__":
    main()
