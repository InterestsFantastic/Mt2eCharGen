from mt2emechanics import events, skills, skills_aliases
from agent import Console
from character import Character

console = Console()
c = Character()
print(f'Character created with characteristics: {c.characteristics_string}')

##print(events['life'][2].script)
events['life'][3].run(c, console)
print(c.log)

##print(events['life'][2].happen)

