# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

1. ord_dh (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Degree heuristic

2. ord_mv (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Minimum-Remaining-Value heuristic


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    Variables and constraints of the problem. The assigned Variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' Return the next variable to be assigned according to the Degree Heuristic '''
    # IMPLEMENT
    varlist = csp.get_all_unasgn_vars()
    maxdegree = -1  
    nextvar = None

    for var in varlist:
        degreeset = set()
        conlist = csp.get_cons_with_var(var)

        for cons in conlist:
            degreeset.update(v for v in cons.get_unasgn_vars() if v != var)

        degree = len(degreeset)

        if degree > maxdegree:
            maxdegree = degree
            nextvar = var
        elif degree == maxdegree and nextvar is None:
            nextvar = var

    return nextvar

def ord_mrv(csp):
    ''' return Variable to be assigned according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    varlist = csp.get_all_unasgn_vars()
    print(varlist)
    nextvar = varlist[0]
    lowestvalue = (varlist[0]).cur_domain_size()

    # remembers the var with the smallest current domain
    for var in varlist:
        value = var.cur_domain_size()
        if lowestvalue > value:
            lowestvalue = value
            nextvar = var

    return nextvar
