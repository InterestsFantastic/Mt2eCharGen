#!/usr/bin/python3
from mechanics import skills, skills_aliases
from utils import get_key_from_aliases

class Console:
    def __init__(self, char=None):
        self.char = char
        
    def choose(self, prompt, choices):
        '''Creates a list given through the choose script:
        e.g. 'choose: gain mil 1, gain investigate 1, gain soc +2.
        It receives the prompt typically from Event.desc and
        generates the choices by splitting on ', ' after 'choose: '.'''
        print('\n' + prompt + '\n')
        choices = choices.split(', ')
        input_prompt = 'Choose'
        input_prompt += ' (c to print character):\n' if self.char is not None else ':\n'

        for i,c in enumerate(choices):
            input_prompt += f'{i}: {c}\n'
        input_prompt += 'Your Choice: '
        answer = ''
        while answer not in range(len(choices)):
            answer = input(input_prompt)
            try:
                answer = int(answer)
            except:
                if answer == 'c':
                    print('\n' + self.char.char_description + '\n')
                answer = None
        return choices[answer]
