assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']]
# diagonal units were introduced to solve the diagonal sudoku constraint
unitlist = row_units + column_units + square_units + diagonal_units
# diagonal units were include in the overall unitlist
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
# units and peers dictionaries also reflected the revised mapping including the diagonal units

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def get_key_value_dict (box_list, values):
    """
    This function is to get the key value pairs from the values dictionary for a set of keys as inputs
    """
    # return a dictionary of keys and values for the matching keys
    return (dict((item, values[item]) for item in box_list))

def find_naked_twins (box_list, values):
    """
    This function is to find the naked twins from a set of boxes passed as input. 
    The idea here is to have a unit passed as input and matching naked twin's box value being returned as a string.
    """    
    sudo_data = get_key_value_dict (box_list, values)
    return_str = ''
    result = {}
    # in the loop below, a result set is created for unique box values from the input unit 
    for key,value in sudo_data.items():
        if value not in result.values():
            result[key] = value
    # set C has the values for the repeating values ( a.k.a naked twin value
    C = [v for k,v in sudo_data.items() if k not in result]
    for a in C:
        return_str = a
    # return the naked twin value as a string
    return return_str

def find_replace_matching_twin_value (box_list, values, matched_value): 
    """
    This function is to find and replace the box values in the unit that match to the naked twins.
    The idea here is to split the matched value into digits. 
    For each digit find the matching box value and store the box key into remove_matching_values_items set.
    For each item in the remove_matching_values_items ignore the following for replacement - 
            the naked twin box
            matched_value size other then 2 
            boxes with single digits
        For the remaining ones, replace them with ''
    """     
    remove_matching_values_items = []
    set_matched_values_digits = set(matched_value)
    for digit in set_matched_values_digits:
        for box in box_list:
            if digit in values[box]:
                if box not in remove_matching_values_items:
                    remove_matching_values_items.append(box)
    
    for box_index in remove_matching_values_items:
        if (len(matched_value) != 2 ):
            pass
        elif len(matched_value) is len(values[box_index]):
            pass
        elif len(values[box_index]) == 1:
            pass
        else:
            for digit in set_matched_values_digits:
                assign_value(values, box_index, values[box_index].replace(digit,''))    
    return values    
            

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    
    In a loop for each unit from the unitlist, call the find_naked_twins and find_replace_matching_twin_value functions.
    This takes care of finding the twins in each unit (including the diagonal ones) and replacing the values in other boxes in the same unit.
    """
    #values = reduce_puzzle(values)    
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        matched_value = find_naked_twins(unit, values)
        values = find_replace_matching_twin_value(unit, values, matched_value)
    return values    


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    print ('len(chars) - ' + str(len(chars)) )       
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[box]) == 1 for box in boxes): 
        return values ## Solved!
    
    # Chose one of the unfilled square s with the fewest possibilities
    digit_length, index = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for digit_values in values[index]:
        dfs_sudoku = values.copy()
        assign_value(dfs_sudoku, index, digit_values)
        result = search(dfs_sudoku)
        if result:
            return result
       
        

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    
    The way this diagonal sudoku is solved is by using the same logic for all contraints across the board in regular sudoku.
    The only difference being that the unitlist, units and peers dictionaries now include the diagonal elements.
    This eliminates the need for additional code to handle the eliminate, only_choice, reduce_puzzle and search functions :-) 
    """
    return search(grid)

if __name__ == '__main__':
    diag_sudoku_grid =  '...............9..97.3......1..6.5....47.8..2.....2..6.31..4......8..167.87......'
    #diag_sudoku_grid = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
    #diag_sudoku_grid = '..123......4........5...463...7.2..88...4...11..6.3...956...7........9......561..'
    #diag_sudoku_grid = '...28.94.1.4...7......156.....8..57.4.......8.68..9.....196......5...8.3.43.28...'
    #diag_sudoku_grid =  '...............9..97.3......1..6.5....47.8..2.....2..6.31..4......8..167.87......'
    #before_naked_twins = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8', 'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8', 'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5', 'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27', 'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6', 'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2', 'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9', 'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279', 'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}

    display(grid_values(diag_sudoku_grid))
    print(solve(grid_values(diag_sudoku_grid)))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
       