#Lesson / Exercise 31, min temp with dataframe. My Code
#provide a shcmea to SparkSession.read
#use withColumn()

from pyspark.sql import SparkSession, functions as func
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, FloatType
# importing new stuff, we are using these to create an explicit schema used for loading that DataFrame into a structured data format w/o the benefit of having a header row in the csv file to work with.

spark = SparkSession.builder.appName("minTempDataFrame").getOrCreate() #same as usual

#here we are constructing a structure, pass in a parameter which is a list of stuff (what the square brackets represent [])
schema = StructType([ \
                    StructField("stationID", StringType(), True), \
                    StructField("date", IntegerType(), True), \
                    StructField("type_measure", StringType(), True), \
                    StructField("temp", FloatType(), True)])
# type_measure is what we are measruing, max temp, precipitation, min temp, etc. True means we allow NULL values

df = spark.read.schema(schema).csv("file:///c:/users/cenzo/SparkCourse/csv/1800.csv") # simply here we are reading a schema from the csv and placing it inside a DataFrame. For each column in the file, this schema IS APPLIED
df.printSchema() #allows us to see the schema and ensure we are doing everything correctly. CHECKPOINT COMPLETE

#now we use a filter like in the RDD. Give us ONLY records with TMIN
minTemps = df.filter(df.type_measure == 'TMIN')

#Only columns we want will be the ID and the actual temperature
stationTemps = minTemps.select("stationID", "temp")

#finding min temp for each station with aggregation
minTempsByStation = stationTemps.groupBy("stationID").min("temp") #do groupby on stationID so we get the min temp for the unique station IDs
#.min is getting minimum value observed
minTempsByStation.show() #testing to make sure this works. CHECKPOINT COMPLETE
#NOTE - when creating something in spark to use in produciton, make sure to remove the show fcns and any debugging fcns and steps because having these takes up resources and takes more time for computing.

#turning temp to Fahrenheit instead of C as well as sorting the datasets
stationMinTempF = minTempsByStation.withColumn("temp", #creating a new temperature column that contains the following:
    func.round( #round up by percession which is 2 next to the first set of closing parenthesis.
        func.col("min(temp)") * 0.1 * (9.0 / 5.0) + 32.0, 2))\
        .select("stationID", "temp") \
        .sort("temp") #sort by the temperature value from lowest at top to highest at bottom
        #.select selects only the ID and temp columns to display
        #func.col(min temp) grabs the minimum temp and then we do the caluclation to convert into fahrenheit

#collect the results first
results = stationMinTempF.collect()

#now format it and print it
for result in results:
    print(result[0] + "\t{:.2f}F".format(result[1]))
    #so first we print out the station ID, that is the 0th element
    # Next we format the output to have 2 decimal places (.2f) then outside curly brace we have the letter F to denote Fahrenheit. 1st element is the the actual temp itself and thats it. CHECKPOINT COMPLETE

spark.stop()