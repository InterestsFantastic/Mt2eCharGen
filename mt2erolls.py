from rpgroller.roller import roll
from random import randint

def rollparse(target):
    '''Converts something like 'int 7+' into (int, 7).'''
    characteristic, target = target[:-1].split()
    target = int(target)
    return characteristic, target

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
