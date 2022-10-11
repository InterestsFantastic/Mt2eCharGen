#!/usr/bin/python3
from ODSReader.odsreader import ODSReader
from ODSReader.utils import keyval_sheet_to_dict, dict_sheet_to_dict_of_dicts
from education import create_educations

non_proficiency_penalty = -3

mechanics_file = 'mt2emechanics.ods'
mechanics = ODSReader(mechanics_file, clonespannedcolumns=True)

characteristic_modifiers = keyval_sheet_to_dict(mechanics, 'CharacteristicModifiers', int)
noble_titles = keyval_sheet_to_dict(mechanics, 'NobleTitles', int, str)
skills = dict_sheet_to_dict_of_dicts(mechanics, 'Skills', 'skill')

educations_funcs = [str, str, str, int, int, int, str, int, int, int]
educations = dict_sheet_to_dict_of_dicts(mechanics, 'Educations', 'name', *educations_funcs)
educations = create_educations(educations)

def make_aliases(dictin, key):
    '''If you have a dict with long keys, this makes a dict of
    references to those keys using shorter keys, this will provide the
    second dict.'''
    out = {}
    for e in dictin:
        if dictin[e][key]:
            out[dictin[e][key]] = e
    return out

skills_aliases = make_aliases(skills, 'short')

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

def get_skill_name(skill):
    '''Returns the full form of a skill name from its alias (or skill name).'''
    if skill in skills:
        return skill
    elif skill in skills_aliases:
        return skills_aliases[skill]
    else:
        assert False, f'Skill not found: {skill}.'

print(educations)
print(skills['Science (Philosophy)'])
print(skills_aliases)
