#Lesson 28 my code
# PROBLEM: Revisit the friends by age example but this time, use a dataframe.
#ID, name, age, num of friends
#0, Will, 33, 385
# Find the average number of frineds that each age has.

#TIPS:
# use the fakefriends-headers csv, already has headers. DONE
#use select("col1", "col2") statement to aquire the columns we need.
# some good data frame fcns to use are avg("colName"), groupBy("colName"), show()
#Look at the spark-sql-dataframe.py file for extra help

from pyspark.sql import SparkSession, functions as func #func will be used later, I did not use this originally

spark = SparkSession.builder.appName("FriendsDataFrame").getOrCreate()

people = spark.read.option("header", "true").option("inferSchema", "true")\
    .csv("file:///c:/users/cenzo/SparkCourse/csv/fakefriends-header.csv") #use header row and infer the schema based on current input inside the csv so this can guess what kind of attributes are in the csv

# result = (spark.sql("SELECT age, AVG(friends) FROM people GROUPBY age")) 
# doesnt work but this is my thought process of how the SQL statement would execute.
# for results in result.collect():
#     print(results)

# newDataFrame = people.select("age", "friends") #can do this so we do not have to have access or use any other data that we do not need

people.groupby("age").avg("friends").show() #for some reason, doing avg first DOES NOT WORK. This solves the problem in one line. DataFrames simplify

#Taking it further: 

people.groupby("age").avg("friends").sort("age").show() # we are sorting by age so lowest age is at the top which in our case is 18 and then as the column goes down, the age goes up, 19, 20, 21...
 
people.groupby("age").agg(func.round(func.avg("friends"), 2)).sort("age").show() #people.round did not work. This sets the decimal value to 2.
#Note, agg means aggregare, we want to take the aggregated results from the groupby for all the vlaues of that age, that we grouped together. Within that set of aggregated results, here, we will take the average and round it by two.

people.groupby("age").agg(
    func.round(
        func.avg("friends"), 2)
    .alias("avg_num_of_friends")).sort("age").show()
    #finally, alias is a function to change the name of the column.

spark.stop() #cant forget to stop the program