#Entry point for script orchestration



from sys import argv
import os
import traceInjectionScript

import json
import pandas as pd
from networkx.readwrite import json_graph
import networkx as nx
import contextlib

##Start of static analysis part
def getidToLineMap(jsonFilename):
    idMap = {}
    with open(jsonFilename, "r") as file:
        jsonContents = json.load(file)
        nodes = jsonContents["nodes"]
        for node in nodes:
            id = node["id"]
            if "line" not in node:
                continue
            lineString: str = node["line"]
            lines= lineString.split()
            idMap[id] = {}
            idMap[id]["lines"] = lines
            idMap[id]["linesString"] = lineString
            idMap[id]["conditional"] = (len(lines) > 1)
    return idMap

def getLineToIdMapAndConditionalMap(jsonFilename):
    lineMap = {}
    conditionalMap = {} #Maps from conditional lines to the combined line string
    with open(jsonFilename, "r") as file:
        jsonContents = json.load(file)
        nodes = jsonContents["nodes"]
        for node in nodes:
            if "line" not in node:
                continue
            lineString: str = node["line"]
            lineMap[lineString] = {}
            lineMap[lineString]["id"] = node["id"]
            lines= lineString.split()
            if (len(lines) > 1):
                lineMap[lineString]["conditional"] = True
                for line in lines:
                    conditionalMap[line] = lineString
            else:
                lineMap[lineString]["conditional"] = False
    return lineMap, conditionalMap


os.system("python3 "+ "buildGraph.py " + argv[1])
##Start of dynamic analysis part
newFileName = traceInjectionScript.run(argv[1]) #Create new temp file for analysis
originalArgsList = []
for i in range(2,len(argv)): #Append user arguments to list
    originalArgsList.append(argv[i])


os.system("python3 "+ newFileName+ " " + " ".join(originalArgsList)) #Call temp new file (which will produce dynamicResults.json now)


idTolineMap = getidToLineMap("static/graph.json") #Will have to change the file locations 
lineToIdMap, conditionalMap = getLineToIdMapAndConditionalMap("static/graph.json")
#Clean up dynamicResults json so that it doesn't include unecessary things before the start of the node graph

node_color = []
startLines = []
with open("static/graph.json", "r") as graphJson:
    
    graphDict = json.load(graphJson)
    links = graphDict["links"]
    for link in links:
        if link["source"] == "0":
            startNodeId = link["target"]
            startLines = idTolineMap[startNodeId]['lines']

with open("dynamicResults.json", "r+") as dynamicResultsFile:
    dynamicResults= json.load(dynamicResultsFile)
    for i in range(0,len(dynamicResults)):
        currentLineNumber = dynamicResults[i]
        if str(currentLineNumber) in startLines: 
            del dynamicResults[:i]
            break
    # Combine if else numbers
    for i in range(len(dynamicResults)):
        if dynamicResults[i] in conditionalMap:
            dynamicResults[i] = conditionalMap[dynamicResults[i]]


    # dynamicResults.insert(0, "0")
    # dynamicResults.append("-1")
    dynamicResultsFile.seek(0)
    dynamicResultsFile.truncate(0)
    json.dump(dynamicResults, dynamicResultsFile)
    #Get one-step markov transitional probabilities
    normalizedProbabilities = pd.crosstab(pd.Series(dynamicResults[1:], name = "Next Line"),
            pd.Series(dynamicResults[:-1], name = "Current Line"),normalize=1)
    transitionCounts = pd.crosstab(pd.Series(dynamicResults[1:], name = "Next Line"),
            pd.Series(dynamicResults[:-1], name = "Current Line"),normalize=False)

with open("transitionProbabilities.txt", "w") as probFile:
    print(normalizedProbabilities, file=probFile)

targetNodeSet = set()

with open("static/graph.json", "r+") as graphJson:
    graphDict = json.load(graphJson)
    links = graphDict["links"]
    for i in range(len(links)):
        if "style" in links[i]:
            continue
        sourceLines = idTolineMap[links[i]["source"]]["linesString"]
        targetLines = idTolineMap[links[i]["target"]]["linesString"]
        
        targetNodeSet.add(links[i]['target'])

        if (sourceLines in normalizedProbabilities ) and (targetLines in normalizedProbabilities[sourceLines]):
            graphDict["links"][i]["percentage"] = str(round(normalizedProbabilities[sourceLines][targetLines] * 100, 2)) + "%"
            graphDict["links"][i]["count"] = str(transitionCounts[sourceLines][targetLines] )
        else:
            graphDict["links"][i]["percentage"] = "0%"
            graphDict["links"][i]["count"] = "0"
        if graphDict["links"][i]['label'] != "\"\"":
            graphDict["links"][i]['label'] = "Percentage: " + graphDict["links"][i]["percentage"] + "\nCount: " + graphDict["links"][i]["count"]
        else:
            graphDict["links"][i]['label'] = ""
    nodes = graphDict["nodes"]
    for i in range(len(nodes)):
        if "isFunctionHead" in nodes[i] and nodes[i]["isFunctionHead"]:
            nodes[i]["label"] = "Start of: " + nodes[i]["cluster"].strip("\"") + "\n\n" + nodes[i]["label"].strip("\"")
        label = nodes[i]["label"]
        if label.startswith("\"") and label.endswith("\""):
            nodes[i]["label"] = label.strip("\"")
    graphJson.seek(0)
    graphJson.truncate(0)
    json.dump(graphDict, graphJson)



with open("static/graph.json") as f:

        js_graph = json.load(f)
        for node in js_graph["nodes"]:
            if( "isFunctionHead" in node ):
                node['style'] = "bold"


        for link in js_graph["links"]:
            if('Percentage:' in link["label"]) :
                i = link['percentage']
                prob = float(i.replace("%", ""))
                if (prob > 50.0):
                    link['color'] = 'green'
                else:
                    link['color'] = 'red'

        nxGraph = json_graph.node_link_graph(js_graph)
        a = nx.nx_agraph.to_agraph(nxGraph)  #Returns a pygraphviz graph from a nxGraph.

         # a.node_attr.update(color='red')

        a.layout(prog='dot')
        a.draw("graph.png")
        
with contextlib.suppress(FileNotFoundError):
    os.remove(newFileName) #Remove temp new python file
    os.remove("outputCFG.png")
    os.remove("outputCFG")
    os.remove("outputCFG.dot")
    os.remove("graph.txt")



def main():
    if len(argv) < 2:
        print("You must pass in an argument for the python file name!")
        exit(0)
if __name__ == "__main__":
    main()