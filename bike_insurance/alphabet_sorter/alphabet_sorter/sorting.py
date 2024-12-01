# alphabet_sorter/sorting.py

def sort_alphabetically(data):
    """Sort a list of strings in ascending alphabetical order."""
    if not isinstance(data, list):
        raise TypeError("Input must be a list.")
    
    return sorted(data)
