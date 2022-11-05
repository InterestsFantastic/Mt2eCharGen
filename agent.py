#!/usr/bin/python3
from mechanics import skills, skills_aliases
from utils import get_key_from_aliases

class Console:
    def choose_skill(self, prompt, exclude=None, include=None):
        query = 'Choose a skill: '
        out = input(f'{prompt} {query}')
        return get_key_from_aliases(out, skills, skills_aliases)

from character import Character
from mechanics import careers
c = Character()
c.agent = Console()
##print(careers['University'].events[9].run(c))
