def match_samples(dict_one, dict_two, sample_list):
    '''Generates a pairing between the two given dicts for each value in the given list'''
    assert isinstance(dict_one, dict) and dict_one
    assert isinstance(dict_two, dict) and dict_two
    assert isinstance(sample_list, list) and sample_list
    assert all(type(sample_list[0]) == type(key) for key in dict_one.keys())
    assert all(type(sample_list[0]) == type(key) for key in dict_two.keys())
    
    d = {s:(dict_one[s], dict_two[s]) for s in sample_list if s in dict_one and s in dict_two}
    return d

def match_error(source_dict, other_dict, sample_list):
    ''''''
    matched = match_samples(source_dict, other_dict, sample_list)
    d = {k:((v[1]-v[0])/v[0]) for k, v in matched.items()}
    return d
    