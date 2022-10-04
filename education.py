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
                events[num] = LifeEvent(event, num)
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

        assert False, 'Need to figure out how to catch graduating with honors.'
        # characteristic_target vs. characteristic_roll?
        # change characteristic i.e. int +1 in character?
        logstr = f'Attempted to graduate from {self.name.title()}: '
        if thisroll >= 11:
            logstr += 'Graduated with honors.'
            char.graduated = 'honors'
        elif thisroll >= target:
            logstr += 'Success.'
            char.graduated = True
        else:
            logstr += 'Failure.'
            char.graduated = False
        char.log.append(logstr)
        
        return char.graduated


class LifeEvent:
    def __init__(self, desc, num):
        self.num = num
        self.desc = desc
    def run(self, char):
        logstr = f'Life Event: {self.desc}'
        result = self.happen()
        if result is not None:
            logstr += f' {result}'
        char.log.append(logstr)

def can_not_graduate(char):
    char.can_graduate = False
    
def can_test_psi(char):
    char.can_test_psi = True
    
def edu2(self, char):
    can_test_psi(char)

def edu3(self, char):
    can_not_graduate(char)

def edu6(self, char):
    thisroll = roll('1d3')
    for x in range(thisroll):
        char.gain_ally()
    return f'Gained {thisroll} allies.'

def edu4(self, char):
    # I need to set up the character attribute vs. target roll here.
    # Rename it or whatever I'm going to do, before proceeding.
    thisroll = roll_normal()
    if thisroll == 2:
        # The player can not achieve 8+ with a roll of 2.
        char.next_career = 'prison'
        can_not_graduate(char)
        char.gain_enemy()
        return 'Gained enemy, can not graduate, and next career is Prison.'
    assert False, 'incomplete.'
    # I'm doing the same check as if I were doing the graduating with honors thing.
##    if char.cond('soc 8+'):
##        char.gain_rival()
##        return 'Gained rival.'
##    else:
##        char.gain_enemy()
##        return 'Gained enemy.'

# 5 Taking advantage of youth, you party as much as you study. Gain Carouse 1.

# 7: Life Event. Roll on the Life Events table (see page 44).

# 8: You join a political movement. Roll SOC 8+. If successful, you become a
# leading figure. Gain one Ally within the movement but gain one Enemy in
# wider society.

# 9: You develop a healthy interest in a hobby or other area of study.
# Gain any skill of your choice, with the exception of Jack-of-all-Trades,
# at level 0.

## 10: A newly arrived tutor rubs you up the wrong way and you work hard to
##overturn their conclusions. Roll 9+ on any skill you have learned
##during this term. If successful, you provide a truly elegant proof
##that soon becomes accepted as the standard approach. Gain a level
##in the skill you rolled on and the tutor as a Rival.

## 11. War comes and a wide-ranging draft is instigated. You can either flee and
##join the Drifter career next term or be drafted
##(roll 1D: 1-3 Army, 4-5 Marine, 6 Navy). Either way, you do not graduate
##this term. However, if you roll SOC 9+, you can get enough strings pulled
##to avoid the draft and complete your education – you may attempt graduation
##normally and are not drafted.

## 12. You gain wide-ranging recognition of your initiative and innovative
##approach to study. Increase your SOC by +1.
