## Lesson 34, Find Most Popular Movie

Will be reviewing Instructor Code named ``popular-movies-dataframe.py``. THis exercvise simply will allow us to find the most popular movies using a dataframe.

The CSV we will be reading from u.data from the ml-100k folder. 
THe info from this csv has the following columns:
User ID, Movie ID, Rating, Timestamp
196 242 3 881250949

How do we find the most popular movie? Simply we will count up what movie has THE MOST ratings. We can also assume if you rated a movie, you have seen the movie.

In our script, its pretty straightforward. We have the boilerplate code
```
from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.types import StructType, StructField, IntegerType, LongType

spark = SparkSession.builder.appName("PopularMovies").getOrCreate()
```
Then we create the schema defining our column names and types since this csv DOES NOT have header rows:
```
schema = StructType([ \
                     StructField("userID", IntegerType(), True), \
                     StructField("movieID", IntegerType(), True), \
                     StructField("rating", IntegerType(), True), \
                     StructField("timestamp", LongType(), True)])
```
After that we load up the dataframe:
```
moviesDF = spark.read.option("sep", "\t").schema(schema).csv("file:///c:/users/cenzo/SparkCourse/ml-100k/u.data")
```
Take note that this file is NOT comma seperated, it is tab seperated. We must tell Spark this by using the `read.option()` fcn and specify that it is seperated, first parameter is `"sep"`, by tabs with `"\t"` in the second parameter. Then we put `.schema()` to apply the schema we defined above.

We do not even need most of the information in here, again, we are looking for the movie with the most ratings as our answer of most popular movie. We do nto care what ratings people give it. Doesn't matter when it was made or who gave it. So for us to count up how many reviews are for each movie in this data set, we simply do `groupBy()` to group all the differnet ratings for each unique movie id. Then we do `.count()` to count how many times each movie ID appears in the dataset. To find out most popular, we will also include `orderBy()` and pass in `func.desc("count")` which means we want to do the ordering using the descendign fcn based on the count column.
```
topMovieIDs = moviesDF.groupBy("movieID").count().orderBy(func.desc("count"))
```

Now we want to grab the top 10 most rated movies by specifying how many to show in the `show()` fcn. Just write 10 in the param
```
topMovieIDs.show(10)
```
Finally, cant forget to stop the Spark program
```
spark.stop()
```
Results:
```
C:\Users\cenzo\SparkCourse\MyCode>cd ../

C:\Users\cenzo\SparkCourse>cd instructorcode

C:\Users\cenzo\SparkCourse\InstructorCode>spark-submit popular-movies-dataframe.py
+-------+-----+
|movieID|count|
+-------+-----+
|     50|  583|
|    258|  509|
|    100|  508|
|    181|  507|
|    294|  485|
|    286|  481|
|    288|  478|
|      1|  452|
|    300|  431|
|    121|  429|
+-------+-----+
only showing top 10 rows
```
So far this is great. Thing is, what is Movie ID 50? We will be building on this example.