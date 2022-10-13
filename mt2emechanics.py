#!/usr/bin/python3
from ODSReader.odsreader import ODSReader
from ODSReader.utils import keyval_sheet_to_dict, dict_sheet_to_dict_of_dicts, dict_sheet_to_dict_of_objs
from careers import Career, create_careers #, create_events
from utils import make_aliases

characteristics = 'str dex end int edu soc'.split()
non_proficiency_penalty = -3

mechanics_file = 'mt2emechanics.ods'
mechanics = ODSReader(mechanics_file, clonespannedcolumns=True)

characteristic_modifiers = keyval_sheet_to_dict(mechanics, 'CharacteristicModifiers', int)
noble_titles = keyval_sheet_to_dict(mechanics, 'NobleTitles', int, str)

skills = dict_sheet_to_dict_of_dicts(mechanics, 'Skills', 'skill')
skills_aliases = make_aliases(skills, 'short')

assert False, 'How should I ignore key in creating events?'
events_funcs = [str, int]
events = dict_sheet_to_dict_of_dicts(mechanics, 'Events', 'name', *events_funcs)
events = create_events(events)

careers_funcs = [str, str, str, str, int, int, int, str, int, int, int]
careers = dict_sheet_to_dict_of_objs(mechanics, 'Careers', 'name', Career, *careers_funcs)

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


print(skills['Science (Philosophy)'])
print(careers['University'].events[2].desc)

from utils import get_key_from_aliases
print(get_key_from_aliases('uni', careers, careers_aliases))
