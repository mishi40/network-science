import graph_tool.all as gt
import sys

args = sys.argv
if len(args) > 1:
    input_name = f"{args[1]}.txt"
    output_name = f"{args[1]}.gt"

edge_list = []
with open(input_name, 'r') as f:
    for line in f:
        u, v = line.split()
        edge_list.append((u, v))

g = gt.Graph(directed=False)
v_original_id = g.add_edge_list(edge_list, hashed=True)
g.vertex_properties["name"] = v_original_id
g.save(output_name)

