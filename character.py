from roller import roll
from mt2e_mechanics import roll_normal, roll_boon, roll_bane
from copy import copy

class Character:
    def __init__(self, gen_method='normal'):
        self.gen(gen_method)

    def gen(self, gen_method):
        # Pick appropriate rolling function to call.
        if gen_method == 'normal':
            attribute_diceroll = roll_normal
        if gen_method == 'boon':
            attribute_diceroll = roll_boon
        if gen_method == 'bane':
            attribute_diceroll = roll_bane

        attrib_rolls = []
        for x in range(6):
            attrib_rolls.append(attribute_diceroll())
        self.str, self.dex, self.end, self.int, self.edu, self.soc = copy(attrib_rolls)

    def print_attribs(self):
        print(self.str, self.dex, self.end, self.int, self.edu, self.soc)

if __name__ == '__main__':
    c = Character()
    c.print_attribs()
