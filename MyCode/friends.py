#Lesson 14 My version, with comments
from pyspark import SparkConf, SparkContext #Next few lines, boilerplate code

conf = SparkConf().setMaster("local").setAppName("FriendsByAge") #Running locally
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',') #split the values in the csv based on where , is
    age = int(fields[2]) #we only need the age in this var so grab age from 2nd param (remember start counting at 0)
    numFriends = int(fields[3]) #same idea, grab the 4th col, 3rd param for the number of friends
    return (age, numFriends) #return key value pair itself. Key age, value num of friends

lines = sc.textFile("file:///C:/Users/cenzo/SparkCourse/CSV/fakefriends.csv")

rdd = lines.map(parseLine)

# output will be:
# 33, 385
# 33, 2
# 55, 221
# 40, 465
# ...
# read this by seeing that the first user is 33 years old and has 385 friends

# chaining ops together is common practice in spark. Below transforming into tupels
totalsByAge = rdd.mapValues(lambda x: (x, 1)
    ).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

# rdd.mapValues(lambda x: (x,1))
# (33, 385) => (33, (385, 1))
# (33, 2) => (33, (2, 1))
# (55, 221) => (55, (221, 1))


# reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
# This adds up all values for each unique key.

averagesByAge = totalsByAge.mapValues(lambda x:x[0] / x[1])
# (33, (387, 2)) -> (33, 194.5)
# Remember, keys UNCHANGED

results = averagesByAge.collect()
for result in results: 
    print(result)