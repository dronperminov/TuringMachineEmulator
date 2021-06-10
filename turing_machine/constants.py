"""
Constants used in Turing machine model.
"""

LAMBDA = 'λ'
"""Marks empty cell on a Turing machine tape."""

STOP_STATE = '!'
"""The state of a Turing machine, which marks end of its run."""

MOVE_LEFT = 'L'
"""Marks next move of a machine: one cell to the left."""
MOVE_NONE = 'N'
"""Next move of a machine is to stay at the same cell."""
MOVE_RIGHT = 'R'
"""Marks next move of a machine: one cell to the right."""

SUCCESSFUL_STATUS = "successful"
"""Result status of a machine run, means machine has stopped."""
MAX_ITERATIONS_REACHED_STATUS = "max iterations reached"
"""Result status of a machine run, means machine needs more tacts to proceed."""
MAX_ITERATIONS = 9999
"""The tacts limit for a machine run."""

NORMAL_MODE = "normal"
"""When machine runs, do not save information about every step."""
BY_STEP_MODE = "by step"
"""When machine runs, do save information about every step."""
