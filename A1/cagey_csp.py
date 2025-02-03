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

from itertools import permutations, product
from math import prod
from cspbase import *

def binary_ne_grid(cagey_grid):
    ''' A model of a Cagey grid (without cage constraints) built using only binary not-equal constraints for both the row and column constraints.'''
    n = cagey_grid[0]
    cells = [[Variable(f"X_{i+1}_{j+1}", list(range(1, n+1))) for j in range(n)] for i in range(n)]
    var_array = [var for row in cells for var in row]
    csp = CSP("Cagey", var_array)
    
    def add_binary_constraints(var_list):
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
    '''A model of a Cagey grid (without cage constraints) built using only n-ary
    all-different constraints for both the row and column constraints.'''
    n = cagey_grid[0]
    cells = [[Variable(f"X_{i+1}_{j+1}", list(range(1, n+1))) for j in range(n)] for i in range(n)]
    var_array = [var for row in cells for var in row]
    csp = CSP("Cagey", var_array)
    
    def add_all_different_constraint(var_list):
        con = Constraint("All-Different", var_list)
        sat_tuples = [tup for tup in permutations(range(1, n+1), len(var_list))]
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)
    
    for row in cells:
        add_all_different_constraint(row)
    for col in zip(*cells):  
        add_all_different_constraint(col)
    
    return csp, var_array



def cagey_csp_model(cagey_grid):
    '''a model of a Cagey grid built using your choice of (1) binary not-equal, 
    or (2) n-ary all-different constraints for the grid, together with 
    Cagey cage constraints.'''
    
    n, cages = cagey_grid
    csp = CSP("Cagey")
    
    grid_vars = [[Variable(f"Var-Cell({i+1},{j+1})", list(range(1, n+1))) for j in range(n)] for i in range(n)]
    var_array = [var for row in grid_vars for var in row]
    for var in var_array:
        csp.add_var(var)
    
    for i in range(n):
        row_constraint = Constraint(f"Row-{i+1}", grid_vars[i])
        row_constraint.add_satisfying_tuples([tup for tup in permutations(range(1, n+1), n)])
        csp.add_constraint(row_constraint)

        col_vars = [grid_vars[j][i] for j in range(n)]
        col_constraint = Constraint(f"Col-{i+1}", col_vars)
        col_constraint.add_satisfying_tuples([tup for tup in permutations(range(1, n+1), n)])
        csp.add_constraint(col_constraint)
    
    for target, cells, operation in cages:
        vars_in_cage = [grid_vars[r-1][c-1] for r, c in cells]

        cage_var_name = f"Cage_op({target}:{operation}:[{', '.join([f'Var-Cell({r},{c})' for r, c in cells])}])"
        cage_var = Variable(cage_var_name, [operation]) 
        var_array.append(cage_var)
        csp.add_var(cage_var)

        vars_in_cage_with_cage_var = [cage_var] + vars_in_cage  
        cage_constraint = Constraint(f"Cage({target},{operation})", vars_in_cage_with_cage_var)
        
        valid_tuples = []
        for values in product(range(1, n+1), repeat=len(vars_in_cage)):
            if operation == '+':
                if sum(values) == target:
                    valid_tuples.append((operation,) + values)
            elif operation == '-' and len(vars_in_cage) == 2:
                a, b = values
                if abs(a - b) == target:
                    valid_tuples.append((operation, a, b))
                    valid_tuples.append((operation, b, a)) 
            elif operation == '*':
                if prod(values) == target:
                    valid_tuples.append((operation,) + values)
            elif operation == '/' and len(vars_in_cage) == 2:
                a, b = values
                if (a % b == 0 and a // b == target) or (b % a == 0 and b // a == target):
                    valid_tuples.append((operation, a, b))
                    valid_tuples.append((operation, b, a))  
        
        if valid_tuples:
            cage_constraint.add_satisfying_tuples(valid_tuples)
            csp.add_constraint(cage_constraint)

    return csp, var_array






def eval_cage_constraint(values, target, operation):
    if operation == '+':
        return sum(values) == target
    elif operation == '-' and len(values) == 2:
        return abs(values[0] - values[1]) == target
    elif operation == '*':
        return prod(values) == target
    elif operation == '/' and len(values) == 2:
        return (values[0] % values[1] == 0 and values[0] // values[1] == target) or (values[1] % values[0] == 0 and values[1] // values[0] == target)
    return False