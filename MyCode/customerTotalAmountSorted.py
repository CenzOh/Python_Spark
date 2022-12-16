#Lesson / Exercise 23 my code, sort the customer total amount 
from pyspark import SparkConf, SparkContext #boilerplate

conf = SparkConf().setMaster("local").setAppName("TotalAmountOrdered")
sc = SparkContext(conf = conf)

def parseLine(line): 
    fields = line.split(',') 
    return (int(fields[0]), float(fields[2])) 
    #return (float(fields[2]), int(fields[1]))  # ALTERNATE OPTION I think
lines = sc.textFile("file:///C:/Users/cenzo/SparkCourse/CSV/customer-orders.csv") #read from correct file

rdd = lines.map(parseLine) 
totalAmount = rdd.reduceByKey(lambda x, y: x+y)
totalSortedAmount = totalAmount.map(lambda x: (x[1], x[0])).sortByKey()
 #to sort this, we want to sort it by total spent so we can see who is biggest spender. TO do this we need to swap the key and values so the amount spent becomes the key

results = totalSortedAmount.collect() 
for result in results: 
    print(str(result[1]) + "\t\t" + str(result[0])) #need to change how output is printed, we do not want the total amount to be pritned first. We also have to cast the result to a string
   