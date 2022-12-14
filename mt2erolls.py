from rpgroller.roller import roll
from random import randint

def rollparse(target):
    '''Converts something like 'int 7+' into (int, 7).
    It does this by removing the implied + at the end, so it had better be there.'''
    characteristic, target = target[:-1].split()
    target = int(target)
    return characteristic, target

def rd66():
    '''Rolls d66'''
    return randint(1,6) * 10 + randint(1,6)

def one_third():
    '''Returns success or failure for a 1/3 check.'''
    return randint(1,3) == 1

def coin_toss():
    '''Returns success or failure for a 1/2 check.'''
    return randint(1,2) == 1

def roll_normal():
    '''Rolls 2d6.'''
    return roll('2d6')

def roll_boon():
    '''Rolls 3d6, keeping highest 2.'''
    return roll('3d6kh2')

def roll_bane():
    '''Rolls 3d6, keeping lowest 2.'''
    return roll('3d6kl2')

def pick_roll_method(rolltype='normal'):
    '''returns a roll method based on rolltype (a string).
    rolltype can bet set to 'boon' or 'bane' if desired.'''
    if rolltype == 'normal':
        return roll_normal
    elif rolltype == 'boon':
        return roll_boon
    elif rolltype == 'bane':
        return roll_bane
    assert False, 'Roll type not recognized.'
