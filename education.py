from mt2erolls import roll_normal

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
                events[int(k.split('_')[1])] = LifeEvent(v)
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
            return False
        elif char.terms == 3:
            dm += self.entry_dm_term3
        elif char.terms == 2:
            dm += self.entry_dm_term2
        if char.soc >= 9:
            dm += self.entry_dm_soc9

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
        # generate DMs
        dm = 0
        if char.end >= 8:
            dm += grad_dm_end8
        if char.soc >= 8:
            dm += grad_dm_soc8


        assert False, 'Need to figure out how to catch graduating with honors.'
        # characteristic_target vs. characteristic_roll?
        # change characteristic i.e. int +1 in character?
        logstr = f'Attempted to graduate from {self.name.title()}: '
        if roll >= 11:
            logstr += 'Graduated with honors.'
            char.graduated = 'honors'
        elif roll >= target:
            logstr += 'Success.'
            char.graduated = True
        else:
            logstr += 'Failure.'
            char.graduated = False
        char.log.append(logstr)
        
        return char.graduated

class LifeEvent:
    def __init__(self, desc):
        self.desc = desc
    def run(self, char):
        char.log.append(f'Life Event: {self.desc}')
