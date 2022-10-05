from mt2erolls import roll_normal
from rpgroller.roller import roll

events_labels = 'event_2 event_3 event_4 event_5 event_6 event_7 event_8 event_9 event_10 event_11 event_12'
events_labels = events_labels.split()

def create_educations(educations):
    '''Input: spreadsheet, output: list of Education objects.'''
    out = []
    for e in educations:
        education = Education()
        events = {}
        for (k,v) in e.items():
            if k in events_labels:
                # Creating events dict with int labels for rolling on.
                event, num  = k.split('_')
                num = int(num)
                event = CareerEvent(v, num)
                event.happen = globals()[event.career_event_short + str(event.num)]
                events[num] = event
            else:
                setattr(education, k, v)
        setattr(education, 'events', events)
        out.append(education)
    return out

class Education:
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


class CareerEvent:
    def __init__(self, desc, num, career_event_short='edu'):
        self.num = num
        self.desc = desc
        self.career_event_short = career_event_short
        
    def run(self, char):
        '''Run and log life event.'''
        logstr = f'Life Event: {self.desc}'
        result = self.happen(char)
        if result is not None:
            logstr += f' {result}'
        char.log.append(logstr)

def can_not_graduate(char):
    char.can_graduate = False
    
def can_test_psi(char):
    char.can_test_psi = True
    
def edu2(char):
    can_test_psi(char)

def edu3(char):
    can_not_graduate(char)

def edu6(char):
    thisroll = roll('1d3')
    for x in range(thisroll):
        char.gain_ally()
    return f'Gained {thisroll} allies.'

def edu4(char):
    event_result = char.characteristic_roll('soc 8+', extras='unmodified')
    if event_result[1] == 2:
        char.next_career = 'prison'
        can_not_graduate(char)
        char.gain_enemy()
        return 'Gained enemy, can not graduate, and next career is Prison.'
    if event_result[0]:
        char.gain_rival()
        return 'Gained rival.'
    else:
        char.gain_enemy()
        return 'Gained enemy.'

def edu5(char):
    char.gain_trait('Carouse +1')

def edu12(char):
    char.gain_trait('soc +1')

def edu8(char):
    event_result = char.characteristic_roll('soc 8+')
    if event_result:
        char.gain_ally()
        char.gain_enemy()
        return 'Gained ally and enemy.'

def edu11(char):
    assert False, 'incomplete'
    choosen_path = 'flee'
    if chosen_path == 'flee':
        can_not_graduate(char)
        char.next_career = 'drifter'
        return 'Fled the draft to become a drifter.'
    else:
        drafted = char.characteristic_roll('soc 9+')
        if drafted:
            can_not_graduate(char)
            service = ['army', 'army', 'army', 'marines', 'marines', 'navy']
            service = choice(service)
            char.next_career = service
            char.drafted = True
            return f'Drafted into {service.title()}.'

def edu7(char):
    # 7: Life Event. Roll on the Life Events table (see page 44).
    assert False, 'incomplete'

def edu9(char):
    assert False, 'incomplete.'
    chosen_skill = 'bribery'
    assert chosen_skill != 'jot', 'Not allowed to choose JoT.'
    char.gain_trait(f'chosen_skill +1')
    return f'Chose {chosen_skill}.'

def edu10(char):
    assert False, 'incomplete.'
    chosen_skill = 'bribery'
    newproof = char.characteristic_roll(f'{chosen_skill} 9+')
    if newproof:
        char.gain_trait(f'chosen_skill +1')
        char.gain_rival()
        return 'Gained a level in {chosen_skill}.'
