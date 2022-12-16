#Lesson / Exercise 22 my code, writing this on my own!!
# Looking at the customer orders csv file

# the way we read the CSV is: 
# customer ID, Item ID, amount spent
# 44, 8602, 37.19

# what we need to do is write a script that consolidates to total amount spent by the customer. So for instance, if we have two fields for customer number 44 where they spent 37.19 and another where they spent 40.64, the output should add the total amounts together to equal 77.83.

# final output is:
# customer ID, total
# 44, 77.83

#Strategy: 
# Split each CSV line into fields, DONE
# map each line to key value pairs of customer ID and dollar amount, DONE 
# use reduceByKey to add up the amount spent by customer ID, 
# collect() the results and print them.

#Useful snippets:  
# split comma delimited fields: fields = line.split(','). DONE
# Treat 0 as an int and field 2 as float: return (int(fields[0]), float(fields[2])). DONE

from pyspark import SparkConf, SparkContext #boilerplate

conf = SparkConf().setMaster("local").setAppName("TotalAmountOrdered")
sc = SparkContext(conf = conf)

def parseLine(line): #we will have to parse the lines since we are reading from a CSV file
    fields = line.split(',') #split each csv line into fields
    return (int(fields[0]), float(fields[2])) # map each line to key value pairs. Cast to int and float respectively. customerID, dollarAmount. Instead of variables, I just put this in return statement.

lines = sc.textFile("file:///C:/Users/cenzo/SparkCourse/CSV/customer-orders.csv") #read from correct file

rdd = lines.map(parseLine) #parse the lines first prior to adding them

# totalAmount = rdd.mapValues(lambda x: (x, 1)
#     ).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])) #this did not work since this adds one to each occurance. Output would be 33(128,1)
totalAmount = rdd.reduceByKey(lambda x, y: x+y) #I had the right idea before when I tried to do the x+y in reduceByKey but I was recieving an error due to me also writing mapValues. We do not need to use map values since we are simply adding the current values toegether.
# HOW DOES THIS WORK IN reduceByKey? Again, lambda allows us to do inline functions. This fcn adds up all of the values encountered given a customer ID. Remember that customerID is the key while amount spent is the value. 
# now gather the total amount. the ReduceByKey adds up the total amount. x = CustomerID, the key. y = ItemAmount, the value.

results = totalAmount.collect() #collect and print results
for result in results: 
    print(result)