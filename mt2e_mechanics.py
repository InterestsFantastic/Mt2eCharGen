#!/usr/bin/python3
from rpgroller.roller import roll

def roll_normal():
    return roll('2d6')

def roll_boon():
    return roll('3d6kh2')

def roll_bane():
    return roll('3d6kl2')

characteristic_modifiers = {
    0: -3,
    1: -2,
    2: -2,
    3: -1,
    4: -1,
    5: -1,
    6: 0,
    7: 0,
    8: 0,
    9: 1,
    10: 1,
    11: 1,
    12: 2,
    13: 2,
    14: 2}

def characteristic_modifier(num):
    '''Returns the diceroll modifier for having a particular value
    in a characteristic'''
    if num in characteristic_modifiers:
        return characteristic_modifiers[num]
    elif num > 14:
        return 3
    assert False, f'Improper characteristic modifier requested: {num}'

