"""
Backtracking CSP Solver
-----------------------

Solves the resource allocation CSP using backtracking.

AI Concepts Covered:
- Constraint Satisfaction Problem
- Backtracking Search
"""

def backtracking_search(csp):

    best_assignment = {}
    best_score = float('-inf')

    def backtrack(assignment):

        nonlocal best_assignment, best_score

        if len(assignment) > 0:
            score = csp.calculate_score(assignment)

            if score > best_score:
                best_score = score
                best_assignment = assignment.copy()

        for var in csp.variables:

            if var not in assignment:

                for value in csp.domains[var]:

                    new_assignment = assignment.copy()
                    new_assignment[var] = value

                    if csp.is_valid(new_assignment):
                        backtrack(new_assignment)

                return  # important (same as your logic)

    backtrack({})
    return best_assignment


def select_unassigned_variable(assignment, csp):

    for var in csp.variables:
        if var not in assignment:
            return var


def forward_check(var, value, csp):

    removed = []

    for v in csp.variables:
        if value in csp.domains[v] and v != var:
            csp.domains[v].remove(value)
            removed.append((v, value))

    return removed


def restore_domains(removed, csp):

    for var, value in removed:
        csp.domains[var].append(value)