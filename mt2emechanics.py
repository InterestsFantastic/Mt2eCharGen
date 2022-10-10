#!/usr/bin/python3
from ODSReader.odsreader import ODSReader
from ODSReader.utils import keyval_sheet_to_dict, rows_to_list_of_dicts, dict_of_dicts_from_list_of_dicts, dict_sheet_to_dict_of_dicts
from education import create_educations

non_proficiency_penalty = -3

mechanics_file = 'mt2emechanics.ods'
mechanics = ODSReader(mechanics_file, clonespannedcolumns=True)

characteristic_modifiers = keyval_sheet_to_dict(mechanics, 'CharacteristicModifiers', int)
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

noble_titles = keyval_sheet_to_dict(mechanics, 'NobleTitles', int, str)
def noble_title(num):
    '''Returns the noble title of a social status.'''
    if num in noble_titles:
        return noble_titles[num]
    else:
        return None

##education_sheet = mechanics.getSheet('PrecareerEducation')
educations_funcs = [str, str, str, int, int, int, str, int, int, int]
educations = dict_sheet_to_dict_of_dicts(mechanics, 'Educations', 'name', *educations_funcs)
print(educations)
educations = create_educations(educations)
##educations = rows_to_list_of_dicts(education_sheet, *educations_funcs)
##educations = create_educations(educations)

skills = dict_sheet_to_dict_of_dicts(mechanics, 'Skills', 'skill')
skills_aliases = {}
for skill in skills:
    if skills[skill]['short'] is not None:
        skills_aliases[skills[skill]['short']] = skill

def get_skill_name(skill):
    '''Returns the full form of a skill name from its alias (or skill name).'''
    if skill in skills:
        return skill
    elif skill in skills_aliases:
        return skills_aliases[skill]
    else:
        assert False, f'Skill not found: {skill}.'

print(educations[0])
print(educations['University'])
print(skills['Science (Philosophy)'])
