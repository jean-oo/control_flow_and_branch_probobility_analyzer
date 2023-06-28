from staticfg import CFGBuilder
import networkx.drawing.nx_pydot
import pydot
import json
import networkx as nx
import re
from sys import argv

cfg = CFGBuilder().build_from_file(argv[1], "./"+argv[1])

cfg.build_visual('outputCFG', 'png')

results = {}

with open('outputCFG', 'r') as fp:
    dot_list = pydot.graph_from_dot_data(fp.read())
    for dot in dot_list:
    	results[dot.get_name()] = networkx.drawing.nx_pydot.from_pydot(dot)
    	for subgraph in dot.get_subgraph_list():
            results[subgraph.get_name()] = networkx.drawing.nx_pydot.from_pydot(subgraph)

graphs = []

for key,value in results.items():
	if len(list(value.nodes)) > 0:
		value._node[list(value.nodes)[0]]['isFunctionHead'] = True
	for node in list(value.nodes):
		value._node[node]['cluster'] = key
	graphs.append(value) 

G = nx.union_all(graphs)

for i in list(G.nodes):
	temp = G._node[i]['label'].replace('\\"', "")

	nodeLine = temp.split(':')[0]

	nodeLine = re.findall(r'\d+', nodeLine)

	if len(nodeLine) != 0:
		G._node[i]['line'] = nodeLine[0]
	G._node[i]['label'] = temp

graphJSON = json.dumps(nx.node_link_data(G))

with open("static/graph.json", "w") as outfile:
    outfile.write(graphJSON)