from collections import defaultdict
from turing_machine.constants import LAMBDA


class Tape:
    """Infinite tape of characters."""
    def __init__(self, input: str = ''):
        self._chars = defaultdict(lambda: LAMBDA)
        self._chars.update(enumerate(input))
        self._left = 0
        self._right = len(input)

    def __getitem__(self, key):
        return self._chars[key]

    def __setitem__(self, key, value):
        if value != LAMBDA:
            self._chars[key] = value
        elif key in self._chars:
            self._chars.pop(key)

        self._right = max(self._chars.keys()) + 1
        self._left = min(self._chars.keys())

    def __str__(self):
        return ''.join(self._chars[i] for i in range(self._left, self._right))

    def string_with_position(self, head: int):
        """String representation with head position marked in []"""
        if head < self._left:
            return f'[{LAMBDA}]' + LAMBDA * (self._left - head - 1) + str(self)
        if head >= self._right:
            return str(self) + LAMBDA * (head - self._right) + f'[{LAMBDA}]'

        left = ''.join(self._chars[i] for i in range(self._left, head))
        curr = f'[{self._chars[head]}]'
        right = ''.join(self._chars[i] for i in range(head + 1, self._right))
        return left + curr + right
