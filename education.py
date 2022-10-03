def create_educations(educations):
    '''Input: spreadsheet, output: list of Education objects.'''
    out = []
    for e in educations:
        education = Education()
        for (k,v) in e.items():
            setattr(education, k, v)
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
