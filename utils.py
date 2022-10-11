#!/usr/bin/python3
def make_aliases(dictin, key):
    '''Given a dictin with long keys, "key" is the name of a short form field.
    Using that key, it creates an alias dict for output.
    Currently works with dicts of dicts and dicts of arbitarary objects.
    The output is used to index the dictin later through other functions.
    E.g. {'apple':{'fruit':True, 'short':'apl'}, ...} --> {'apl':'apple", ...}'''
    out = {}
    for e in dictin:
        if type(dictin[e]) is dict:
            if dictin[e][key]:
                out[dictin[e][key]] = e
        else:
            # Assuming arbitrary object instead.
            if getattr(dictin[e], key):
                out[getattr(dictin[e], key)] = e
    return out

def get_key_from_aliases(search_term, main, aliases):
    '''Searches a main dict, then an aliases dict, to return the key in the
    main dict corresponding to the search term. Uses title case for the main
    dict and lower case for the alias search.'''
    if search_term.title() in main:
        return search_term.title()
    elif search_term.lower() in aliases:
        return aliases[search_term]
    else:
        assert False, f'Search term not found: {search_term}.'

