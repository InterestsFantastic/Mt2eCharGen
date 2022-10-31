from mt2emechanics import events#, skills, skills_aliases
from agent import Console
from character import Character

import pprint
pp = pprint.PrettyPrinter(indent=4)

console = Console()
c = Character()
print(f'Character created with characteristics: {c.upp}\n\n')

##print(events['life'][2].script)
events['life'][3].run(c, console)

for x in range(25):
    events['life'][2].run(c, console)
    print(c.characteristics_string)
    
pp.pprint(c.log)
print('\n\n\n')

