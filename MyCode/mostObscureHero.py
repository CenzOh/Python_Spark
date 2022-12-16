# Lesson 38, Find most Obscure Super heros
# List the names of ALL superheros with only ONE connection. - DONE
# BONUS: compute the ACTUAL smallest number of connections in the data set INSTEAD of assuming it is one. - DONE

#QUICK NOTE - I did not read the strategy prior to tackling the problem. I will write it out anyway:
# - Start witha copy of the script, most-popular-superhero-dataset.py
# - Pretty much largely unchanged. Only really up to the point where the connections dataFrame is constructed.
# - filter the connections to find rows with ONE connection
# - join results with the names dataFrame
# - select names column, show it
# Code snippets:
# dataframename.filter(func.col("columnname") == somevalue)
# dataframename.join(someOtherDataFrameWithACommonCOlumnName, "commonColumnName")
# agg(func.min("columnName")).first()[0]

#boilerplate
from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

#same as what was done in most popular super hero
spark = SparkSession.builder.appName("MostObscureSuperhero").getOrCreate()

schema = StructType([ \
                     StructField("id", IntegerType(), True), \
                     StructField("name", StringType(), True)])

names = spark.read.schema(schema).option("sep", " ").csv("file:///c:/users/cenzo/SparkCourse/csv/Marvel-names.txt")

lines = spark.read.text("file:///c:/users/cenzo/SparkCourse/csv/Marvel-graph.txt")

connections = lines.withColumn("id", func.split(func.trim(func.col("value")), " ")[0]) \
    .withColumn("connections", func.size(func.split(func.trim(func.col("value")), " ")) - 1) \
    .groupBy("id").agg(func.sum("connections").alias("connections"))

#Okay now grab the connections by least number. note that we must grab MORE THAN ONE obscure so using .last will not really help us.
mostObscure = connections.sort(func.col("connections"))#.show() #will print out ID and number of connections from least amount. 
# 2139 0
# 4364 1
# What I needed was the .join based on the names dataFrame with ID field! It was that easy.
mostObscureNames = mostObscure.join(names,"id") \
    .sort("connections") \
    .filter(func.col("connections") == 1) \
    .show(mostObscure.count())
# the join allows us to have the names and number of connections
# the filter makes it so we ONLY see the connections equal to 1. If we wanted to see the absolute lowest, we could make it equal to mostObscure which show us multiple connections equal to 0
# to show ALL the names, in the .show() function, and inside reference the mostObscure dataFrame .count() to get the number of rows in that DataFrame so we will just display all the rows in this new filtered dataFrame.

# *** reviewing solution to help me with my solution ***
# lowConnectCount = connections.agg(func.min("connections")).first()[0] #min fcn, finds the absolute lowest value litterally prints:
# min(connections)
# 0 
# print(lowConnectCount) #litterally prints 0 when adding .first()[0] to above
# minConnections = connections.filter(func.col("connections") == lowConnectCount)#.show()
#displays dataFrame with the super heros with 0 connections only. Seems like the filter says "WHERE connections == 0"