## Lesson 40, Superhero degrees of separation - BreadthFirst Search.

Have you heard of this idea that everyone is connected through this six degrees of separation? Somebody you know, knows somebody else, who knows somebody else, etc. You can eventually be connected to pretty much EVERYONE on the planet. 
We can bring this idea of degrees of separation to our superheroes dataset / virtual social network of super heroes. Let us figure out the degree of separation between any two heros in that dataset. 
We find this out using an algorithm called **Breadth-First-Search**. 
This is the more complicated aspect of Spark problems. The following can be framed as Spark problems even though they may not seem like it.
Think of this, our example issue will deal with so much data it can not be handled on just one machine so we have to kind of use Spark or something like it to analyze data and pick relationships out of these larger social network data sets.

Okay here is an example of the degree of separation with some super heroes simplified:
```
Iron Man - Thor
    \      /
Incredible Hulk - Spider-Man
```
Okay so in this example we see that spide man is connected to the hulk who is connected to iron man. SO if we want to know the degrees of separation between spiderman and ironman, with this we can say that they are **two degrees** of separation from each other. Whereas the hulk and thor are **one degree**, the hulk and iron man are also **one degree**. 
In other words, we are asking how many hops do you need to go through in some common acquaintance in order to find a connection with somebody else? Again, we do this with BFS which will search through a graph like this. We track through the whole graph and keep track of the distances from the hulk to any other character.
Below is a mroe complex example to travel through in the graph using letters and the lines represent the connections between them. We can think of it like, a line represents two superheroes appear together in the same comic book at some point. We have these complicated relationships that go on. Not very straighforward so we need an algorithm to help us solve it.
```
R---S   T---U
|   | / |   |
V   W---X---Y
```
The idea is that we have associated each superhero with one of these letters, the ID is associated as well as a distance to the node that we are interested in. As well as a color to keep track of its processing state. 
Ex - lets say S represents Hulk and we want to measure how many degrees of separation people are from the Hulk? I will write it out in a list to count the distance as well as write the path. 
When we start with Hulk, the distance / degrees of separation equals 0.
```
S expand - 0 
```
I will also specify with 'expand' next to the distance if that node can be expanded upon. 
This algorithm is iterative so we will pass through the graph multiple times until we discover every node. 
```
S - R expand - 1 
S - W expand - 1 
```
Okay next, we expaned and we see that nodes R and W are **one degree** of separation from the Hulk. Now we pass through it all again and we have to expand R and W in the next pass.
```
S - W - T expand - 2
S - W - X expand - 2
```
First, we expand W. We have processed everything in W. W can not be expanded anymore. T and X need to be explored next. Increment the distance to equal **two degrees** of separation from the Hulk. We DID NOT explore R yet. We will do that now.
```
S - R - V expand - 2
```
Next we expanded R. R has been processed all the way. DIstance is now 2. Explore V further. THis is our second pass. Third pass lets expand T.
```
S - W - T - U expand - 3
```
NOTE that we HAVE come across X before, T does connect to X. We will not change it, no different. S to X will still have a distance of 2. U is new. Distance is 3. Now we explore X
```
S - W - X - Y expand - 3
```
Newly discovered node Y. DIstance 3. Still need to process V, who is not connected to anyone:
```
S - R - V - 2
```
V is done now. U and Y are not connected to anyone new so nothing is really going to happen after we visit and process them:
```
S - W - T - U - 3
S - W - X - Y - 3
```
Finished. 