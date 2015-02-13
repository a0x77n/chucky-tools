def field_select(fields, indices):
    """
    Returns selected fields from list of fields.
    :param fields: the list containing all fields
    :param indices: the indices of fields to be selected
    :return: a tuple containing all selected fields
    """
    return tuple([fields[i] for i in indices])


def field_select_complement(fields, indices):
    """
    Returns selected fields from list of fields.
    :param fields: the list containing all fields
    :param indices: the indices of fields to be discarded
    :return: a tuple containing all non discarded fields
    """
    complement_indices = [i for i in range(len(fields)) if i not in indices]
    return field_select(fields, complement_indices)


def attribute_escape(attriute_string):
    """
    Strips all non alpha numeric characters from string
    :param attriute_string: the raw string
    :return: the escaped string
    """
    return filter(str.isalnum, attriute_string)