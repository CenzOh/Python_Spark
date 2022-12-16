#Exercise / Lesson 32, another example for me to go through and complete
# read the cusomter-orders.csv file example, we will be working with a dataframe in this example

# to read data, we have:
# customer ID, Item ID, amount spent
# 44, 8602, 37.19

#we want to transform the data so that we can have JUST customer ID and total spent. COmpute this with dataframes.
# 44, 77.83

# TO DO:
# load data (customer-orders.csv) file as a dataFrame with schema - DONE
# group by cust_id - DONE
# sum by amount_spent (BONUS: round to 2 decimal places) - DONE
# sort by total spent - DONE
# show the results - DONE

from pyspark.sql import SparkSession, functions as func #boiler plate
from pyspark.sql.types import StructField, StructType, IntegerType, FloatType #we require this to write our own schema for the dataframe


spark = SparkSession.builder.appName("CustomerTotalSpentDataFrame").getOrCreate() #boilerplate to create the spark session

#below is code to create the schema, we are supplying name of columns and type 
schema = StructType([ \
    StructField("cust_id", IntegerType(), True), \
    StructField("item_id", IntegerType(), True), \
    StructField("amount_spent", FloatType(), True), \
])

dataFrame = spark.read.schema(schema).csv("file:///c:/users/cenzo/SparkCourse/csv/customer-orders.csv") #with the created schema, load the csv into a dataframe with this created schema

# dataFrame.groupby("cust_id").sum("amount_spent").show() #testing to try to sum the customer's total amount spent while grouping together the same customer ID. THIS WORKS

totalByCusomter = dataFrame.groupby("cust_id")\
    .agg(func.round(\
        func.sum("amount_spent")
        , 2)
    .alias("total_amount_spent")) \
    .sort("total_amount_spent")
    
    #we need to do an aggregate to round. Within the aggregate we also call the sum fcn to get the total amount spent
    #, 2 is for the round function, round to two decimal places
    #alias changes name of column. Sort will sort the results from lowest top to highest bottom. Also with sort, we have to sort by the new column name cant sort by old column name because we are not using old column anymore

totalByCusomter.show(totalByCusomter.count())
#NOTE AFTER SEEING SOLUTION: Good idea to show ALL the rows. Easy way to do that is to save our results into another dataframe and then with the .show() fcn we have to specify in the parameter how many rows to display. Dynamically, we can just put in the dataframe again and use the .count() fcn to get the total row count as how many rows the show fcn should display!

spark.stop() #close session, can not forget this

#LAst recap about dataframes and RDDs. RDDs have their place. If you can think of your problem as a SQL command, DataFrames will make your life easier and is easier for Spark to optimize the whole job and for Spark jobs. 
  