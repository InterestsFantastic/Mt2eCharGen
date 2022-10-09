#!/usr/bin/python3
from ODSReader.odsreader import ODSReader
from ODSReader.utils import dict_sheet_to_dict, rows_to_list_of_dicts
from education import create_educations

mechanics_file = 'mt2emechanics.ods'
mechanics = ODSReader(mechanics_file, clonespannedcolumns=True)

characteristic_modifiers = mechanics.getSheet('CharacteristicModifiers')
characteristic_modifiers = dict_sheet_to_dict(characteristic_modifiers, int)
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

noble_titles = mechanics.getSheet('NobleTitles')
noble_titles = dict_sheet_to_dict(noble_titles, int, str)
def noble_title(num):
    '''Returns the noble title of a social status.'''
    if num in noble_titles:
        return noble_titles[num]
    else:
        return None

education_sheet = mechanics.getSheet('PrecareerEducation')
educations_funcs = [str, str, int, int, int, str, int, int, int]
educations = rows_to_list_of_dicts(education_sheet, *educations_funcs)
educations = create_educations(educations)

skills_sheet = mechanics.getSheet('Skills')
skills = rows_to_list_of_dicts(skills_sheet)

skills_aliases = {}
skills_list = []
for skill in skills:
    if skill['short'] is not None:
        skills_aliases[skill['short']] = skill["skill"]
    skills_list.append(skill['skill'])

def get_skill_name(skill):
    '''Returns the full form of a skill name from its alias (or skill name).'''
    if skill in skills_list:
        return skill
    elif skill in skills_aliases:
        return skills_aliases[skill]
    else:
        assert False, f'Skill not found: {skill}.'
