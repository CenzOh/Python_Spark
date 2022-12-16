# Lesson 27, my code
#this time we will be reading from the CSV with headers already included
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SparkSQL").getOrCreate()

people = spark.read.option("header", "true").option("inferSchema", "true")\
    .csv("file:///C:/Users/cenzo/SparkCourse/CSV/fakefriends-header.csv")

#Before we loaded as an RDD and applied Maps to create a Row object. SInce this csv is structured with header rows or a json object that is structrued, we can simply say Spark.read.option. Not using Spark context at all here!!! Pass in an option sayign we have a header row and to infer the schema. So this tells Spark to take the csv file and figure out the schema based on the data within it.

print("Here is our inferred schema:") #here we call fcns form the dataframe itself. This makes it easier to do some debugging. 
people.printSchema()

print("Displaying the name column:")
people.select("name").show() #new dataFrame with ONLY the name column that has been extracted. select is a function call here, directly on the dataframe. 

print("Filter out anyone over 21:")
people.filter(people.age < 21).show() #filter function, pretty cool syntax, boolean function being passed in and it works. We can do people.age to refer to column names within the code itself. THis is inferred at runtime. 

print("Group by age")
people.groupBy("age").count().show() #groupby aggregates all the people of distinct ages. COunt() will count how many people are within each age. show() will display the results, by default for the first 20. If we want to show more than 20 rows we jsut put the parameter in show: show(50)

print("Making everyone 10 years older:")
people.select(people.name, people.age + 10).show() #creating a whole new constructed column making everyone 10 years older. Again, this is a brand new column we are making. 

spark.stop() #dont forget to stop the session