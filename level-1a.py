import json
from collections import defaultdict
import heapq
import sys

file = open("Input data/level1a.json")
data = json.load(file)

# Extract relevant data
n_neighbourhoods = data["n_neighbourhoods"]
order_quantities = [info["order_quantity"] for neighbourhood, info in data["neighbourhoods"].items()]
rest_distance = data["restaurants"]["r0"]["neighbourhood_distance"]
                                          
#neighbours distance
node_list=['n0','n1','n2','n3','n4','n5','n6','n7','n8','n9','n10','n11','n12','n13','n14','n15','n16','n17','n18','n19','r0']



# Define constraints
CARRIER_CAPACITY = 600  
MIN_DISTANCE = 500  


dist_matrix=[]
x=0
for i in data["neighbourhoods"]:
    weight=[]
    for j in data["neighbourhoods"][i]["distances"]:
        weight.append(j)
    weight.append(rest_distance[x])
    x=x+1
    dist_matrix.append(weight)
i=0
rest_distance.append(i)
dist_matrix.append(rest_distance)

# Create function to calculate order size and distance
def order_size_distance(node, dist_matrix):
    order_size = order_quantities[node]
    distance = sum(dist_matrix[node])
    return order_size, distance

# Implement a modified Nearest Neighbor algorithm with constraints
def constrained_nearest_neighbor(dist_matrix, start_vertex, slots):
    n_vertices = len(dist_matrix[0])
    unvisited = set(range(n_vertices))
    current_slot = {"orders": [], "distance": 0}
    slots.append(current_slot)
    current_vertex = start_vertex
    total_distance = 0

    unvisited.remove(start_vertex)

    while unvisited:
        next_vertex = min(
            unvisited,
            key=lambda vertex: (
                dist_matrix[current_vertex][vertex],
                order_size_distance(vertex, dist_matrix)[1],
            ),
        )
        order_size, next_distance = order_size_distance(next_vertex, dist_matrix)

        # Check if adding order exceeds slot capacity
        if current_slot["orders"] and (
            sum(o[0] for o in current_slot["orders"]) + order_size > CARRIER_CAPACITY
        ):
            start_new_slot = True
        elif next_distance < MIN_DISTANCE:
            # If minimum distance not met, create new slot with current vertex
            start_new_slot = True
        else:
            start_new_slot = False

        if start_new_slot:
            current_slot = {"orders": [], "distance": 0}
            slots.append(current_slot)

        current_slot["orders"].append((next_vertex, order_size))
        current_slot["distance"] += dist_matrix[current_vertex][next_vertex]
        current_vertex = next_vertex
        total_distance += dist_matrix[current_vertex][next_vertex]
        unvisited.remove(next_vertex)

    # Return to start vertex and update distance
    total_distance += dist_matrix[current_vertex][start_vertex]
    current_slot["distance"] += dist_matrix[current_vertex][start_vertex]

    return slots, total_distance

# Run the algorithm
start_vertex = 20  # Set bakery location
slots = []
delivery_plan, total_distance = constrained_nearest_neighbor(dist_matrix, start_vertex, slots)

# Convert node IDs to names
for slot in delivery_plan:
    slot["orders"] = [(node_list[i], n) for i, n in slot["orders"]]

# Save output to JSON
output = {"v0": {"delivery_plan": delivery_plan, "total_distance": total_distance}}
json_object = json.dumps(output, indent=4)
with open("Output/level1_output.json", "w", encoding="utf-8") as outfile:
    outfile.write(json_object)

print(f"Delivery plan generated! Total distance: {total_distance}")

file.close()
