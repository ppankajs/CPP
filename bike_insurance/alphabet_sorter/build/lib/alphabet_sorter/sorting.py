# ascending_sort.py

def sort_alphabetically(input_list):
    """
    Sorts a given list of strings in ascending order alphabetically.
    Args:
    - input_list (list): List of strings to be sorted.

    Returns:
    - list: Sorted list of strings.
    """
    if not all(isinstance(item, str) for item in input_list):
        raise ValueError("All elements in the list must be strings")
    
    return sorted(input_list)

