def convert_to_array_of_ints(string_to_convert):
    string_as_array = string_to_convert.split(',')
    return [int(i) for i in string_as_array]
