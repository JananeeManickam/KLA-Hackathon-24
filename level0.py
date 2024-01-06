# import math
# import itertools
# import json

# # Function to load the input data (JSON format)
# def load_data(filename):
#     f_in = open('Input data\level0.json')
#     data = json.load(f_in)
#     return data

# # Function to construct the graph representation
# def construct_graph(data):
#     # graph = {}
#     # for node, distances in data["restaurants"].items():
#     #     graph[node] = distances["neighbourhood_distance"]
    
#     src_distances = [] # SOURCE DISTANCE
#     for neighbourhood, info in data["restaurants"].items():
#         src_distances.append(info["neighbourhood_distance"])

#     distances_list = [] # 20 NEIGHBORHOOD DISTANCES 
#     for neighbourhood, info in data["neighbourhoods"].items():
#         distances_list.append(info["distances"])

    
#     return distances_list, src_distances

# # Function to implement the Brute Force TSP algorithm
# def solve_tsp_brute_force(graph, start_node):
#     nodes = list(graph)
#     print("NODES:",nodes)
#     print("STRT_NODES:",start_node)
#     shortest_distance = math.inf
#     shortest_route = None

#     for permutation in itertools.permutations(nodes):
#         if permutation[0] != start_node:  # Ensure starting node is at the beginning
#             continue

#         total_distance = 0
#         for i in range(len(permutation) - 1):
#             total_distance += graph[permutation[i]][permutation[i + 1]]
#         total_distance += graph[permutation[-1]][permutation[0]]  # Return to starting node

#         if total_distance < shortest_distance:
#             shortest_distance = total_distance
#             shortest_route = permutation

#     return shortest_route, shortest_distance

# # Main function to execute the solution
# def main():
#     data = load_data("input.json")  # Replace with your input file
#     graph, start_node = construct_graph(data)
    
#     # print(graph)
#     # print(start_node)
    
#     shortest_route, total_distance = solve_tsp_brute_force(graph, start_node)
    
#     print("Shortest route:", shortest_route)
#     print("Total distance:", total_distance)

# if __name__ == "__main__":
#     main()







import json
from collections import defaultdict
import heapq
import sys

file=open('Input data/level0.json')
data=json.load(file)

n=data["n_neighbourhoods"]
# print("no.of neighbours is:",n)

#restaurant distance to neighbours
rest_distance=[]
rest_distance=data["restaurants"]["r0"]["neighbourhood_distance"]
print(rest_distance)

#neighbours distance
node_list=['n0','n1','n2','n3','n4','n5','n6','n7','n8','n9','n10','n11','n12','n13','n14','n15','n16','n17','n18','n19','r0']
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

def nearest_neighbor(dist_matrix, start_vertex):
    n_vertices = len(dist_matrix[0])

    unvisited = set(range(n_vertices))
    path = [start_vertex]
    current_vertex = start_vertex
    total_distance = 0

    unvisited.remove(start_vertex)

    while unvisited:
        nearest_vertex = min(unvisited, key=lambda vertex: dist_matrix[current_vertex][vertex])
        total_distance += dist_matrix[current_vertex][nearest_vertex]
        current_vertex = nearest_vertex
        path.append(nearest_vertex)
        unvisited.remove(nearest_vertex)

    # Return to the start vertex
    total_distance += dist_matrix[current_vertex][start_vertex]
    path.append(start_vertex)

    return path, total_distance

start_vertex = 20

path, total_distance = nearest_neighbor(dist_matrix, start_vertex)

# write into json file output
for i in range(len(path)):
    path[i]=node_list[path[i]]
#print(path)
output={"v0":{"path":path}}
#print(output)
json_object=json.dumps(output,indent=len(path))
with open("Output/level0_output.json", "w", encoding='utf-8') as outfile:
    outfile.write(json_object)

print("Nested JSON data written to 'my_data.json' successfully!")
file.close()