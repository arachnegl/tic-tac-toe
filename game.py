import re

from unittest import TestCase

X = 'X'
O = 'O'


def new_game():
    return (
        (None, None, None),
        (None, None, None),
        (None, None, None),
    )


def get_value(axis, type_=str):
    assert type_ is int or type_ is str, type_
    got = None
    attempts = 5
    while got is None:
        inputted = input('{}: '.format(axis))
        try:
            got = type_(inputted)
        except:
            print('you inputted {} must be {}'.format(inputted, type_))
            pass
    return got


def play():
    g = new_game()
    x = input('x ')
    y = input('y ')
    print(g)


if __name__ == '__main__':
    play()


class TestGame(TestCase):

    def test_can_play(self):
        pass
