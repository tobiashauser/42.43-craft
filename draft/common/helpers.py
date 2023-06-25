from typing import Any, Dict


def combine_dictionaries(
    dict1: Dict[Any, Any], dict2: Dict[Any, Any]
) -> Dict[Any, Any]:
    result = dict1
    for key, value in dict2.items():
        if key not in dict1:
            result[key] = value
        else:
            # if both are lists, combine the lists
            if isinstance(value, list) and isinstance(dict1[key], list):
                result[key] = dict1[key] + value
            # if both are dictionaries, combine them
            elif isinstance(value, dict) and isinstance(dict1[key], dict):
                result[key] = combine_dictionaries(dict1[key], value)
    return result
