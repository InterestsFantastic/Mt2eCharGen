#!/usr/bin/python3
from mt2emechanics import skills, skills_aliases
from utils import get_key_from_aliases

class Console:
    def choose_skill(prompt, exclude=None, include=None):
        query = 'Choose a skill: '
        out = input(f'{prompt} {query}')
        return get_key_from_aliases(out, skills, skills_aliases)

from character import Character
from mt2emechanics import educations
c = Character()
c.agent = Console()
print(educations['University'].events[9].run(c))