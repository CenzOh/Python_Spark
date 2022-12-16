## Lesson 41, using BFS in Spark and accumulators
We want to represent each line as a node with connections, a color, and a distance. Different from my version. Instructor version example:
```
5983 1165 3836 4361 1282
becomes
(5983, (1165, 3836, 4361, 1282), 999, WHITE)
```
What this means is, our initial condition is that a node is infinitely distant (9999) and white. Read this as hero ID 5983 appeared with hero IDs 1165, etc.
Turning this into a map function to convert marvel-graph.txt to BFS nodes
```
def convertToBFS(line):
    fields = lines.split()
    heroID = int(fields[0])
    connections = []
    for connection in fields[1:]:
        connections.append(int(connection))

    color = 'WHITE'
    distance = 999

    if(heroID == startCharacterID):
        color = 'GRAY'
        distance = 0

    return(heroID, (connections, distance, color))
```
esentially we make this node look a like into an actual key value pair of a key of a hero ID and a vlaue that is a composite value of te list connections, the distance and color. Makes it easier for us to group together by heroID later.
First part of the code, we split up the input line, extract the hero ID from the first field and then with Python we extract all of the fields from numbe one forward (the [1:] part). This lets us iterate through all friends or lets us iterate through that hero ID that are fields one going forward and appends into a list of connections.
At this point, we have a hero ID, that we extracted. A list of all connections for that hero ID. Finally we set the initial conditions that we talked about to WHITE and infinite distance except for initial condition.
Ex - we start with Hulk and the hero ID we encounter is the Hulk, we would know this is the guy we want to start from. Measuring the degrees of separation form the Hulk to himself, we color this node GREY and give him an initial distance of zero, meaning that the Hulk is the Hulk. Grey means this node NEEDS to be processed and expanded upon through the next iteration of BFS. 
Again, final output is key value pair where hero ID is the key, and the value is the list of connections. The list consists of the distance and the color. 

**Iteratively process the RDD!** Just like each step of our BFS example. Go through looking for gray nodes to expand. Color nodes we are finished with BLACK. Update the distances as we go through. We will iterate multiple times. Idea is this fcn is looking for the degree of separation between TWO different characters. 

**BFS iteration as a map and reduce job**. The mapper - creates new nodes for each connection of grey nodes, with a distance incremented by one, color gray, and no connections. Colors the grey node we just processed black. Copies the node itself into the results.
The reducer - Combines together all nodes for the same hero ID. Preserves the shortest distance, and the darkest color found. Preserves the list of connections from the original node. 

**How do we know when we are done?** An **acumulator** allows many executors to increment a shared variable. For instance:
`hitCounter = sc.accumulator(0)` sets up a shared accumulator with an initial value of 0. For each iteration, if the character we are interested in is hit, we increment the hitCOunter accumulator. After each iteration, we check if hitCounter is greater than one - if so, we are done. 
Recall how a broadcast variable allows us to share objects across all the nodes in our cluster. An accumulator allows all of the exectors in the cluster to increment some shared variable. Think of a counter that is mantained and synchronized across all of the different nodes in our cluster. 
Example, we call accumulator function on our spark context with an initial value of 0 and we can call that accumulator object our hitCounter. When going through the iterations, if any node that happens to be running this job encounters the character we are looking for, we can increment the hitcounter accumulator. Every other node and our dirver script has access to this. SO after each iteration, we can check that counter to see if anybody incremented it. Multiple nodes may have incremented it. IE - we found the guy we are looking for. 
