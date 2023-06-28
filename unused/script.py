import pygraphviz as pgv
import networkx as nx
import matplotlib.pyplot as plt
import json

G = pgv.AGraph("graph.txt")
G_ = nx.drawing.nx_agraph.from_agraph(G)

# nodes = list(G_.nodes(data=True))

delNodes = []

for i in list(G_.nodes):
    pNode = G_._node[i]['line']

    pNodeLabel = G_._node[i]['label']


    if i not in G_._node.keys():
        continue

    if pNodeLabel.find('exit') != -1:
        delNodes.append(i)


    children = G_.successors(i)

    for c in children:
        if G_._node[c]['line'] == pNode:
            if c not in delNodes:
                delNodes.append(c)

for delNode in delNodes:
    for pred in G_.predecessors(delNode):
        for succ in G_.successors(delNode):
            G_.add_edge(pred, succ)

    G_.remove_node(delNode)


nodeList = reversed(list(G_.nodes))

for i in nodeList:
    if i not in G_._node.keys():
        continue

    pNodeLabel = G_._node[i]['label']

    if pNodeLabel.find(" elif") != -1:
        for c in list(G_.successors(i)):
            if ((G_._node[c]['label'].find(" if") != -1) or (G_._node[c]['label'].find(" elif") != -1)):
                G_._node[i]['label'] = G_._node[i]['label'] + '\n' + G_._node[c]['label']
                ids = [G_._node[i]['line']]
                if type(G_._node[c]['line']) is list:
                    ids.extend(G_._node[c]['line'])
                else:
                    ids.append(G_._node[c]['line'])
                for succ in list(G_.successors(c)):
                    G_.add_edge(i, succ)
                G_.remove_node(c)
                break
        if 'ids' in locals():
            G_._node[i]['line'] = " ".join(ids)

for i in list(G_.nodes):
    if i not in G_._node.keys():
        continue

    pNodeLabel = G_._node[i]['label']

    if "\n" in pNodeLabel:
        G_._node[i]['label'] = G_._node[i]['label'].replace(" elif", " if")

for i in list(G_.nodes):
    print(G_._node[i]['label'])
    print(G_._node[i]['line'])

# print(labels)
# nx.draw(G_, with_labels=True, font_weight='bold')
a = nx.nx_agraph.to_agraph(G_)
a.layout(prog='dot')
a.draw("graph.png")

j = json.dumps(nx.node_link_data(G_))

print(j)

with open("static/graph.json", "w") as outfile:
    outfile.write(j)

# plt.show()