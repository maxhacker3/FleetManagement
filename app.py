import requests
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value
import time
import subprocess
import os
import csv


from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_scenario_running(id, allocation):
    url = f"{BASE_URL_RUNNER}/Scenarios/get_scenario/{id}"
    response = requests.get(url)
    res = response.json()
    c = res["customers"]
    cars = res["vehicles"]
    _,id, allocation = assign_customers_to_vehicles(res, allocation=allocation)
    print(f"ID: {id}")
    with open("id.csv", "w") as File:
        writer = csv.writer(File)
        writer.writerow(id)

    return res, res['id']

@app.route('/get_scenario/<int:id>', methods=['GET'])
def create_app(id):
    try:
        
        scenario_data, id = get_scenario_running(id)
        return jsonify(scenario_data), 200
    except requests.exceptions.RequestException as e:
        # Handle errors when calling the external API
        return jsonify({"error": "Failed to fetch scenario", "details": str(e)}), 500


def main(idd):
    id = idd  # Example: Initialize the ID in main
    app = create_app(id)
    app.run(port=8090)



def start_react_server():
    react_app_path = "./dashboardd/" 

    try:
        os.chdir(react_app_path)
        process = subprocess.Popen(
            ["npm", "start"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        print("Starting React server...")
        time.sleep(5)

        return process

    except Exception as e:
        print(f"Failed to start React server: {e}")
        return None

BASE_URL = "http://localhost:8080"
BASE_URL_RUNNER = "http://localhost:8090"





def assign_customers_to_vehicles(scenario, allocation):
    customers = scenario["customers"]
    for vehicle in scenario["vehicles"]:
        is_available = vehicle["isAvailable"]
        print(f"Vehicle ID: {vehicle['id']}, Occupied: {not is_available}, Loc: ({vehicle['coordX']}, {vehicle['coordX']})")
        if vehicle["isAvailable"]:
            vehicle_id = vehicle["id"]

            
            for customer_id in allocation[vehicle_id]:  
                customer = next((cust for cust in customers if cust["id"] == customer_id), None)

                if customer and customer["awaitingService"]:  
                    
                    vehicle["customerId"] = customer_id
                    vehicle["isAvailable"] = False

                    # Update customer details
                    customer["awaitingService"] = False
                    break
        else:
            continue

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    url = f"{BASE_URL_RUNNER}/Scenarios/initialize_scenario"
    
    try:
        # Send POST request with JSON payload
        response = requests.post(url, headers=headers, json=scenario)
        
        # Check if the response is successful
        if response.status_code == 200:
            respon = response.json()
            return respon, scenario["id"], allocation
        else:
            return {
                "status": "Failed",
                "error": response.text,
                "code": response.status_code
            }
    except requests.exceptions.RequestException as e:
        # Handle connection issues or other exceptions
        return {
            "status": "Failed",
            "error": str(e)
        }
    



def get_scenario(scenario_id):
    url = f"{BASE_URL}/scenarios/{scenario_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")

def set_scenario(number_cars, number_cust):
    url = f"{BASE_URL}/scenario/create"
    params = {
        "numberOfVehicles": number_cars,
        "numberOfCustomers": number_cust
    }
    headers = {"accept": "application/json"}
    response = requests.post(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")




def get_customer(customer_id):
    url = f"{BASE_URL}/customers/{customer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  
    else:
        print(f"Error: {response.status_code}, {response.text}")

def get_customers(scenario_id):
    url = f"{BASE_URL}/scenarios/{scenario_id}/customers"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
def get_vehicles(scenario_id):
    url = f"{BASE_URL}/scenarios/{scenario_id}/vehicles"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
def get_vehicle(vehicle_id):
    url = f"{BASE_URL}/vehicles/{vehicle_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")

def get_poisson():
    ### showcase function

    num_cars = input("Number of cars\n")
    num_cust = input("Number of Customers\n")
    scenario = set_scenario(number_cars = num_cars, number_cust = num_cust)
    df = pd.DataFrame(scenario["customers"])
    dff = df[["coordX", "coordY"]].to_numpy()
    dfff = df[["destinationX", "destinationY"]].to_numpy()
    
    plt.figure(figsize = (12,8))
    distances = []
    for i in range(len(dff[:,0])):
        #plt.plot([dff[i,0], dfff[i,0]], [dff[i,1], dfff[i,1]], ".-", lw = 0.1, color = "Black")
        distances.append(np.sqrt((dff[i,0] - dfff[i,0])**2 + (dff[i,1] - dfff[i,1])**2))
    
    plt.hist(distances)
    #haa
    #plt.scatter(dfff[:,0], dfff[:,1], s = 3, color = "Orange")
    plt.show()


def LinearOptimization(scenario):
    # Linear optimization programme
    num_cars = len(scenario["vehicles"])
    num_cust = len(scenario["customers"])
    df = pd.DataFrame(scenario["customers"])
    df_veh = pd.DataFrame(scenario["vehicles"])
    dff = df[["coordX", "coordY"]].to_numpy()
    dfff = df[["destinationX", "destinationY"]].to_numpy()
    num_customers = len(df["coordX"])
    num_cars = len(df_veh["coordX"])
    plt.figure(figsize = (12,8))
    distances = []
    for i in range(len(dff[:,0])):
        plt.plot([dff[i,0], dfff[i,0]], [dff[i,1], dfff[i,1]], ".-", lw = 0.1, color = "Black")
        plt.scatter(df_veh["coordX"], df_veh["coordY"])
        distances.append(np.sqrt((dff[i,0] - dfff[i,0])**2 + (dff[i,1] - dfff[i,1])**2))
    def loss_matrix(customer_info, vehicle_info):
        rel_vehicle_data = vehicle_info[["coordX", "coordY"]]
        rel_customer_data = customer_info[["coordX", "coordY", "destinationX", "destinationY"]]
        loss = np.zeros((len(rel_vehicle_data["coordX"]), len(rel_customer_data["coordX"])))
        for i, (_, row_v) in enumerate(rel_vehicle_data.iterrows()):
            for j, (_, row_c) in enumerate(rel_customer_data.iterrows()):
                distance = np.sqrt((row_c["destinationX"] - row_c["coordX"])**2 + (row_c["destinationY"] - row_c["coordY"])**2)
                anfahrt = np.sqrt((row_c["coordX"] - row_v["coordX"])**2 + (row_c["coordY"] - row_v["coordY"])**2)
                mu = anfahrt / distance if distance > 0 else np.inf
                loss[i, j] = mu
        return loss
    
    prob = LpProblem("Taxi-Customer_Assignment", LpMinimize)
    x = [[LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(num_cust)] for i in range(num_cars)]
    cost = loss_matrix(df, df_veh)

    # Loss function
    prob += lpSum(cost[i][j] * x[i][j] for i in range(num_cars) for j in range(num_cust))

    # Here, the constraints are formulated
    for j in range(num_cust):
        prob += lpSum(x[i][j] for i in range(num_cars)) == 1
    for i in range(num_cars):
        prob += lpSum(x[i][j] for j in range(num_cust)) <= 1

    prob.solve()
    d = {}
    for i in range(num_cars):
        customer_costs = []
        for j in range(num_cust):
            if value(x[i][j]) == 1:  # If the customer is assigned to the car
                customer_costs.append((df.loc[j, "id"], cost[i][j]))
        customer_costs.sort(key=lambda x: x[1])
        d[df_veh.loc[i, "id"]] = [cust_id for cust_id, _ in customer_costs]
    
                #print(f"Car {i+1} is assigned to Customer {j+1} with cost {cost[i][j]:.2f}")
    # Plot the best first options for the cars
    plot = False
    if plot:
        for i in range(len(x)):  
            indices = []
            for j in range(len(x[i])):  
                if value(x[i][j]) == 1:
                    indices.append(j)
            res = np.array([cost[i][index] for index in indices])
            argmin = np.argmin(res)
            passenger_index = indices[argmin]
            plt.plot([df_veh["coordX"][i], df["coordX"][passenger_index]],[df_veh["coordY"][i], df["coordY"][passenger_index]], "--")

        plt.legend()
        plt.show()

    
    
    return d, x, cost




def get_scenarios():
    url = f"{BASE_URL}/scenario/create"
    params = {
        "numberOfVehicles": 2,
        "numberOfCustomers": 5
    }
    headers = {"accept": "application/json"}
    response = requests.post(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")


def extract_distance_matrix(customers):
    #### unnötig
    df_customers  = pd.DataFrame(customers)
    df_customers["Distances"] = np.sqrt(
        (df_customers["coordX"] - df_customers["destinationX"])**2 +
        (df_customers["coordY"] - df_customers["destinationY"])**2
    )
    return df_customers


def check_taxi_status(order):
    #check taxi status, if its occupied
    for index, row in order.iterrows():
        vehicle_id = row["id"]
        url = f"{BASE_URL}/vehicles/{vehicle_id}"
        response = requests.get(url).json()
        IA = response["isAvailable"]
        print(f"Taxi: {vehicle_id}, Status: {IA}")

def launch(scenario_id):
    headers = {"accept": "application/json"}
    params = {
        "scenario_id" : scenario_id,
        "speed" : 0.002
    }
    response = requests.post(
        f"{BASE_URL_RUNNER}/Runner/launch_scenario/{scenario_id}",
        headers=headers, params = params
    )
    if response.status_code == 200:
        
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")


if __name__ == "__main__":
    #LinearOptimization()
    
    scenario = get_scenarios()
    allocation, x, loss = LinearOptimization(scenario)
    response, id, allocation = assign_customers_to_vehicles(scenario, allocation= allocation)
    final_response = launch(id)
    #sc_id = final_response["scenario_id"]
    #print(final_response)
    for i in range(10):
        resp, id = get_scenario_running(id, allocation)
        time.sleep(10)

    app.run(port = 8090)

    react_process = start_react_server()

    if react_process:
        print("React server started successfully.")
        # Do other tasks or wait for user to terminate the process
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Terminating React server...")
            react_process.terminate()
    #customers = scenario[0]["customers"]
    #vehicles = scenario[0]["vehicles"]
    
    #res = assign_customers_to_vehicles(customers, vehicles)
    #strategy_id = next(iter(res)) 
    #meta = metadata(strategy_id)

    #order = determine_order(customers, vehicles).dropna()
    #response = assign_customers_to_vehicles(order)
    #solution_id = next(iter(response))
    
    #print(launch("scenario_1"))
    #check_taxi_status(order)
    #print(response[0]['vehicles'])
    