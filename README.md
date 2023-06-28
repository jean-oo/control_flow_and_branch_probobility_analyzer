# Control Flow and Branch Probability Analyzer

### Group 22

Jean Xue, 
Joram Tsai, 
Leo Shin, 
Wilson Tung, 
Yutong Li

## Introduction

For project 2, we created a Python control flow analyzer that allows the user to understand a python script’s program flow and see the probabilities of each branch taken. The outputs will hopefully allow the user more understanding into their program, as well as perhaps refactoring the branches for efficiency. The program will read a user-specified python script and output a png image of the program’s flowchart with each branch’s respective probability labeled alongside the edges.

## Example Output
![example image](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group22/blob/main/example.png)

## Setting up the environment
Make sure your computer has python installed and has the proper path setup. Here’s a link to help setting up the python environment: https://www.tutorialspoint.com/python/python_environment.htm 

Since our program implements many external Python modules, the user would have to locally install these library with the following command in the terminal (or powershell for windows users): <br />

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; pip install -r requirements.txt

If an error is encountered during the installation, please see the troubleshooting section below.

## Running the program
1) Create a file containing the Python script to be analyzed. 
2) Using the terminal (powershell), cd into the project directory and run the following command: <br /><br />
For Mac users: <br />
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;python entry.py **[the path of the file] [list of arguments the file needs]**<br /><br />
For Windows users: <br />
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;python entryAlt.py **[the path of the file] [list of arguments the file needs]**<br /><br />
3) The image of the flowchart can be found by opening graph.png in the project directory

## Detailed information regarding the design of the project
Our program analyzes Python scripts both statically and dynamically.

### The static analyzer:
To obtain the flowchart of the script, our program will first statically read the source code using an ast. Then, it will parse the gathered information into a JSON file containing nodes and edges of the program’s flowchart.

### The dynamic analyzer:
To obtain the probabilities of each branch being visited, we dynamically log line information of the script and parse the data into a JSON file. And with the JSON file, we then were able to create a Markov transition matrix using the line data and obtain the probabilities of each edge in the flowchart being taken.

### The visualizer:
With JSON files containing the flowchart’s nodes and edges along with a transitional matrix of the probability of all edges being taken, the program would then generate a png image of the complete flowchart and label each edge with probabilities and number of times taken. For the edges in the graph that are taken > 50% of the time, they are colored green; and red vice-versa. To prevent the graph from being too crowded and messy, we’ve decided to only include percentages for edges that are meaningful (edges pointing out from if/else/for/while nodes).

### Output Files:

graph.png   (visualization output)

dynamicResults.json ( line sequence of the file execution)

transitionProbabilities.txt (transition probability matrix of the lines)

### Constraints of the program
Due to trouble with overlapping line numbers and other extraneous behavior, our analysis program would only track and produce the graph for the file specified. If the file calls other files, they will be reduced to a simple function call in the result.

## Troubleshooting
If you have trouble installing graphviz and pygraphviz, see the following link: <br />
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://pygraphviz.github.io/documentation/stable/install.htm
