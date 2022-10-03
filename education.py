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

        return char.characteristic_roll(self.entry, dm)
