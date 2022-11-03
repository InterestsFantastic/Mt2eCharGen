#!/usr/bin/python3
'''Careers and career events/mishaps.'''
from utils import setattrs
from mt2erolls import roll_normal
from rpgroller.roller import roll
import inflect
inflection = inflect.engine()

def create_careers(careers, events):
    '''Input: dict of careers without events, events. Output: dict of career objects with events.'''
    for career in careers.values():
        career.events = {}
        for num, event in events[career.event_short].items():
            career.events[num] = event

    assert False, 'incomplete'
    return careers

    for (e, d) in careers.items():
        career = Career()
        events = {}
        for (k,v) in d.items():
            if k in events_labels:
                # Creating events dict with int labels for rolling on.
                event, num  = k.split('_')
                num = int(num)
                event = CareerEvent(v, num)
                event.happen = globals()[event.career_event_short + str(event.num)]
                events[num] = event
            else:
                setattr(career, k, v)
        setattr(career, 'events', events)
        out[e] = career
    return out

class Career:
    def __init__(self, attribs):
        setattrs(self, attribs)
        
    def attempt_entry(self, char):
        '''Sets character.entered and appends to character.log.'''
        # generate DMs
        dm = 0
        if char.terms > 3:
            assert False, 'Can not enter career after 3 terms.'
        elif char.terms == 3:
            dm += self.entry_dm_term3
        elif char.terms == 2:
            dm += self.entry_dm_term2
        # multiplying by a bool (0/1).
        dm += char.check_characteristic('soc 9+') * self.entry_dm_soc9

        result = char.characteristic_roll(self.entry, dm)
        
        logstr = f'Attempted entry into {self.name.title()}: '
        if result:
            logstr += 'Success.'
            char.entered = True
        else:
            logstr += 'Failure.'
            char.entered = False
        char.log.append(logstr)

        if char.entered:
            # run event if successful entry.
            self.events[roll_normal()].run(char)
        return char.entered

    def attempt_graduate(self, char):
        '''Sets character.graduated and appends to character.log.'''
        if not char.can_graduate:
            # Flip back to true for next career
            char.can_graduate = True
            return False

        # generate DMs
        dm = 0
        dm += char.check_characteristic('end 8+') * self.grad_dm_end8
        dm += char.check_characteristic('soc 8+') * self.grad_dm_soc8

        logstr = f'Attempted to graduate from {self.name.title()}: '

        grad_result = char.characteristic_roll(self.grad, extras='modified')
        if grad_result[1] >= 11:
            logstr += 'Graduated with honors.'
            char.graduated = 'honors'
        elif grad_result[0]:
            logstr += 'Success.'
            char.graduated = True
        else:
            logstr += 'Failure.'
            char.graduated = False
        char.log.append(logstr)
        
        return char.graduated


def none_event(char):
    '''Nothing happens as a result of this event being run.'''
    # agent included for conformity.
    return 'No effect.'

def injury(char):
    '''Character is injured.'''
    return char.injure()


class Event:
    def __init__(self, attribs):
        setattrs(self, attribs)
        self.make_happen()
        
    def make_happen(self):
        '''Assigns functions to self.happen (like `edu2()`).'''
        dothese = {'life':[2,3,5,6,7], 'edu':[5,12]}
        if self.career_short not in dothese:
            return
        if self.num not in dothese[self.career_short]:
            return

        event = self.script
        if event[-1] == '.':
            done = True
            event = event[:-1]
        else:
            done = False
        
        if event == 'none':
            self.happen = none_event
        elif event == 'injury':
            self.happen = injury
        elif event[:5] == 'gain ':
            def func(char):
                return char.gain(event[5:])
            self.happen = func
        if not done:
            assert False, 'Incomplete.'
##            print(self.happen())
        
        # Look at script
        # 
##        self.happen = globals()[self.career_short + str(self.num)]
        
    def run(self, char):
        '''Run and log life event.'''
        logstr = f'Event: {self.desc}'
        result = self.happen(char) if hasattr(self, 'happen') else None
        if result is not None:
            logstr += f' {result}'
        char.log.append(logstr)

def edu2(char):
    char.can_test_psi = True

def edu3(char):
    char.can_graduate = False

def edu4(char):
    event_result = char.characteristic_roll('soc 8+', extras='unmodified')
    if event_result[1] == 2:
        char.next_career = 'prison'
        char.can_graduate = False
        char.gain_enemy()
        return 'Gained enemy, can not graduate, and next career is Prison.'
    if event_result[0]:
        char.gain_rival()
        return 'Gained rival.'
    else:
        char.gain_enemy()
        return 'Gained enemy.'

def edu5(char):
    char.gain_skill('carouse +1')

def edu6(char):
    thisroll = roll('1d3')
    for x in range(thisroll):
        char.gain_ally()
    return f'Gained {thisroll} {inflection.plural("ally", thisroll)}.'

def edu7(char):
    # 7: Life Event. Roll on the Life Events table (see page 44).
    assert False, 'incomplete'

def edu8(char):
    event_result = char.characteristic_roll('soc 8+')
    if event_result:
        char.gain_ally()
        char.gain_enemy()
        return 'Gained ally and enemy.'

##You develop a healthy interest in a hobby or other area of study.
##Gain any skill of your choice, with the exception of Jack-of-all-Trades,
##at level 0.
def edu9(char):
    assert False, 'incomplete.' # figure out how to structure program!
    chosen_skill = char.agent.choose_skill('s', 'joat') # e.g. how to find s!
    char.gain_skill(f'chosen_skill +1')
    return f'Chose {chosen_skill}.'

def edu10(char):
    assert False, 'incomplete.'
    chosen_skill = 'bribery'
    newproof = char.characteristic_roll(f'{chosen_skill} 9+')
    if newproof:
        char.gain_skill(f'chosen_skill +1')
        char.gain_rival()
        return 'Gained a level in {chosen_skill}.'

def edu11(char):
    assert False, 'incomplete'
    choosen_path = 'flee'
    if chosen_path == 'flee':
        char.can_graduate = False
        char.next_career = 'drifter'
        return 'Fled the draft to become a drifter.'
    else:
        drafted = char.characteristic_roll('soc 9+')
        if drafted:
            char.can_graduate = False
            service = ['army', 'army', 'army', 'marines', 'marines', 'navy']
            service = choice(service)
            char.next_career = service
            char.drafted = True
            return f'Drafted into {service.title()}.'

def edu12(char):
    char.soc += 1

