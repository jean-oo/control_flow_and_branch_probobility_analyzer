# Milestone 1

## Project Ideas:
1. Threading analyzer 
2. Memory utilization and leaks analyzer (potentially combined with pointer visualizer)
3. Control flow simplification (eg. if return else return can be simplified), while/for loop simplification, always true/false checks, final variable checks, etc

## Plans for next week:
1. Narrow down ideas
2. Discuss and brainstorm further

# Milestone 2

Choice of project: Null pointer check, division by zero in Java. Static Analysis <br>
TA discussion: We discussed the general scope of the project. <br>

## Team member responsibilities:
- AST/parsing: Wilson, Yutong
- Sketching out input/output: Jean, Jerome
- User study: Leo

## Summary of progress:
We have decided to do null pointer and division by zero checks for the project.

## Roadmap
| Week        | Goals     |
| ----------- | ----------- |
| November 1-5   (Milestone 2)  | Decide on project topic and scope, plan user study |
| November 6-12 (Milestone 3) | Perform task-driven prototype study, basic sketch of input/output finished, plan out implementation for checks |
| November 13-19 (Milestone 4/5) | Implement checks, plan for task-driven user study, testing and debugging |
| November 20-26 (Milestone 5) | Finish implementation, perform task-driven user study, plan for video |
| November 27-30 | Finalizing project, finish video |




# Milestone 3

## Project Mockup:
Control flow probability calculator and visualizer (+ providing suggestions for better code)

### Implementation steps:
1. Through dynamic analysis, gather statistics of control flow to train the Markov model or LSTM model.
2. Train Markov model / LSTM model using library
3. Provide a graph visualization (maybe with interactive feature)

Still need to decide which model to use e.g. Markov model or LSTM model

Markov model does not consider the path taken to the current node to calculate probabilities of going to the next basic block, however it still needs the control flow sequence to train the model.
LSTM model would require an interactive visualization component to allow users to select a path to the current node, and use this path to calculate the probability of going to another basic block from being in the current basic block.


## Notes From User Study:

- User was able to clearly understand the goals of the project.
- User noted the confusion of having multiple nodes with the same line number on the control flow sequence.
- Redesign (Manipulate the graph to combine nodes using the python package networkx)
- The user had a slight preference towards the LSTM model as they were intrigued by the interactive visualization component.

## Progress & Any changes to original design.

- Static control flow graph can be generated and passed to the visualizer (using NetworkX)
- LSTM model, dynamic analysis, and visualization still in progress

## Roadmap
| Week        | Goals     |
| ----------- | ----------- |
| November 13-19 (Milestone 4/5) | Train LSTM model, finish dynamic logging, begin visualization component |
| November 20-26 (Milestone 5) | Finish implementation, perform task-driven user study, plan for video |
| November 27-30 | Finalizing project, finish video |




# Milestone 4 
## Status of Implementation:
Completed initial design of the logger and static analysis. Started implementation on graph visualizer and ways to insert logged data onto the graph

## Plans for final user study:
We plan to have the final user study done on November 25th.

## Planned timeline for the remaining days:
Complete and finalize the implementation of logger and visualizer by November 25th and perform final user study. Debugging and finishing up the project and finishing the video before November 30th.

## Progress against the timeline planned for the team:
We are roughly on schedule right now according to our initial timeline with exceptions for the process of testing and debugging as we have yet have the chance to fully test the functionality of our implementation.

# Milestone 5
## Status of final user study:
In progress, will be performed on Sun

## Plans for final video:
Plan to begin working on video on Sun

## Planned timeline for the remaining days:
Fri-Sun: Finish implementation, perform task-driven user study, begin working on video
Mon-Tue: Finalizing project, finish video

## Progress against the timeline planned for the team:
We are roughly on schedule right now according to our initial timeline, still testing and debugging our implementation.
