from roller import roll
from copy import copy

class Character:
    def __init__(self, gen_method='normal'):
        self.gen(gen_method)

    def gen(self, gen_method):
        if gen_method == 'normal':
            attribute_diceroll = '2d6'
        if gen_method == 'boon':
            attribute_diceroll = '3d6kh2'

        attrib_rolls = []
        for x in range(6):
            attrib_rolls.append(roll(attribute_diceroll))
        self.str, self.dex, self.end, self.int, self.edu, self.soc = copy(attrib_rolls)

    def print_attribs(self):
        print(self.str, self.dex, self.end, self.int, self.edu, self.soc)

if __name__ == '__main__':
    c = Character()
    c.print_attribs()
