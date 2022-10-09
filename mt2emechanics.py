#!/usr/bin/python3
from ODSReader.odsreader import ODSReader
from ODSReader.utils import keyval, rows_to_list_of_dicts
from education import create_educations

mechanics_file = 'mt2emechanics.ods'
mechanics = ODSReader(mechanics_file, clonespannedcolumns=True)

characteristic_modifiers = mechanics.getSheet('CharacteristicModifiers')
characteristic_modifiers = keyval(characteristic_modifiers, int)
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
noble_titles = keyval(noble_titles, int, str)
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
print(skills)

skills_aliases = {}
skills_list = []
for skill in skills:
    if 'short' in skills[skill]:
        skills_aliases[skills[skill].short] = skill
    skills_list.append(skills[skill].skill)

print(skills_list)
print(skills_aliases)
