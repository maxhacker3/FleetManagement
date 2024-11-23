from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value

# Number of cars and customers
num_cars = 2
num_customers = 5

# Cost matrix (example values, replace with your actual costs)
cost = [
    [10, 15, 20, 25, 30],  # Car 1's cost for each customer
    [20, 10, 25, 15, 10]   # Car 2's cost for each customer
]

# Define the problem
prob = LpProblem("Taxi-Customer_Assignment", LpMinimize)

# Decision variables
x = [[LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(num_customers)] for i in range(num_cars)]

# Objective function: minimize total cost
prob += lpSum(cost[i][j] * x[i][j] for i in range(num_cars) for j in range(num_customers))

# Each customer is assigned to exactly one car
for j in range(num_customers):
    prob += lpSum(x[i][j] for i in range(num_cars)) == 1

# Each car is assigned to at most one customer
for i in range(num_cars):
    prob += lpSum(x[i][j] for j in range(num_customers)) <= 1

# Solve the problem
prob.solve()

# Output the results
for i in range(num_cars):
    for j in range(num_customers):
        if value(x[i][j]) == 1:
            print(f"Car {i+1} is assigned to Customer {j+1} with cost {cost[i][j]}")
