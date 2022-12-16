## Lecture 14, Key Value RDDS 
We will be using a friends broken down by age example. RDDs can hold key value pairs such as a total number of friends by their age. In this case the key would be the age and the value would be the number of friends. Rather than seperate lists of ages and of num of friends, we will store them as (age, num of friends), (age, num of friends), ... Key value pairs / Key value RDDs look like NoSQL databases.

Syntatically, nothing special to create them. We simply map pairs of data into an RDD, example:

`` totalsByAge = rdd.map(lambda x: (x,1)) ``

It is as simple as this to create a key value RDD. We can have lists as a value too. Not limited to storing just one thing.

Some functions:
``reduceByKey()`` combines all values with SAME key using a function. ex, adding all the values to a key do this: ``rdd.reduceByKey(lambda x, y: x+y)`` here we call a lambda function to add x and y.
``groupByKey()`` groups values with SAME key.
``sortByKey()`` sort RDD by the key values
``keys(), values()`` create RDD of just keys or just values. 
``join, rightOuterJoin, leftOuterJoin, cogroup, subtractByKey`` these are SQL style joins we can do on two key value RDDs. 

If we DO NOT modify keys with the transformations, we need to call ``mapValues(), flatMapValues()`` rather than JUST ``map(), flatMap()``. More efficient, Spark can maintain partioning original data rather than shuffle it around which can get expensive. 
Note that when calling mapValues or flatMapValues, the actual values themselves will be passed in. Keys will be fine, this just means that they are NOT being modified and exposed to us.  Again, these value fcns only recieve the value of the key value pair. 
Real example: please view the fakefriendssample csv file


### Task - find average number of friends by age. Ex - average num of friends for a 33 year old. 

So what we want to do is parse / map the input data.
Please refer to friends.py file.
Output of key value paris of (age, num of freinds):
33, 385
33, 2
55, 221
40, 465

Read this by seeing that the first user is 33 years old and has 385 friends.

`` totalsByAge = rdd.mapValues(lambda x: (x, 1)
    ).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])) ``

First we have this compound operation. Call the values with mapValues. it transforms every value in key value pair so the x will be passed in as value piece in original RDD. Ex, the first entry in original RDD with 33 year old with 385 friends, the value 385 will be passed in through mapValues for EVERY LINE, this is the x variable. Output is a pair or a list of 385 (x) and number 1.

rdd.mapValues(lambda x: (x,1))

`` (33, 385) => (33, (385, 1))
(33, 2) => (33, (2, 1))
(55, 221) => (55, (221, 1)) ``

To get an avg, we need to count total num of friends for a given age and number of times the age occurred. The way we can read this is, we have the total amount of friends as the first value in the list, and then the value for the total number of times that age occurred in the second value in the list. In other words we are building a total of how many times 33 year olds were seen and total number of friends that they had.
Our output with the RDD.mapValues() fcn is a new RDD but remember, the keys within this key value pair are UNTOUCHED. The values have been transformed from the number of friends to a pair value of 385 and 1.

Add everything together with the following:
`` reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))``

This adds up all values for each unique key. SO think this, x can be 385 and y is 2, 1. So then we would just add up each component by taking the first element of each value and adding them together, then take the second element of each value and adding them together. Below is the output where we would do 385 + 2 = 387 and 1 + 1 = 2. We do this for everytime we envounter values for the key 33

(33, (387, 2)) this is grand total of number of friends, 387, with how many times we saw that key, 2.

``averagesByAge = totalsByAge.mapValues(lambda x:x[0] / x[1]) ``
(33, (387, 2)) -> (33, 194.5)

``results = averagesByAge.collect()
for result in results: 
    print result``

Remember, nothing in SPark happens until an action is called. First action is reduceByKey. Our other action in the script is the collect call.
 