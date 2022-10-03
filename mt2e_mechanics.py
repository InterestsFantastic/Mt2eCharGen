#!/usr/bin/python3
from rpgroller.roller import roll
from random import randint
from ODSReader.odsreader import ODSReader
from ODSReader.utils import keyval

mechanics_file = 'mt2e_mechanics.ods'
mechanics = ODSReader(mechanics_file, clonespannedcolumns=True)

characteristic_modifiers = mechanics.getSheet('CharacteristicModifiers')
characteristic_modifiers = keyval(characteristic_modifiers, int)
def characteristic_modifier(num):
    '''Returns the diceroll modifier for having a particular value
    in a characteristic'''
    if num in characteristic_modifiers:
        return characteristic_modifiers[num]
    elif num > 14:
        return 3
    assert False, f'Improper characteristic modifier requested: {num}'

noble_titles = mechanics.getSheet('NobleTitles')
noble_titles = keyval(noble_titles, int, str)
def noble_title(num):
    '''Returns the noble title of a social status.'''
    if num in noble_titles:
        return noble_titles[num]
    else:
        return None


def rd66():
    return randint(1,6) * 10 + randint(1,6)

def one_third():
    '''Returns success or failure for a 1/3 check.'''
    return randint(1,3) == 1

def coin_toss():
    '''Returns success or failure for a 1/2 check.'''
    return randint(1,2) == 1

def roll_normal():
    return roll('2d6')

def roll_boon():
    return roll('3d6kh2')

def roll_bane():
    return roll('3d6kl2')

