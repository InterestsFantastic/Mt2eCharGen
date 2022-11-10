from careers import events
from character import Character
from agent import Console

import pprint
pp = pprint.PrettyPrinter(indent=4)

c = Character()
c.agent = Console(c)
print(c.char_description)

##events['life'][3].run(c)
##events['life'][2].run(c)
##events['life'][5].run(c)
##events['life'][6].run(c)
##events['life'][7].run(c)
##events['life'][9].run(c)
##events['life'][10].run(c)
events['edu'][5].run(c)
##events['edu'][12].run(c)
##events['life'][4].run(c)
##events['life'][11].run(c)
events['life'][8].run(c)
##events['edu'][2].run(c)
events['agent'][10].run(c)

pp.pprint(c.log)
print(c.char_description)
print(f'Benefit dms: {c.benefit_dms}')
print(f'Next qual dm: {c.qual}')
