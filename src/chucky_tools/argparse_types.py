from argparse import ArgumentTypeError


def property_type(property_string):
    if not property_string.isalpha():
        raise ArgumentTypeError("invalid property string: '{}'".format(property_string))
    return property_string
