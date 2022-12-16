## Lesson 42, Review code of super hero degrees of separation.

File is called `degrees-of-separation.py`. Code review.

```
startCharacterID = 5306 #SpiderMan
targetCharacterID = 14  #ADAM 3,031 (who?)
```
These are the two character IDs we are looking for. We want to see how many degrees of separation ADAM 3,031 is from SpiderMan.
```
# Our accumulator, used to signal when we find the target character during
# our BFS traversal.
hitCounter = sc.accumulator(0)
```
Remember, accumulator signals the driver script when we have actually found Adam. 
```
def convertToBFS(line):
    fields = line.split()
    heroID = int(fields[0])
    connections = []
    for connection in fields[1:]:
        connections.append(int(connection))

    color = 'WHITE'
    distance = 9999

    if (heroID == startCharacterID):
        color = 'GRAY'
        distance = 0

    return (heroID, (connections, distance, color))
```
Above sets up the initial conditions of our graph and converts input data into node structures. Each entry of our RDD is going to consist of a key value pair where the key is super hero ID and value is a composite value that consists of a list of connections, the distance, and the color. 
Remember, initial distance is 9999 implying infinity and initial color is WHITE. SPiderman is the exception, he will be colored GRAY to start and have a starting distance of 0 because Spiderman has a degree of separation of 0 from himself. GRAY indicates we have to expand upon that node.

Going to skip the meat of the program and go through the main program. 
```
#Main program here:
iterationRdd = createStartingRdd()
```
First, we call this function the `createStartingRDD()`. This does the following:
```
def createStartingRdd():
    inputFile = sc.textFile("file:///c:/users/cenzo/sparkcourse/csv/marvel-graph.txt")
    return inputFile.map(convertToBFS)
```
First we load in the input file with `sc.textFile()`, we are loading the `graph.txt` file. Then the fcn calls the `convertToBFS` function. That is the function we described earlier to make it look like Node IDs in BFS traversal.
Next in the main program we do this:
```
for iteration in range(0, 10):
    print("Running BFS iteration# " + str(iteration+1))
```
Here, we go through some upper bound of iterations. We will assume that we are never going to be MORE than 10 degrees of separation from anybody in this graph. If so, they prob are not connected at all!! We really are just picking some arbitrary upper bound here and will run iterate through the graph doing the BFS traversal up to ten times. First time we will be running BFS iteration number one, then we call our flatmap, which runs the first step we discussed in the previous lecture of blowing out all of the gray nodes. 
Then, that calls our BFS map function:
```
    # Create new vertices as needed to darken or reduce distances in the
    # reduce stage. If we encounter the node we're looking for as a GRAY
    # node, increment our accumulator to signal that we're done.
    mapped = iterationRdd.flatMap(bfsMap)
```
The following is what the `BfsMap()` function does:
```
def bfsMap(node):
    characterID = node[0]
    data = node[1]
    connections = data[0]
    distance = data[1]
    color = data[2]

    results = []

    #If this node needs to be expanded...
    if (color == 'GRAY'):
        for connection in connections:
            newCharacterID = connection
            newDistance = distance + 1
            newColor = 'GRAY'
            if (targetCharacterID == connection):
                hitCounter.add(1)

            newEntry = (newCharacterID, ([], newDistance, newColor))
            results.append(newEntry)

        #We've processed this node, so color it black
        color = 'BLACK'

    #Emit the input node so we don't lose it.
    results.append( (characterID, (connections, distance, color)) )
    return results
```
As discussed, it extracts the info from each node and looks for gray nodes and blows them out. After, it will color them black and create new gray nodes from their connections. Since this is a flat map, we return a results list of nodes that get added into the new resulting RDD.
Finally, we put the original node back onto the list as well so we can reconnect its connections back to that node in the reducer. This creates not only the original node we started wit, but new nodes (potentially) that are colored gray that need to be expanded upon. For each new node we expanded upon, we increment the distance to keep track of the degrees of separation. 
If need review, look back on the last two lectures.
To make all of this happen, we must call an action:
```
    # Note that mapped.count() action here forces the RDD to be evaluated, and
    # that's the only reason our accumulator is actually updated.
    print("Processing " + str(mapped.count()) + " values.")
```
Recall how we have lazy evaluation in spark, IE just calling `flat map()` DOES NOT make anything happen. A very key thing occurred in the `BfsMap()` fcn. It is this line below:
```
            if (targetCharacterID == connection):
                hitCounter.add(1)
```
So, if we encountered the character that we were looking for, we increment our hit counter / accumulator. **Super important**. To explain again, the moment we encounter Adam 3031, this hit counter is going to get incremented which signals back to our driver script that we have found the person we are looking for. 
However, map functions are transforms. THey do not actually cause anything to actually get run in spark UNTIL we call an action. So what we do here is a bit of a cheat. We call the `mapped.count()` fcn on the RDD to force it to get evaluated and that way, our accumulator will get set at this point. 
It will also print out some interesting informaiton as a side effect. We can see how we are processing more and more nodes as we expand outward from our starting node. 
Upon this mapping pass, if we DID inf act encounter Adam 3031, we do the following:
```
  if (hitCounter.value > 0):
        print("Hit the target character! From " + str(hitCounter.value) \
            + " different direction(s).")
        break
```
Here we check if `hitCounter` has incremented, if so, print it out and say we found our guy! We can also print out HOW many times the hit counter was hit because we can actually come at a given character from many different direction spotentially! If not, we keep on processing so we will call the following:
```
    # Reducer combines data for each character ID, preserving the darkest
    # color and shortest path.
    iterationRdd = mapped.reduceByKey(bfsReduce)
```
We call the `reduceByKey()` function to actually gather together all of the nodes that we might have generated in the flat map operation and recombine them together for each given character ID. There can be only one node per character ID and that enforces that. 
`BfsReduce()` simply gathers them ALL back together snad preserves the min distance as well as darkest color found and reconnect the list of all the connections that were found for the original node.

We iterate through until we hit a maxium of 10 iterations, however, nothing will get that high.
Below is output:
```
C:\Users\cenzo\SparkCourse\InstructorCode>spark-submit degrees-of-separation.py
Running BFS iteration# 1
Processing 8330 values.
Running BFS iteration# 2
Processing 220615 values.
Hit the target character! From 1 different direction(s).
```
We only had to go through two steps to find the connection between spiderman and this obscure character. THat is pretty cool!!
It is also interesting that we can use Spark to complete this complex operation we would have not thought of as something spark could do! You simply have to think about stuff in different ways to model it.
      
      