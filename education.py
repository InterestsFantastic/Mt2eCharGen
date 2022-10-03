def create_educations(educations):
    out = []
    for e in educations:
        education = Education()
        for (k,v) in e.items():
            setattr(education, k, v)
        out.append(education)
    return out

class Education:
    def attempt_entry(self, char):
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
        else:
            logstr += 'Failure.'

        char.log.append(logstr)
        return result

    def attempt_grad(self, char):
        # generate DMs
        dm = 0
        if char.end >= 8:
            dm += grad_dm_end8
        if char.soc >= 8:
            dm += grad_dm_soc8

        assert False, 'Need to figure out how to catch graduating with honors.'
        # characteristic_target vs. characteristic_roll?
        # change characteristic i.e. int +1 in character?
        return char.characteristic_roll(self.grad, dm)
