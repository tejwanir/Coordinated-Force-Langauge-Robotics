def get_selected_items(target, selection):
    """
    Retrieves items from the target based on the selection.

    Args:
        target: The data structure to retrieve items from (e.g., list, tuple, numpy array, or dictionary).
        selection: The indices or keys specifying the items to retrieve. Can be:
        - A single integer or string.
        - A tuple or list of indices/keys.
        - A nested tuple or list for hierarchical selection.

    Returns:
        The selected items:
        - A single item if the selection is a single integer or string.
        - A tuple of items if the selection is a list or tuple.
        - A tuple of tuples for nested selections.

    Raises:
        ValueError: If the selection is of an invalid type.

    Examples:
        - get_selected_items(['a', 'b', 'c'], 0) -> 'a'
        - get_selected_items(['a', 'b', 'c'], (0, 2)) -> ('a', 'c')
        - get_selected_items({'x': 'a', 'y': 'b'}, ('x', 'y')) -> ('a', 'b')
    """
    if isinstance(selection, (list, tuple)):
        selected_items = ()
        for subselection in selection:
            if isinstance(subselection, (list, tuple)):
                subselected_items = ()
                for single_item in subselection:
                    subselected_items += (target[single_item],)
                selected_items += (subselected_items,)
            else:
                selected_items += (target[subselection],)
        return selected_items
    elif isinstance(selection, (int, str)):
        return target[selection]
    else:
        raise ValueError(f'Invalid selection: {selection}')

def set_selected_items(target, selection, values):
    """
    Sets values in the target based on the selection.

    Args:
        target: The data structure to modify (e.g., list, tuple, numpy array, or dictionary).
        selection: The indices or keys specifying where to set values. Can be:
        - A single integer or string.
        - A tuple or list of indices/keys.
        - A nested tuple or list for hierarchical selection.
        values: The new values to set. Must match the structure of the selection.
        - A single value for single selections.
        - A tuple or list of values for list/tuple selections.
        - A nested tuple or list of values for nested selections.

    Raises:
        ValueError: If the selection is of an invalid type.

    Examples:
        set_selected_items(['a', 'b', 'c'], 0, 'x') modifies the list to ['x', 'b', 'c']
        set_selected_items({'x': 'a', 'y': 'b'}, ('x',), ('z',)) modifies the dict to {'x': 'z', 'y': 'b'}
    """
    if isinstance(selection, (list, tuple)):
        for i, subselection in enumerate(selection):
            if isinstance(subselection, (list, tuple)):
                for j, single_item in enumerate(subselection):
                    target[single_item] = values[i][j]
            else:
                target[subselection] = values[i]
    elif isinstance(selection, (int, str)):
        target[selection] = values
    else:
        raise ValueError(f'Invalid selection: {selection}')

if __name__ == '__main__':
    
    import numpy as np

    a = np.array(['a', 'b', 'c', 'd', 'e',])

    set_selected_items(a, 0, 'A')

    print(get_selected_items(a, 0)) # -> 'A'

    set_selected_items(a, (0,2), ('a','C'))

    print(get_selected_items(a, (0,))) # -> ('a',)

    print(get_selected_items(a, (0,2))) # -> ('a', 'C')

    set_selected_items(a, ((2,),), (('c',),))

    print(get_selected_items(a, ((0,),))) # -> (('a',),)

    print(get_selected_items(a, ((0,2),(1,3)))) # -> (('a','c'),('b','d'))

    print(get_selected_items(a, ((0,),2,4,(1,3)))) # -> (('a',),'c','e',('b','d'))

    b = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e',}

    print(get_selected_items(b, 0)) # -> 'a'

    print(get_selected_items(b, (0,))) # -> ('a',)

    print(get_selected_items(b, (0,2))) # -> ('a', 'c')

    print(get_selected_items(b, ((0,),))) # -> (('a',),)

    print(get_selected_items(b, ((0,2),(1,3)))) # -> (('a','c'),('b','d'))

    print(get_selected_items(b, ((0,),2,4,(1,3)))) # -> (('a',),'c','e',('b','d'))

