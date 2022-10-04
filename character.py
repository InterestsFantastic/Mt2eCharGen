#!/usr/bin/python3
from mt2e_mechanics import roll_normal, roll_boon, roll_bane, \
    characteristic_modifier, educations, rollparse, characteristic_modifiers
from copy import copy

class Character:
    def __init__(self, gen_method='normal'):
        '''gen_method can bet set to 'boon' or 'bane' if desired.'''
        if gen_method is not None:
            self.gen(gen_method)

    def gen(self, gen_method='normal'):
        self.terms=1
        self.log = []

        # Pick appropriate rolling function to call.        
        if gen_method == 'normal':
            characteristic_diceroll = roll_normal
        elif gen_method == 'boon':
            characteristic_diceroll = roll_boon
        elif gen_method == 'bane':
            characteristic_diceroll = roll_bane

        characteristic_rolls = []
        for x in range(6):
            characteristic_rolls.append(characteristic_diceroll())
        # copy may be unnecessary here.
        self.str, self.dex, self.end, self.int, self.edu, self.soc = copy(characteristic_rolls)


    def characteristic_modifier(self, characteristic):
        '''Returns the characteristic modifier resultant from having a characteristic at a certain value, e.g. int returns 0 if character's int is 7.'''
        score = getattr(self, characteristic)
        return characteristic_modifier(score)
        
    def characteristic_roll(self, target, dm=0, rolltype = 'normal'):
        '''Rolls dice against a target using characteristic OR skill modifier.
        In the case of the latter, useful mostly during career progression.
        Will handle rolltype 'boon' and 'bane'.
        The assumption is that all rolls will be +'''
        # Pick appropriate rolling function to call.
        rollmethod = roll_normal
        if rolltype == 'boon':
            rollmethod = roll_boon
        elif rolltype == 'bane':
            rollemethod = roll_bane

        # Splits characteristic and target number and removes the + at the end.
        characteristic, target = rollparse(target)
        if characteristic in characteristic_modifiers:
            dm += self.characteristic_modifier(characteristic)

        thisroll = rollmethod()
        return thisroll + dm >= target
                
    def print_characteristics(self):
        print(self.str, self.dex, self.end, self.int, self.edu, self.soc)

if __name__ == '__main__':
    c = Character()
    c.print_characteristics()
    print('str mod: ', c.characteristic_modifier('str'))
    educations[0].attempt_entry(c)
    print(c.log)
    

print('hello world') #testing github stuff
