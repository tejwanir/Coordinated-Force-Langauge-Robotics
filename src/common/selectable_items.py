from typing import Sequence

def get_selected_items(target, selection):
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

