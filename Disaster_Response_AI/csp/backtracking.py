"""
Backtracking CSP Solver
-----------------------

Solves the resource allocation CSP using backtracking.

AI Concepts Covered:
- Constraint Satisfaction Problem
- Backtracking Search
"""

def backtracking_search(csp):
    """
    Entry point for solving CSP.
    """
    return backtrack({}, csp)


def backtrack(assignment, csp):
    """
    Recursive backtracking solver.

    assignment example:
    {
        'V1': 'A1',
        'V2': 'A2'
    }
    """

    # If assignment complete → solution found
    if len(assignment) == len(csp.variables):
        return assignment

    # Select unassigned variable
    var = select_unassigned_variable(assignment, csp)

    # Try domain values
    for value in csp.domains[var]:

        new_assignment = assignment.copy()
        new_assignment[var] = value

        if csp.is_valid(new_assignment):
            result = backtrack(new_assignment, csp)

            if result is not None:
                return result

    # No valid assignment found
    return None


def select_unassigned_variable(assignment, csp):
    """
    Select the next unassigned variable.
    """
    for variable in csp.variables:
        if variable not in assignment:
            return variable