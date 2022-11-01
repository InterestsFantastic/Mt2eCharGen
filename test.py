from mt2emechanics import events#, skills, skills_aliases
from character import Character

import pprint
pp = pprint.PrettyPrinter(indent=4)

c = Character()
print(f'Character created with characteristics: {c.upp}\n\n')
events['life'][3].run(c)
input(c.log)

##for x in range(25):
##    events['life'][2].run(c)
##    print(c.characteristics_string)
##pp.pprint(c.log)
##print('\n\n\n')
##input()

events['life'][5].run(c)
events['life'][6].run(c)
events['life'][7].run(c)
events['edu'][5].run(c)
pp.pprint(c.log)
