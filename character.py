#!/usr/bin/python3
'''Characters and injuries.'''
from mt2erolls import pick_roll_method
from mt2emechanics import  characteristic_modifier, educations, characteristics

def parse_gain_skill(desc):
    assert False, 'ensure that skill is in skill list here.'
    '''Helper for Character.gain_skill
    Splits 'carouse 1' into ('carouse', '=', 1).
    Splits 'carouse +1' into ('carouse', '+'.'''
    skill, rest = desc.split()
    if rest[0] == '+':
        mod = '+'
        rest = rest[1:]
    else:
        mod = '='
    val = int(rest)
    return skill, mod, val

class Character:
    def __init__(self, characteristic_method='normal'):
        '''characteristic_method can bet set to 'boon' or 'bane' if desired.'''
        if characteristic_method is not None:
            self.gen(characteristic_method)

    def gain_skill(self, desc):
        '''Character gains a skill.
        desc examples: carouse 0, carouse 1, carouse +1'''
        skill, mod, val = parse_gain_skill(desc)
        if mod == '=':
            if skill not in self.skills or self.skills[skill] < val:
                # Will not reduce a skill.
                self.skills[skill] = val
        elif mod == '+':
            if skill not in self.skills:
                self.skills[skill] = val
            else:
                self.skills[skill] += val
        else:
            assert False, f'Unknown modifier for gaining a skill: {mod}'

    def gen(self, characteristic_method='normal'):
        self.terms=1
        self.can_test_psi = False
        self.next_career = None
        self.drafted = False
        self.allies = []
        self.rivals = []
        self.enemies = []
        self.log = []

        characteristic_method = pick_roll_method(characteristic_method)

        characteristic_rolls = []
        for x in range(6):
            characteristic_rolls.append(characteristic_method())
        self.str, self.dex, self.end, self.int, self.edu, self.soc = characteristic_rolls


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
        characteristic, target = roll_parse(target)
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
        characteristic, target = roll_parse(target)
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
    

