import re

from collections import Counter


class StateInvalid(Exception):
    pass


class State:
    def __init__(self, state):
        self.state = state
        if not self.is_valid():
            raise StateInvalid(state)

    def get_row(self, i):
        assert 0 <= i <= 2, i
        end = 3 * (i + 1)
        start = end - 3
        return self.state[start: end]

    def get_col(self, i):
        assert 0 <= i <= 2, i
        return self.state[i::3]

    def get_diag_1(self):
        s = self.state
        return s[0] + s[4] + s[8]

    def get_diag_2(self):
        s = self.state
        return s[2] + s[4] + s[6]

    def has_won(self, player):
        wins = self.get_wins()
        if 1 <= len(wins) <= 2:
            return wins[0] == player
        return None

    def get_wins(self):
        """Return a list of player wins.

        More than one win would indicate an invalid state.
        """
        checks = (
            self.get_row(0), self.get_row(1), self.get_row(2),
            self.get_col(0), self.get_col(1), self.get_col(2),
            self.get_diag_1(), self.get_diag_2(),
        )
        wins = []
        for c in checks:
            win = self.get_player_if_won(c)
            if win:
                wins.append(win)
        return wins

    @classmethod
    def get_player_if_won(cls, plays):
        assert len(plays) == 3, plays

        def all_(s):
            return all([p == s for p in plays])

        if all_('x'):
            return 'x'
        if all_('o'):
            return 'o'
        return None

    def is_valid(self):
        """Validates the state of the game.

        Assumption: it is always 'o's turn.
        """
        # Check state representation is valid
        if not re.match(r'^[ox ]{9}$', self.state):
            return False

        # A player's turn has been skipped
        counts = Counter(self.state)
        if abs(counts['o'] - counts['x']) > 1:
            return False

        # If there is a winner there can only be one
        wins = self.get_wins()
        if len(wins) == 2:
            # The same player can validly win twice
            if not wins[0] == wins[1]:
                return False
        if len(wins) > 2:
            return False

        return True  # All checks passed

    def is_terminal(self):
        if self.state.count(' ') == 0:
            return True
        if len(self.get_wins()) == 1:
            return True
        return False

    def is_draw(self):
        if self.state.count(' ') == 0 and len(self.get_wins()) == 0:
            assert not self.has_won('x')
            assert not self.has_won('o')
            return True
        return False

    def __repr__(self):
        return (
            '{}|{}|{}\n'.format(*self.get_row(0).upper()) +
            '-+-+-\n' +
            '{}|{}|{}\n'.format(*self.get_row(1).upper()) +
            '-+-+-\n' +
            '{}|{}|{}\n'.format(*self.get_row(2).upper())
        )

    def __eq__(self, state):
        if isinstance(state, str):
            return self.state == state
        return self.state == state.state


class Node:
    """Always play 'o'
    """
    def __init__(self, state, parent=None, depth=None):
        self.state = State(state)
        self.parent = parent
        self.children = []
        self.depth = depth
        self.value = None

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return self.children == []

    def create_children(self, depth=0):
        player = 'o' if not depth % 2 else 'x'
        # Base Case
        if self.state.is_terminal():
            # print(
            #     '{} {} player: {} wins: {}'
            #     .format(depth * '-', self, player, self.state.get_wins())
            # )
            # leaf, no children
            return
        # Recursive Case
        parent_state = self.state.state
        for i, play in enumerate(parent_state):
            if not play == ' ':
                continue
            # Generate new Child
            child_state = list(parent_state)
            child_state[i] = player
            child_state = ''.join(child_state)
            child = Node(child_state, parent=self, depth=depth)
            # Depth First
            if not child.state.is_terminal():
                child.create_children(depth=depth + 1)
            self.children.append(child)
            # print(
            #     '{} - {} plays - wins: {}'
            #     .format(child, player, child.state.get_wins())
            # )
        assert len(self.children) == parent_state.count(' ')

    def mini_max(self):
        max_val = self.max_value()
        for node in self.children:
            if node.value == max_val:
                return node.state

    def max_value(self):
        if self.state.is_terminal():
            self.value = self.utility()
            return self.value
        val = -float("inf")
        for child in self.children:
            val = max(val, child.min_value())
        self.value = val
        return val

    def min_value(self):
        if self.state.is_terminal():
            self.value = self.utility()
            return self.value
        val = float("inf")
        for child in self.children:
            val = min(val, child.max_value())
        self.value = val
        return val

    def utility(self):
        if self.state.has_won('o'):
            return 10
        elif self.state.has_won('x'):
            return -10
        else:
            return 0

    def __repr__(self):
        return 'Node - state: <{}>, depth: {}, children: {}'.format(
            self.state.state, self.depth, len(self.children)
        )


def tic_tac_toe(state):
    game = Node(state)
    game.create_children()
    return game.mini_max().state
