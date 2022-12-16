#Exercise / Lesson 35. My code
# Originally, we used broadcasted variables to display the movie names instead of ID numbers. Here I will create a dataframe to display the most popular movie from the dataset.

from pyspark.sql import SparkSession, functions as func
from pyspark.sql.types import StructType, StructField, IntegerType, LongType

spark = SparkSession.builder.appName("PopularMovies").getOrCreate()

schema = StructType([ \
                     StructField("userID", IntegerType(), True), \
                     StructField("movieID", IntegerType(), True), \
                     StructField("rating", IntegerType(), True), \
                     StructField("timestamp", LongType(), True)])

moviesDF = spark.read.option("sep", "\t").schema(schema).csv("file:///c:/users/cenzo/SparkCourse/ml-100k/u.data")

popularMovies = moviesDF.groupBy("movieId").count().orderBy(func.desc("count"))

lines = spark.read.option("sep", "|").option("inferSchema", "true").text("file:///c:/users/cenzo/sparkcourse/ml-100k/u.item")

# popularMovieNames = moviesDF.withColumn("movieName", lines[0])
# Getting error, need to fix

# trimPopMovie = lines.withColumn("id", func.split(func.trim(func.col("value")), "|"[0])).show() # not printing correctly, may come back.

# popularMovieNames.show()
# lines.show() #NOT BEING INFERRED CORRECTLY INCOMPLETE WILL FIX

spark.stop()