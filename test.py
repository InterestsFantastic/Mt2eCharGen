from mt2emechanics import events#, skills, skills_aliases
from character import Character, parse_gain_skill

import pprint
pp = pprint.PrettyPrinter(indent=4)

c = Character()
print(c.char_description)

print(parse_gain_skill('carouse 0'))
print(parse_gain_skill('carouse 1'))
print(parse_gain_skill('carouse +1'))
print(parse_gain_skill('Animals (Handling) +1'))
print(parse_gain_skill('Animals (handling) +1'))
##print(parse_gain_skill('carouse -1')) # Works




##print(c.skills)

##events['life'][3].run(c)
##
####for x in range(25):
####    events['life'][2].run(c)
####    print(c.characteristics_string)
####pp.pprint(c.log)
####print('\n\n\n')
####input()
##
##events['life'][2].run(c)
##events['life'][3].run(c)
##events['life'][5].run(c)
##events['life'][6].run(c)
##events['life'][7].run(c)
##events['edu'][5].run(c)
##events['edu'][12].run(c)
##pp.pprint(c.log)
##print(c.char_description)
