def match_samples(dict_one, dict_two, sample_list):
    '''Generates a pairing between the two given dicts for each
    value in the given list
    :param dict_one: 1st dictionary to find words in
    :type: dict
    :param dict_two: 2nd dictionary to find words in
    :type: dict
    :sample_list: words to compare
    :type: dict
    :returns: dict
    '''
    assert isinstance(dict_one, dict) and dict_one
    assert isinstance(dict_two, dict) and dict_two
    assert isinstance(sample_list, list) and sample_list
    assert all(type(sample_list[0]) == type(key) for key in dict_one.keys())
    assert all(type(sample_list[0]) == type(key) for key in dict_two.keys())
    d = {s:(dict_one[s], dict_two[s]) for s in sample_list if s in dict_one and s in dict_two}
    return d

def match_error(source_dict, other_dict, sample_list):
    '''
    Creates dictionary with match_samples and takes the relative frequency
    (v2-v1)/v1 instead of just comparing the two directly
    :param source_dict: 1st dictionary to find words in
    :type: dict
    :param other_dict: 2nd dictionary to find words in
    :type: dict
    :param sample_list: words to compare
    :type: list
    :returns: dict
    '''
    matched = match_samples(source_dict, other_dict, sample_list)
    d = {k:((v[1]-v[0])/v[0]) for k, v in matched.items()}
    return d
