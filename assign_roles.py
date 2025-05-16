from ortools.sat.python import cp_model

def assign_roles():

    # Create the model
    model = cp_model.CpModel()

    # Data
    associates = ["A", "B", "C"]
    roles = ["Role1", "Role2", "Role3"]
    num_associates = len(associates)
    num_roles = len(roles)

    # Restrictions: Associate A can't do Role2 (index 1)
    restrictions = {("A", "Role2"): False}  # False means not allowed

    # Variables: assignment[i][j] = 1 if associate i is assigned to role j, else 0
    assignment = {}
    for i in range(num_associates):
        for j in range(num_roles):
            assignment[(i, j)] = model.NewBoolVar(f"assign_{associates[i]}_{roles[j]}")

    # Constraints
    # 1. Each role is assigned to exactly one associate
    for j in range(num_roles):
        model.AddExactlyOne(assignment[(i, j)] for i in range(num_associates))

    # 2. Each associate is assigned to at most one role
    for i in range(num_associates):
        model.AddAtMostOne(assignment[(i, j)] for j in range(num_roles))

    # 3. Apply restrictions
    for (assoc, role), allowed in restrictions.items():
        if not allowed:
            assoc_idx = associates.index(assoc)
            role_idx = roles.index(role)
            model.Add(assignment[(assoc_idx, role_idx)] == 0)

    # Objective: For prototype, maximize assignments (ensure all roles filled)
    # Later, you can add fairness (e.g., minimize max hours)
    model.Maximize(sum(assignment[(i, j)] for i in range(num_associates) for j in range(num_roles)))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output results
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Assignments:")
        for i in range(num_associates):
            for j in range(num_roles):
                if solver.Value(assignment[(i, j)]) == 1:
                    print(f"{associates[i]} assigned to {roles[j]}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    assign_roles()