"""
Graphical user interface for Turing machine, using Tkinter.
"""
import tkinter as tk
from tkinter import ttk


class GraphicalInterface(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('Turing Machine Emulator')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        self.set_weight(self)

    @staticmethod
    def set_weight(widget):
        """Set all cells' weight to 1."""
        for column in range(widget.grid_size()[0]):
            widget.columnconfigure(column, weight=1)
        for row in range(widget.grid_size()[1]):
            widget.rowconfigure(row, weight=1)

    def new_widget(self, cls, row, column, parent=None, **kwargs):
        """Create subwidget and place it in grid automatically."""
        if parent is None:
            parent = self
        x = cls(parent, **kwargs)
        x.grid(row=row, column=column, sticky='NEWS')
        return x

    def no_repeats(self, prev:str):
        """Check the alphabet entry."""
        if len(set(self.alphabet_var.get())) == len(self.alphabet_var.get()):
            self.update_rules()
            return True
        self.alphabet_var.set(prev)
        return False

    def create_widgets(self):
        """Create all the widgets."""
        self.alphabet_var = tk.StringVar()

        self.tape = self.new_widget(ttk.Frame, 0, 0)
        # for i, c in enumerate('12334'):
        self.new_widget(ttk.Label, 0, 0, parent=self.tape, textvariable=self.alphabet_var)
        self.set_weight(self.tape)

        machine_settings = self.new_widget(ttk.Frame, 1, 0)

        vc = self.register(self.no_repeats)
        self.alphabet = self.new_widget(ttk.Entry, 0, 0, parent=machine_settings,
            textvariable=self.alphabet_var, validate='focusout', validatecommand=(vc, '%s'))  # code for 'value before change'

        self.tacts = self.new_widget(ttk.Label, 0, 1, parent=machine_settings, text='Tacts:')
        self.go = self.new_widget(ttk.Button, 0, 2, parent=machine_settings, text='Go')
        self.makestep = self.new_widget(ttk.Button, 0, 3, parent=machine_settings, text='Step')

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
        for i in range(len('states')):
            self.new_widget(ttk.Label, i + 1, 0, parent=self.rules, text='q' + str(i))

        for j, c in enumerate(self.alphabet_var.get()):
            self.new_widget(ttk.Label, 0, j + 1, parent=self.rules, text=c)
        for i in range(len('states')):
            for j, c in enumerate(self.alphabet_var.get()):
                self.new_widget(ttk.Label, i + 1, j + 1, parent=self.rules, text='j, N, ' + c)
        self.set_weight(self.rules)


if (__name__ == "__main__"):
    GraphicalInterface().mainloop()
