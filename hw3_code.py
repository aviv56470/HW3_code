from scipy.optimize import linprog

# Variable order:
# x = [x11, x12, x14, x22, x25, x33, x34, x42, x45]
variables = ["x11", "x12", "x14", "x22", "x25", "x33", "x34", "x42", "x45"]

# Objective:
# Maximize x11 + x12 + x14 + x22 + x25 + x33 + x34 + x42 + x45
# linprog minimizes, so we minimize the negative objective
c = [-1, -1, -1, -1, -1, -1, -1, -1, -1]

# Inequality constraints of the form A_ub @ x <= b_ub
A_ub = [
    # Supplier capacity constraints
    [1, 1, 1, 0, 0, 0, 0, 0, 0],  # u1: x11 + x12 + x14 <= 3.5
    [0, 0, 0, 1, 1, 0, 0, 0, 0],  # u2: x22 + x25 <= 2
    [0, 0, 0, 0, 0, 1, 1, 0, 0],  # u3: x33 + x34 <= 4
    [0, 0, 0, 0, 0, 0, 0, 1, 1],  # u4: x42 + x45 <= 1.5

    # Consumer capacity constraints
    [1, 0, 0, 0, 0, 0, 0, 0, 0],  # v1: x11 <= 2.5
    [0, 1, 0, 1, 0, 0, 0, 1, 0],  # v2: x12 + x22 + x42 <= 3
    [0, 0, 0, 0, 0, 1, 0, 0, 0],  # v3: x33 <= 2
    [0, 0, 1, 0, 0, 0, 1, 0, 0],  # v4: x14 + x34 <= 1.5
    [0, 0, 0, 0, 1, 0, 0, 0, 1],  # v5: x25 + x45 <= 2
]

b_ub = [
    3.5,  # u1
    2,    # u2
    4,    # u3
    1.5,  # u4
    2.5,  # v1
    3,    # v2
    2,    # v3
    1.5,  # v4
    2     # v5
]

# Non-negativity constraints
bounds = [(0, None) for _ in variables]

# Solve the linear program
result = linprog(
    c=c,
    A_ub=A_ub,
    b_ub=b_ub,
    bounds=bounds,
    method="highs"
)

# Print the result
if result.success:
    print("An optimal solution was found!")
    print("The optimal value of the objective function is:", -result.fun)
    print()

    print("Variable values:")
    for var_name, value in zip(variables, result.x):
        if abs(value) < 1e-9:
            value = 0
        print(f"{var_name} = {value}")
else:
    print("No solution was found.")
    print(result.message)