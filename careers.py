'''Careers and career events/mishaps.'''
from utils import setattrs, default_second_elem
from mt2erolls import roll_normal
from rpgroller.roller import roll
from mechanics import char_counters
from ODSReader.odsreader import ODSReader
from ODSReader.utils import keyval_sheet_to_dict, dict_sheet_to_dict_of_dicts, dict_sheet_to_dict_of_objs, dict_sheet_to_list_of_dicts

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

def make_choice(prompt, choices):
    '''Gets a choice fom char's agent and returns it.'''
    def func(char):
        choice = char.agent.choose(prompt, choices)
        # Ensure that the choice is read as done.
        e = DummyEvent(choice + '.')
        return f'Chose {choice}. ' + e.happen(char)
    return func

def none_event(char):
    '''Nothing happens as a result of this event being run.'''
    # agent included for conformity.
    return 'No effect.'

def injury(char):
    '''Character is injured.'''
    return char.injure()

def prison(char):
    '''Character is injured.'''
    char.next_career = 'pris'
    return 'Next career is prison.'

class Event:
    def __init__(self, attribs):
        setattrs(self, attribs)
        if self.can_make_happen():
            self.make_happen()
        
    def can_make_happen(self):
        # For testing, lists what methods are to be built.
        dothese = {'life':[2,3,4,5,6,7,8,9,10,11], 'edu':[5,12]}
        if self.career_short not in dothese:
            return
        if self.num not in dothese[self.career_short]:
            return
        return True
    
    def make_happen(self):
        '''Assigns functions to self.happen.'''
        event = self.script
        # Is event None? Is it complete?
        if event is None:
            custom = True
        elif event[-1] != '.':
            custom = True
        else:
            event = event[:-1]
            custom = False

        if event is not None: 
            if event == 'none':
                self.happen = none_event
            elif event == 'injury':
                self.happen = injury
            elif event == 'prison':
                self.happen = prison
            elif event[:5] == 'gain ' or event.split(' ')[0] in char_counters:
                def func(char):
                    return char.gain(event[5:])
                self.happen = func
            elif event[:8] == 'benefit ':
                def func(char):
                    char.benefit_dms.append(default_second_elem(event.split(' ')))
                    return f'Gained {char.benefit_dms[-1]} to a benefits roll.'
                self.happen = func
            elif event[:8] == 'choose: ':
                self.happen = make_choice(self.desc, event[8:])

        # If there isn't a . at the end of the script, then this means that you
        # need to run some custom code from a named function in this module.
        if custom:
            try:
                self.happen = globals()[self.career_short + str(self.num)]
            except KeyError:
                err = f'No method found for this event, did you mean to have a period at the end of the script? Event: {self.career_short} {self.num}.'
                print(err)
                assert False, err

        
    def run(self, char):
        '''Run and log life event.'''
        logstr = f'Event: {self.desc}'
        result = self.happen(char) if hasattr(self, 'happen') else None
        if result is not None:
            logstr += f' {result}'
        char.log.append(logstr)

class DummyEvent(Event):
    '''This object exists specifically to make the happen method.'''
    def __init__(self, script):
        self.script = script
        self.make_happen()

def life8(char):
    '''Lose one of ally or contact (if available) and gain enemy or rival.'''
    out = ''
    # Losing 1 of ally or contact if available.
    if char.contact and char.ally:
        prompt = 'Choose between losing an ally and losing a contact.'
        choices = 'gain ally -1, gain contact -1'
        out = make_choice(prompt, choices)(char)
    elif char.contact:
        out = char.gain('contact -1')
    elif char.ally:
        out = char.gain('ally -1')

    # Gaining enemy or rival.
    prompt = 'Choose between losing an ally and losing a contact.'
    choices = 'gain rival, gain enemy'
    out += make_choice(prompt, choices)(char)
    return out

mechanics_file = 'mechanics.ods'
mechanics = ODSReader(mechanics_file, clonespannedcolumns=True)

events_funcs = [str, int]
events_keys = ['career_short', 'num']
##events = dict_sheet_to_dict_of_dicts(mechanics, 'Events', events_keys, events_funcs)
events = dict_sheet_to_dict_of_objs(mechanics, 'Events', Event, events_keys, events_funcs)
##pp.pprint(events)
##pp.pprint(events['life'])
##print(dir(events['life'][2]))
##pp.pprint(events['life'][2].career_short)
##print(events['life'][2].script)
##pp.pprint(events['life'][3].desc)
##pp.pprint(events['life'][3].happen)
##input('End of test.')

