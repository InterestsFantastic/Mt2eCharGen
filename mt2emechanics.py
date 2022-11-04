#!/usr/bin/python3
from ODSReader.odsreader import ODSReader
from ODSReader.utils import keyval_sheet_to_dict, dict_sheet_to_dict_of_dicts, dict_sheet_to_dict_of_objs, dict_sheet_to_list_of_dicts
from careers import Career, Event, create_careers
from utils import make_aliases
from random import choice

import pprint
pp = pprint.PrettyPrinter(indent=4)

non_proficiency_penalty = -3

characteristics = 'str dex end int edu soc'.split()
phys_characteristics = 'str dex end'.split()
def randphys():
    '''Returns random physical characteristic.'''
    return choice(phys_characteristics)

mechanics_file = 'mt2emechanics.ods'
mechanics = ODSReader(mechanics_file, clonespannedcolumns=True)

characteristic_modifiers = keyval_sheet_to_dict(mechanics, 'CharacteristicModifiers', [int])
noble_titles = keyval_sheet_to_dict(mechanics, 'NobleTitles', [int, str])
##print(noble_titles)
##input()

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

##pp.pprint(skills)
##pp.pprint(skills_aliases)
##pp.pprint(skills_cascades)
##input()

events_funcs = [str, int]
events_keys = ['career_short', 'num']
##events = dict_sheet_to_dict_of_dicts(mechanics, 'Events', events_keys, events_funcs)
events = dict_sheet_to_dict_of_objs(mechanics, 'Events', Event, events_keys, events_funcs)
##pp.pprint(events)
##pp.pprint(events['life'])
##print(dir(events['life'][2]))
##pp.pprint(events['life'][2].career_short)
##print(events['life'][2].script)
##pp.pprint(events['life'][3].desc)
##pp.pprint(events['life'][3].happen)
##input('End of test.')

careers_funcs = [str, str, str, str, int, int, int, str, int, int, int]
careers = dict_sheet_to_dict_of_objs(mechanics, 'Careers', Career, ['name'], careers_funcs)
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
