'''Characters and injuries.'''
from mt2erolls import pick_roll_method
from mechanics import  characteristic_modifier, characteristics, randphys, \
     phys_characteristics, skills, findskill, char_zeros, people, \
     char_counters, psi_test_price
from rpgroller.roller import roll
from random import choice
from TravellerLetterNumbers.travellerletternumbers import numbers_to_letters
from utils import set_zeros, default_second_elem

def parse_gain_skill(desc):
    '''Helper for Character.gain_skill
    Splits 'carouse 1' into ('Carouse', '=', 1).
    Splits 'carouse +1' into ('Carouse', '+', 1).
    If skill is not found it will return None and therefore you want to make
    sure that you aren't expecting multiple args if it can fail.'''

    *skill, val = desc.split(' ')
    if len(desc) == 1:
        skill = skill[0]
    else:
        # eg "vacc suit"
        skill = ' '.join(skill)
    skill = findskill(skill)
    if not skill:
        return None

    assert val[0] != '-', 'Losing skills not supported.'
    mod = '+' if val[0] == '+' else '='
    val = int(val)
    return skill, mod, val

class Character:
    def __init__(self, characteristic_method='normal'):
        '''characteristic_method can bet set to 'boon' or 'bane' if desired.'''
        if characteristic_method is not None:
            self.gen(characteristic_method)
        self.skills = {}
        self.benefit_dms = []
        self.agent = 'agent'
        set_zeros(self, people)
        set_zeros(self, char_zeros)

    def test_psi(self):
        '''Tests psionic strength.'''
        self.cr -= psi_test_price
        self.psi = roll(f'2d6-{self.terms}', min1=False)
        result = self.psi > 0
        if result:
            self.next_career = 'psi'
            return f'Character found to possess {self.psi} psionic strength.'
        else:
            return 'Character not found to possess psionic strength.'

    def gain(self, gained):
        '''Gain something, like a skill, ally, ally 2, etc.'''
        if parse_gain_skill(gained):
            return self.gain_skill(gained)

        parts = gained.split(' ')
        if parts[0] in char_counters:
            change = default_second_elem(parts)
            setattr(self, parts[0], getattr(self, parts[0]) + change)
            return f'Gained {change} {parts[0]}.'

    def handle_cascade(self, skill):
        '''Game mechanics dictate that if you get drive 0 it applies to all cascaded driving skills, such as Drive (Tracked).'''
        # Creating output that logs each change to a skill.
        out = ''
        for s in skills:
            if skills[s]['cascade_from'] == skill:
                gain_result = self.gain_skill(f'{s} 0')
                if gain_result != 'No effect.':
                    out += gain_result + ' '
        # Removing trailing space. Ensuring _some_ output.
        out = 'No effect.' if out == '' else out[:-1]
        return out
    
    def gain_skill(self, desc):
        '''Character gains a skill.
        desc examples: carouse 0, carouse 1, carouse +1'''
        skill, mod, val = parse_gain_skill(desc)

        if skills[skill]['cascade']:
            assert val == 0, f'Can not take cascading skill {skill} at a level other than 0.'
            return self.handle_cascade(skill)

        if skill not in self.skills:
            self.skills[skill] = val
        elif mod == '=' and self.skills[skill] < val:
            # Will not reduce a skill.
            self.skills[skill] = val
        elif mod == '+':
            self.skills[skill] += val
        else:
            return 'No effect.'

        if skills[skill]['cascade_from']:
            assert False, 'Not done.'

        return f'Skill {skill} becomes {self.skills[skill]}.'

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


    def injure(self, num=0):
        '''Character is injured. You can specify an injury (sometimes you
        would roll twice and pick the lowest dice or something to that
        effect.'''
        assert 0 <= num <= 6, f'Invalid injury number {num}'

        # By default, roll 1d6.
        if num == 0:
            num = roll('1d6')

        if num == 1:
            out  = 'Nearly killed – reduce one physical characteristic by 1D, reduce two other physical characteristics by 2.'
            phys = randphys()
            reduction = roll('1d6')
            setattr(self, phys, getattr(self, phys) - reduction)
            for pc in phys_characteristics:
                if pc != phys:
                    setattr(self, pc, getattr(self, pc) - 2)
            out += f' Result: {phys} reduced by {reduction} and the others by 2.'
        elif num == 2:
            out  = 'Severely injured – reduce one physical characteristic by 1D.'
            phys = randphys()
            reduction = roll('1d6')
            setattr(self, phys, getattr(self, phys) - reduction)
            out += f' Result: {phys} reduced by {reduction}.'
        elif num == 3:
            out  = 'Missing Eye or Limb – reduce STR or DEX by 2.'
            phys = choice(['str', 'dex'])
            reduction = 2
            setattr(self, phys, getattr(self, phys) - reduction)
            out += f' Result: {phys} reduced by {reduction}.'
        elif num == 4:
            out  = 'Scarred – you are scarred and injured. Reduce any physical characteristic by 2.'
            phys = randphys()
            reduction = 2
            setattr(self, phys, getattr(self, phys) - reduction)
            out += f' Result: {phys} reduced by {reduction}.'
        elif num == 5:
            out  = 'Injured. Reduce any physical characteristic by 1.'
            phys = randphys()
            reduction = 1
            setattr(self, phys, getattr(self, phys) - reduction)
            out += f' Result: {phys} reduced by {reduction}.'
        else:
            out = 'No effect.'
        return out

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
                
    @property
    def upp(self):
        '''Returns character's UPP.'''
        return numbers_to_letters([self.str, self.dex, self.end, self.int, self.edu, self.soc])

    @property
    def characteristics_string(self):
        '''Returns string of tuple of characteristics.'''
        return str((self.str, self.dex, self.end, self.int, self.edu, self.soc))

    @property
    def char_description(self):
        characterline = f'Character: {self.upp}.'
        peopleline = ''
        for p in people:
            peopleline += f'{p.title()}: {getattr(self, p)}\t'
        skillsline = f'Skills: {self.skills}'
        desc = '\n'.join([characterline, peopleline, skillsline])
        return desc
    
if __name__ == '__main__':
    c = Character()
    print(f'Character created with characteristics: {c.characteristics_string}')
##    print('str mod: ', c.characteristic_modifier('str'))
##    educations[0].attempt_entry(c)
##    print(c.log)
    

