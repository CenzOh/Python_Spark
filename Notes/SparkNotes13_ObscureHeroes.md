## Lesson 39, Reviewing solution for most Obscure Superheros

My solution and prompt: `mostObscureHero.py`
Instructor solution: `most-obscure-superheros.py`

First, we start with a copy of the most popular superhero dataFrame script. I will go over what code snippets are different. 

```
minConnectionCount = connections.agg(func.min("connections")).first()[0]
```
This is first line that is NOT identical. So in this line, we are trying to figure out what is the smallest number of connections without hardcoding in the value. So we take the connections dataFrame and call `func.min("connections")` this will find the minimum value in the connections column. We also add `.agg()` since we are applying that to the aggregate of the entire connections dataFrame. Next, we call `.first()` because there should only be ONE minimum. `[0]` simply extracts the result of that. The first column we get back will be the result of the min number of connections seen on the dataFrame. Again this should equal one.
```
minConnections = connections.filter(func.col("connections") == minConnectionCount)
```
Next up, we do `connections.filter()` where the `connections` column is equal to the `minConnectionCount` which will equal 1. This gives us bakck a new dataFrame called `minConnections`. This contains ONLY connections where the number of connections euqals to one! This, of course, will be a much smaller data set to deal with. 
```
minConnectionsWithNames = minConnections.join(names, "id")
```
This next line joins in with the actual names. Note that this was done after filtering out the data. This is way more efficient. Why spend a lot of time mapping all IDs to names when there are a lot of IDs we will not even use? Better to find WHICH IDs we need, THEN map it out. 
To explain what is going on in this line of code, we join the `names` dataFrame with the `minConnections` dataFRame based on the column name "ID". Both `connections` and `minConnections` has an ID field and the `names` dataFrame also has the ID field. Think SQL join operation. Both of these contain the super hero IDs so we can now join the names to the corresponding IDs. So in effect, this will append a names column from the `names` dataFrame to our `minConnections` dataFrame. The resulting dataFrame is called `minConnectionsWithNames`.
```
print("The following characters have only " + str(minConnectionCount) + " connection(s):")

minConnectionsWithNames.select("name").show()
```
This next line prits the results. We will also convert the connection count to a string connections. After we print out results with the `.show()` fcn. We also use `select()` and pick only the name column, we do not care about displaying the other info.
 