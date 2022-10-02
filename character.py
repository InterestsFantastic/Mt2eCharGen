#!/usr/bin/python3
from mt2e_mechanics import roll_normal, roll_boon, roll_bane, \
    characteristic_modifier
from copy import copy

class Character:
    def __init__(self, gen_method='normal'):
        '''gen_method can bet set to 'boon' or 'bane' if desired.'''
        self.gen(gen_method)

    def gen(self, gen_method):
        # Pick appropriate rolling function to call.
        if gen_method == 'normal':
            attribute_diceroll = roll_normal
        if gen_method == 'boon':
            attribute_diceroll = roll_boon
        if gen_method == 'bane':
            attribute_diceroll = roll_bane

        attrib_rolls = []
        for x in range(6):
            attrib_rolls.append(attribute_diceroll())
        # copy may be unnecessary here.
        self.str, self.dex, self.end, self.int, self.edu, self.soc = copy(attrib_rolls)


    def characteristic_modifier(self, characteristic):
        '''Returns the characteristic modifier resultant from having a characteristic at a certain value, e.g. int returns 0 if character's int is 7.'''
        # What does getattr return if attr not found?
        score = getattr(self, characteristic)
        return characteristic_modifier(score)
        
    def characteristic_roll(self, target, rolltype = 'normal'):
        '''Rolls dice against a target using characteristic modifier.
        Will handle rolltype 'boon' and 'bane'.
        Assumption is that all rolls will be +'''
        # Pick appropriate rolling function to call.
        rollmethod = roll_normal
        if rolltype == 'boon':
            rollmethod = roll_boon
        elif rolltype == 'bane':
            rollemethod = roll_bane

        # Splits characteristic and target number and removes the + at the end.
        characteristic, target = target[:-1].split()
        target = int(target)

        thisroll = rollmethod()
        return thisroll + self.characteristic_modifier(characteristic) >= target
                
    def print_attribs(self):
        print(self.str, self.dex, self.end, self.int, self.edu, self.soc)

if __name__ == '__main__':
    c = Character()
    c.print_attribs()
    print('str mod: ', c.characteristic_modifier('str'))

