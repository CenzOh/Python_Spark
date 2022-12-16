# Lesson 26 my code
from pyspark.sql import SparkSession #import spark sql with session and row
from pyspark.sql import Row #both of these thigns we use to itneract with SparkSQL and dataFrames

spark = SparkSession.builder.appName("SparkSQL").getOrCreate() #the get or create again, creating a new spark session or connect to one from a previous one

def mapper(line):
    fields = line.split(',')
    return Row(ID = int(fields[0]), #going in order to create the rows. First field or 0th element is ID, etc.
                name = str(fields[1].encode("utf-8")), \
                age = int(fields[2]), 
                numFriends = int(fields[3]))

lines = spark.sparkContext.textFile("../CSV/fakefriends.csv") #note that this csv does NOT ahve headers so it may make it difficult to structure the data. We still have SparkCOntext availabel under spark session. Creates RDD named lines.
# Also quick note, original code said textFile("fakefriends.csv") this still has the path problem so I had to update it to go to the director with the csv files
people = lines.map(mapper) #map every row from the incoming lines. Need rows first before creating a DataFrame. 

schemaPeople = spark.createDataFrame(people).cache() #we first infer the schema. Passing in people RDD and converting into dataframe. Keep this in memory thats why we cache it
schemaPeople.createOrReplaceTempView("people") #register the DataFrame as a table. Existing view then it would be replaced. Can use this like a database table

teenagers = spark.sql("SELECT * FROM people WHERE age >= 13 AND age <= 19")
#SQL can be run over DataFrames that have been registered as a table ^^^. Teenagers is a dataFrame!! Also the names map back to the names we gave them when we constructed the Row object. 

for teen in teenagers.collect(): #results of SQL queries are RDDs and supprot all the normal RDD operations
    print(teen) #this is a simple collect and print 

schemaPeople.groupBy("age").count().orderBy("age").show() #can also use fcns rather than SQL queries. We can do either fcns or SQL commands!

spark.stop() #kinda like opening and closing a database. good practice to close if we do not use. Stop when done.