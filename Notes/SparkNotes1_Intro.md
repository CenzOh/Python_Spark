# Notes for first few lessons of course
**Note:** Syntax of using Spark in Python is pretty similar to using Spark in Scala.

**RDD** - Resilient Distributed Dataset

**SC** - Spark Context, this is used when we use PySpark it creates a Spark Shell enviornment which in turn creates this SC object. 

**EX** - of hardcoding:
nums = parallelize([1,2,3,4])

Instead we would really use:
sc.textFile("file:///C:/users/frank/gob-o-text.txt")

Hive runs on top of Hadoop, basically for data warehousing. 
hiveCtx = HiveContext(sc) rows = hiveCtx.sql("SELECT name, age FROM users")

Cassandra is a NoSQL database.


We can transform RDD's with some common operations such as: 

map, take a set of data anad transform it into another set of data. Ex - square all numbers in a dataset, we will have a function that multiplies everything in the RDD by itself. One-to-one relationship. Everything in original gets mapped in the new RDD. Both RDDs have same amount of entries.

```flatmap```, similar but has capability to produce MULTIPLE values from the original RDD values. Could be LARGER or SMALLER than RDD we started with. 
``filter``, trim info we do not need. Think web log data but we want to filter / remove all the ones with error in it.
`distinct`, get only the unique values in an RDD, throw out the duplicate values.
`sample`, get a random sample of the dataset so we can work with a smaller size of the dataset. 
`union`, take two RDD inputs and output a single RDD. Union of the two
`intersection`, similar to above ?
`subtract`, the values from one RDD to another
`cartesian`, every combination between every element in RDD, that will blow p quick!

Powerul operations but not a lot of them.


**MAP example:**
```rdd = sc.parallelize([1,2,3,4])
rdd.map(lambda x:x*x) # will square every value in the RDD ```
### this yields 1,4,9,16

**Note**, a lot of the RDD methods can accept a fcn within the parameter such as lambda, instead of defining our own function.

Lambda? Python thing, concept called funcitonal programming. Pass in operation we want to perform on whole RDD. 


**RDD actions:**

`collect`, dump all values we have right now
`count`, how many values we have in RDD
`countByValue`, breakdown by unique value, how many times they occur
`take`, some sample of the final values
`top`, similar to above ?
`reduce`, write a fcn that lets us combine all different values for a given key value, boil down to an aggregation of our RDD. 

**Note:** Nothing happens in RDD / drive rprogram UNTIL an action is taken. RDD is foundation of spark!!