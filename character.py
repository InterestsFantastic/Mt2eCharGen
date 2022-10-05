#!/usr/bin/python3
from mt2erolls import roll_normal, roll_boon, roll_bane, pick_roll_method, rollparse
from mt2emechanics import  characteristic_modifier, educations, characteristic_modifiers
from copy import copy

characteristics = 'str dex end int edu soc'.split()

class Character:
    def __init__(self, gen_method='normal'):
        '''gen_method can bet set to 'boon' or 'bane' if desired.'''
        if gen_method is not None:
            self.gen(gen_method)

    def gen(self, gen_method='normal'):
        self.terms=1
        self.can_test_psi = False
        self.next_career = None
        self.drafted = False
        self.allies = []
        self.rivals = []
        self.enemies = []
        self.log = []

        gen_method = pick_roll_method(gen_method)

        characteristic_rolls = []
        for x in range(6):
            characteristic_rolls.append(gen_method())
        # copy may be unnecessary here.
        self.str, self.dex, self.end, self.int, self.edu, self.soc = copy(characteristic_rolls)


    def gain_ally(self):
        self.allies.append('I')
    def gain_rival(self):
        self.rivals.append('I')
    def gain_enemy(self):
        self.enemies.append('I')
        
    def characteristic_modifier(self, characteristic):
        '''Returns the characteristic modifier resultant from having a characteristic at a certain value, e.g. int returns 0 if character's int is 7.'''
        score = getattr(self, characteristic)
        return characteristic_modifier(score)
        
    def check_characteristic(self, target):
        '''Checks to see if character has e.g. 'int 8+'.'''
        characteristic, target = rollparse(target)
        if characteristic in characteristics:
            return getattr(self, characteristic) >= target
        else:
            assert False, f'skill is being searched for? {characteristic}'

    def characteristic_roll(self, target, dm=0, rollmethod='normal', extras=None):
        '''Rolls dice against a target using characteristic OR skill modifier.
        In the case of the latter, useful mostly during career progression.
        Will handle rolltype 'boon' and 'bane'.
        The assumption is that all rolls will be +
        Normally the function returns only pass/fail but if you argue
        'modified' in extras you will get the final roll as well, and
        'unmodified' will return the base roll.'''

        # Splits characteristic and target number and removes the + at the end.
        characteristic, target = rollparse(target)
        if characteristic in characteristics:
            dm += self.characteristic_modifier(characteristic)
        else:
            assert False, f'skill is being searched for? {characteristic}'
        
        thisroll = pick_roll_method(rollmethod)()
        if extras is None:
            return thisroll + dm >= target
        elif extras == 'modified':
            return thisroll + dm >= target, thisroll + dm
        elif extras == 'unmodified':
            return thisroll + dm >= target, thisroll
        else:
            assert False, f'unknown extras specification {extras}'
                
    def print_characteristics(self):
        print(self.str, self.dex, self.end, self.int, self.edu, self.soc)

if __name__ == '__main__':
    c = Character()
    c.print_characteristics()
    print('str mod: ', c.characteristic_modifier('str'))
    educations[0].attempt_entry(c)
    print(c.log)
    

