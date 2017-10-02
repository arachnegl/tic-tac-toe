from unittest import TestCase

from game_tree import Node, State, StateInvalid


class TestState(TestCase):
    # To run tests:
    # python -m unittest game_tree.TestState

    def test_is_valid(self):
        assert State('ooxxoxoxx').is_valid()
        assert State('    o    ').is_valid()
        with self.assertRaises(StateInvalid):
            State('oooxoxxxx').is_valid()

    def test_get_rows(self):
        st = State('xxxo o o ')
        assert st.get_row(0) == 'xxx'
        assert st.get_row(1) == 'o o'
        assert st.get_row(2) == ' o '

    def test_get_cols(self):
        st = State('x oxo x o')
        assert st.get_col(0) == 'xxx'
        assert st.get_col(1) == ' o '
        assert st.get_col(2) == 'o o'

    def test_diags(self):
        assert State('xo oxo ox').get_diag_1() == 'xxx'
        assert State('o xoxoxo ').get_diag_2() == 'xxx'

    def test_has_won(self):
        assert State('xo oxo ox').has_won('x')
        assert State(' ooxoxxox').has_won('o')

    def test_is_terminal(self):
        assert State('xxx o  oo').is_terminal()
        assert State(' o xox o ').is_terminal()


class TestGame(TestCase):
    # To run tests:
    # python -m unittest game_tree.TestGame
    def test_create_children(self):
        root = Node('o   xoxox')
        root.create_children()

        assert root.state == 'o   xoxox'

        # Depth 0 'o' plays
        assert [n.state for n in root.children] == [
            'oo  xoxox', 'o o xoxox', 'o  oxoxox'
        ]

        # Depth 1 'x' plays
        assert [n.state for n in root.children[0].children] == [
            'oox xoxox', 'oo xxoxox',
        ]
        assert [n.state for n in root.children[1].children] == [
            'oxo xoxox', 'o oxxoxox'
        ]
        assert [n.state for n in root.children[2].children] == [
            'ox oxoxox', 'o xoxoxox'
        ]
        assert root.children[0].children[0].is_leaf()
        assert root.children[0].children[0].state.has_won('x')

        # Depth 2 'o' plays
        assert [n.state for n in root.children[0].children[1].children] == [
            'oooxxoxox'
        ]
        assert [n.state for n in root.children[1].children[0].children] == [
            'oxooxoxox'
        ]
        assert root.children[0].children[1].children[0].is_leaf()
        assert root.children[0].children[1].children[0].state.has_won('o')
        assert root.children[1].children[0].children[0].is_leaf()
        assert root.children[1].children[0].children[0].state.is_draw()

    def test_mini_max(self):
        root = Node('o   xoxox')
        root.create_children()
        got = root.mini_max()
        self.assertEqual(got, 'o o xoxox')

    def test_mini_max_spec(self):
        root = Node(' xxo  o  ')
        root.create_children()
        got = root.mini_max()
        self.assertEqual(got, 'oxxo  o  ')

    def test_aaron(self):
        root = Node('  xoo x  ')
        root.create_children()
        got = root.mini_max()
        self.assertEqual(got, '  xooox  ')
