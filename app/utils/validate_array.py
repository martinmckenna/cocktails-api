def is_array_of_ints(array):
  is_list = type(array) is list

  # ensure this is an array
  # and all values are ints
  return (
      is_list is True
      and all(
          type(eachElement)
          is int for eachElement
          in array
      )
  )
  

def list_contains_none_elements(_list):
    return any(
        eachElement
        is None for eachElement
        in _list
    )
