#!/usr/bin/python3
from ODSReader.odsreader import ODSReader
from ODSReader.utils import keyval_sheet_to_dict, dict_sheet_to_dict_of_dicts, dict_sheet_to_dict_of_objs, dict_sheet_to_list_of_dicts
from utils import make_aliases
from random import choice

import pprint
pp = pprint.PrettyPrinter(indent=4)

mechanics_file = 'mechanics.ods'
mechanics = ODSReader(mechanics_file, clonespannedcolumns=True)

non_proficiency_penalty = -3

people = 'ally enemy patron rival contact'.split()
char_zeros = 'qual'.split()
characteristics = 'str dex end int edu soc'.split()
phys_characteristics = 'str dex end'.split()
char_counters = people + characteristics + char_zeros

def randphys():
    '''Returns random physical characteristic.'''
    return choice(phys_characteristics)

characteristic_modifiers = keyval_sheet_to_dict(mechanics, 'CharacteristicModifiers', [int])
noble_titles = keyval_sheet_to_dict(mechanics, 'NobleTitles', [int, str])

skills = dict_sheet_to_dict_of_dicts(mechanics, 'Skills', ['skill'])
skills_aliases = make_aliases(skills, 'short')
# Sometimes there are 2+ aliases for a skill.
skills_aliases.update(keyval_sheet_to_dict(mechanics, 'OtherSkillAliases'))
skills_cascades = {}
for s in skills:
    cf = skills[s]['cascade_from']
    if cf:
        if cf in skills_cascades:
            skills_cascades[cf].append(s)
        else:
            skills_cascades[cf] = [s]

def findskill(skill):
    '''Returns the skill key used in dicts, referred to by a string skill,
    searching aliases as well as the base dict of skills. Accepts lower case
    skills by searching via title case.'''
    if skill.title() in skills:
        return skill.title()
    elif skill in skills_aliases:
        return skills_aliases[skill]
    else:
        return None

##pp.pprint(noble_titles)
##pp.pprint(skills)
##pp.pprint(skills_aliases)
##pp.pprint(skills_cascades)
##print(findskill('carouse'))
##print(findskill('riding'))
##input()


##careers_funcs = [str, str, str, str, int, int, int, str, int, int, int]
##careers = dict_sheet_to_dict_of_objs(mechanics, 'Careers', Career, ['name'], careers_funcs)
##careers = create_careers(careers, events)

def characteristic_modifier(num):
    '''Returns the diceroll modifier for having a particular value
    in a characteristic'''
    if num in characteristic_modifiers:
        return characteristic_modifiers[num]
    elif num > 14:
        return 3
    else:
        # negative numbers.
        assert False, f'Improper characteristic modifier requested: {num}'

def noble_title(num):
    '''Returns the noble title of a social status.'''
    if num in noble_titles:
        return noble_titles[num]
    else:
        return None

##print(skills['Science (Philosophy)'])
##print(careers['University'].events[2].desc)
##
##from utils import get_key_from_aliases
##print(get_key_from_aliases('uni', careers, careers_aliases))
