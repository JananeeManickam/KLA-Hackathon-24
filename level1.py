import json

def findMinRoute(tsp):
    num_nodes = len(tsp)
    visited = [False] * num_nodes
    visited[0] = True  # Start from the first node 'r0'
    route = [0]  # Initialize the route with the starting node
    
    current_node = 0
    total_distance = 0

    for _ in range(num_nodes - 1):
        min_distance = float('inf')
        next_node = None

        for neighbor in range(num_nodes):
            if neighbor != current_node and not visited[neighbor] and tsp[current_node][neighbor] < min_distance:
                min_distance = tsp[current_node][neighbor]
                next_node = neighbor
        
        if next_node is not None:
            route.append(next_node)
            visited[next_node] = True
            total_distance += min_distance
            current_node = next_node

    # Adding the distance back to the starting node
    total_distance += tsp[current_node][0]
    route.append(0)

    print("Total distance:", total_distance)
    print("Route:", route)

    path_labels = ['r0'] + [f'n{i}' for i in range(num_nodes - 1)]
    path = [path_labels[node] for node in route]

    result = {"v0": {"path": path}}

    with open("my_data.json", "w") as f:
        json.dump(result, f, indent=4)

    print("Nested JSON data written to 'my_data.json' successfully!")

f_in = open('Input data/level0.json')
data = json.load(f_in)

src_distances = [info["neighbourhood_distance"] for _, info in data["restaurants"].items()]
distances_list = [info["distances"] for _, info in data["neighbourhoods"].items()]

tsp = src_distances + distances_list
findMinRoute(tsp)
