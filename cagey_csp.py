# =============================
# Student Names: Robert He, Peter Zhou, Ethan Mah
# Group ID: 45
# Date: Jan 30, 2025
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

import itertools
from math import prod
from cspbase import *

def binary_ne_grid(cagey_grid):
    ''' A model of a Cagey grid (without cage constraints) built using only binary not-equal
    constraints for both the row and column constraints.'''
    n = cagey_grid[0]
    cells = []

    for i in range(n):
        row_cells = []
        for j in range(n):
            var = Variable(f"X_{i+1}_{j+1}", list(range(1, n+1)))   
            row_cells.append(var)
        cells.append(row_cells)

    var_array = [var for row in cells for var in row]
    csp = CSP("Cagey", var_array)


    def add_binary_constraints(var_list):
        '''Adds binary not-equal constraints for a given row or column.'''
        for i in range(len(var_list)):
            for j in range(i + 1, len(var_list)):
                con = Constraint(f"C_{var_list[i].name}_{var_list[j].name}", [var_list[i], var_list[j]])
                sat_tuples = [(a, b) for a in var_list[i].domain() for b in var_list[j].domain() if a != b]
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)

    for row in cells:
        add_binary_constraints(row)

    for col in zip(*cells):  
        add_binary_constraints(col)

    return csp, var_array


def nary_ad_grid(cagey_grid):
    ''' A model of a Cagey grid (without cage constraints) built using only n-ary
    all-different constraints for both the row and column constraints. '''
    n = cagey_grid[0]
    cells = []

    for i in range(n):
        row_cells = []
        for j in range(n):
            var = Variable(f"X_{i+1}_{j+1}", list(range(1, n+1)))
            row_cells.append(var)
        cells.append(row_cells)
    
    var_array = [var for row in cells for var in row]  
    csp = CSP("Cagey", var_array)


    def add_all_different_constraint(var_list):
        ''' Adds an n-ary all-different constraint for a given list of variables (row or column). '''
        con = Constraint("All-Different", var_list)
        sat_tuples = [(tuple(values)) for values in itertools.permutations(range(1, n+1), len(var_list))]
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)

    for row in cells:
        add_all_different_constraint(row)

    for col in zip(*cells):  
        add_all_different_constraint(col)

    return csp, var_array


def cagey_csp_model(cagey_grid):
    ''' a model of a Cagey grid built using your choice of (1) binary not-equal, or
        (2) n-ary all-different constraints for the grid, together with Cagey cage
        constraints. '''
    
    n = cagey_grid[0]  # Grid size
    cages = cagey_grid[1]  # List of cage constraints
    
    csp = CSP("Cagey")  # Create the CSP object
    grid_vars = [[Variable(f"V{i+1},{j+1}", [str(x) for x in range(1, n+1)]) for j in range(n)] for i in range(n)]

    # Flatten the grid variables
    var_array = [var for row in grid_vars for var in row]

    # Add each variable to the CSP object
    for var in var_array:
        csp.add_var(var)  # Make sure this is correctly adding the variable to the CSP object

    # Now add row and column constraints
    for i in range(n):
        # Row constraints
        row_constraint = Constraint(f"Row-{i+1}", grid_vars[i])
        row_constraint.add_satisfying_tuples(list(itertools.permutations(range(1, n+1), n)))
        csp.add_constraint(row_constraint)
        
        # Column constraints
        col_vars = [grid_vars[j][i] for j in range(n)]
        col_constraint = Constraint(f"Col-{i+1}", col_vars)
        col_constraint.add_satisfying_tuples(list(itertools.permutations(range(1, n+1), n)))
        csp.add_constraint(col_constraint)


    for target, cells, operation in cages:
        vars_in_cage = [grid_vars[r-1][c-1] for r, c in cells]
        cage_constraint = Constraint(
            f"Cage_op({target}:{operation}:[{' '.join([f'Var-Cell({r},{c})' for r, c in cells])}])",
            vars_in_cage
        )

        valid_tuples = []

        if operation == '+':
            for values in itertools.product(range(1, n+1), repeat=len(vars_in_cage)):
                if sum(values) == target:
                    valid_tuples.append(values)

        elif operation == '-':
            if len(vars_in_cage) > 2:
                for perm in itertools.permutations(vars_in_cage, 2):
                    if abs(perm[0] - perm[1]) == target:
                        valid_tuples.append(perm)
            else:
                print(f"Warning: Subtraction only supported for 2 variables, found {len(vars_in_cage)} variables.")

        elif operation == '*':
            # Initialize valid_tuples
            valid_tuples = []
            valid_factors = [i for i in range(1, n+1) if target % i == 0]
            for values in itertools.product(valid_factors, repeat=len(vars_in_cage)):
                product = 1
                for value in values:
                    product *= value
                    if product > target:
                        break
                if product == target:
                    valid_tuples.append(values)

        elif operation == '/':
            if len(vars_in_cage) == 2:
                for values in itertools.product(range(1, n+1), repeat=2):
                    if (values[0] % values[1] == 0 and values[0] // values[1] == target) or \
                       (values[1] % values[0] == 0 and values[1] // values[0] == target):
                        valid_tuples.append(values)
            else:
                print(f"Warning: Division only supported for 2 variables, found {len(vars_in_cage)} variables.")

        elif operation == '?':
            for op in ['+', '-', '*', '/']:
                if eval_cage_constraint(vars_in_cage, target, op):
                    valid_tuples.append(vars_in_cage)

        if valid_tuples:
            cage_constraint.add_satisfying_tuples(valid_tuples)
            csp.add_constraint(cage_constraint)
        else:
            print(f"Warning: No valid tuples for {cage_constraint.name} (target={target}, op={operation})")
    return csp, var_array


def eval_cage_constraint(vars_in_cage, target, operation):
    '''Evaluates whether the values in `vars_in_cage` satisfy the target for the given operation.'''

    values = [var.value for var in vars_in_cage]
    
    if operation == '+':
        return sum(values) == target
    
    elif operation == '-':
        if len(values) == 2:
            return abs(values[0] - values[1]) == target
        else:
            return False
    
    elif operation == '*':
        product = 1
        for value in values:
            product *= value
        return product == target
    
    elif operation == '/':
        if len(values) == 2:
            return (values[0] % values[1] == 0 and values[0] // values[1] == target) or \
                   (values[1] % values[0] == 0 and values[1] // values[0] == target)
        else:
            return False
    
    else:
        return False
