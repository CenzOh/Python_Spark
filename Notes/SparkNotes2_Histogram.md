## Lesson 13, breaking down ratings histogram 

First, we import what we need:

`` from pyspark import SparkConf, SparkContext
import collections``

We imported the collections to sort from Python.
Next we st up our context:

`` conf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc = SparkContext(conf = conf)``

Will look similar in all Spark scripts in Python. Spark Conf set the master node to the local machine, run on local one system not a cluster. We CAN split it up among multiple CPU cores. We did not need to do distribution of data in this example. Set the app name as part of the call, this is so we can look into the Spark Web UI so we can monitor it and find it by Job Name!! 
Now we create spark context object, always call it SC for spark context.
Now we load up the data file:

`` lines = sc.textFile("file:///SparkCourse/ml-100k/u.data")``

So, a common way to create an RDD is through the sc.textFile, it will look through the local file system and find that u.data file. QUICK NOTE that for me I had to EXPLICITLY define the path of this file so I had to write the whole 'C:\...' Took me way too long to figure that one out. THis breaks up the input file line by line into balues. One line in one value. 

`` ratings = lines.map(lambda x: x.split()[2]) ``

Extracting or mapping the data we want. Lamnbda shorthand passes functions. X is passed into splut, extracting the 2 number field. This splits on EACH line. THis is what the input looks like:
196 242 3   881250949
These values represent:
user ID, movie ID, rating value, timestamp. 
So in other words, User 196 watched movie 242, gave it a 3 out of 5 star rating at this particualr timestamp. 
This function with the split ONLY grabs the star rating from each line since the star rating is field number 2. All of this goes into a NEW RDD called ratings. Again the new RDD will ONLY have the ratings value from EACH line in the original RDD.
NOTE: THe origianl, lines, RDD is UNAFFECTED by this function. Nothing has changed in the original RDD. 

`` result = ratings.countByValue() ``

Perform an action which is count by value. Quick way to create something like a histogram. So for instance, if our new RDD has the following ratings PULLED from each line in the old RDD: 
3,3,1,2,1. 
The count by value will count HOW MANY TIMES the value has occurred. SO in this case, a 3 star rating occurred only two times. So the output would be: 
(3,2), (1,2), (2,1). 
Read this by looking at the first value 3, has occurred the amount of times in the second value which is 2. These are tuples, pair values. This object is also now a regualr python object not an RDD so we can do what we want with it.

`` sortedResults = collections.OrderedDict(sorted(result.items()))
for key, value in sortedResults.iteritems():
    print "%s %i" % (key, value) ``

THis is python code, using collections package to create a dictonary and sort them in order. Iterate through every key value pair. End result is the following:
1 2
2 1
3 2
Essentially its the original key value pair from before but sorted.