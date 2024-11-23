import requests
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

BASE_URL = "http://localhost:8080"
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

def set_scenario2(scenario_id):
    s = get_scenario(scenario_id)
    number_cars = len(s[0]['vehicles'])
    number_cust = len(s[0]['customers'])
    ###Backend access
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
        return response.json()  # Assuming the response is JSON
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
    num_cars = input("Number of cars\n")
    num_cust = input("Number of Customers\n")
    scenario = init_scenario(number_cars = num_cars, number_cust = num_cust)
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


def get_scenarios():
    url = f"{BASE_URL}/scenarios"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")


def metadata(scenario_id):
    url = f"{BASE_URL}/scenario/{scenario_id}/metadata"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")

def filter_scenario(scenario_id):
    pass
if __name__ == "__main__":
    resp = get_scenarios()
    customers = resp[0]["vehicles"]
    #id = resp[0]['id']
    print(len(customers))
