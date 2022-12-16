## Lesson 35, Display the Movie Names instead of IDs

We will do this from the `u.item` file. 
We can use a DataSet to map the IDs to the names, and then join it with our ratings dataset. HOWEVER, this comes with some unnecessary overhead.
So we could just keep a dictionary loaded in the driver program.
OR, we could let Spark automatically forward it to each executor when we need it. However, what if table size was massive? We would only want to transfer it once to each executor and keep it there.

There is a trick to this, introducing **Broadcast variables and UDFs**
Broadcast objects to executors, such that they are always there whenever needed. SImply use ``sc.broadcast()`` to ship off whatever we want. Then we can use ``.value()` to get our obkect back. We use the broadcast object however we would like, map funcitons, UDFs, anything really.
Remember, **UDF - User Defined Function**

Please now refer to ``popular-movies-nice-dataframe.py`` script in instructorCode folder. Most is same.

```import codecs```

We use this import to load up u.item file locally in driver scirpt before broadcasting it out.

After creating spark session, we do the following:
``` 
nameDict = spark.sparkContext.broadcast(loadMovieNames())
```
Broadcast variables are a function of the spark context (RDD interface instead of Session). 
Now jumping up, here is what the `loadMovieNames()` function does:

```
movieNames = {}
```
first, define a dictionary called movie names.
```
# CHANGE THIS TO THE PATH TO YOUR u.ITEM FILE:
with codecs.open("C:/users/cenzo/SparkCourse/ml-100k/u.ITEM", "r", encoding='ISO-8859-1', errors='ignore') as f:
```
codec.open has a hardcoded path to wher that file resides on our local file system where the driver script is being run. I updated this path to be accurate to my actual path of where u.item is located. `'r'` is read only, the following encoding, ignore errors, and we will refer to it as 'f'.
```
    for line in f:
        fields = line.split('|')
        movieNames[int(fields[0])] = fields[1]
    return movieNames
```
for every line in f, we split based on the pip '|' character, this is based on OUR knowledge of the file format. Then we take the first field [0], assuming this is the movie ID, convert it to an integer which is where the `int(fields[0])` comes in. Assign this to the movie name, which is in the second field [1].
This creates a dictionary of movie names that map integer format movie IDs to string format movie names. Finalyl, return that dictionary from movie names into the broadcast object. Again that is this line:
```
nameDict = spark.sparkContext.broadcast(loadMovieNames())
```
THis broadcasts the dictonary to the entire cluster. SO this dictionary mapping is available ALL across the cluster as needed. We will refer to this cluster as nameDict. NOTE: This is the broadcasted object, NOT the dictionary itself. If we want the dictionary, we would have to retrieve it. We will see how to do it later.
Next up, we create the schema, same concept as before
```
schema = StructType([ \
                     StructField("userID", IntegerType(), True), \
                     StructField("movieID", IntegerType(), True), \
                     StructField("rating", IntegerType(), True), \
                     StructField("timestamp", LongType(), True)])
```
Next up loading the movie data as a dataframe is still unchanged, this is a csv, tab seperated:
```
moviesDF = spark.read.option("sep", "\t").schema(schema).csv("file:///c:/users/cenzo/SparkCourse/ml-100k/u.data")
```
Again like before, we do the `.count()`, group everything by movie id, count them up to see how many times a specific movie appears:
```
movieCounts = moviesDF.groupBy("movieID").count()
```

Okay, now things get interesting. We will create a user defined funciton that will let us lok up movie names from that dictionay from the movie ID.
```
def lookupName(movieID):
    return nameDict.value[movieID]

lookupNameUDF = func.udf(lookupName)
```
the `lookupName` is us defining the function that we want to do. We want to create a new column that ultimately consists of the movie title. To create this column in our dataFrame command, we must create this UDF that will convert a movie ID to a movie name. The fcn takes in a movie ID and returns `nameDict` which is the broadcasted value and gives us back the actual dictionary. Looking up the movie ID in the dictionary will give us back the name associated with that movie ID. 
IMPORTANT: say `.value()` on a broadcasted object to get the actual object back. If we were running this on a distributed cluster, and running on idnividual executor nodes. By broadcasting the dictionary, we would ensure that it was available to every individual executor on every individual node. Furthermore, this was broadcasted ONCE to minimize overhead.

Now apply the user defined function with the following:
```
moviesWithNames = movieCounts.withColumn("movieTitle", lookupNameUDF(func.col("movieID")))
```
Remember, movieCOunts is the dataframe grouped by movieID with the count of how many times it occurred. Append this with `.withColumn()` and name the column 'movieTitle'. Contents will be `lookupNameUDF` which we made that equal to `func.udf(lookupName)`. This is how we convert a Python function into a UDF that we can apply with SparkSQL. So by saying `lookupNameUDF`, we created a UDF that we can apply with Spark SQL. Passin the UDF, within the argument we pass in the contents of the movie ID column. Refer to this with `func.col("movieID")`.
This will pass in whatever is in the movie ID column into the UDF looking for the names and the result goes into the `movieTitle` column.

Next, we order the results with the following: 
```
sortedMoviesWithNames = moviesWithNames.orderBy(func.desc("count"))
```
we are ordering by count in descending order, so we will get our last results which have the highest values at the top. 
FInally, show top ten results with the `.show()` fcn.
sortedMoviesWithNames.show(10, False)

Output:
```
C:\Users\cenzo\SparkCourse\InstructorCode>spark-submit popular-movies-nice-dataframe.py
+-------+-----+-----------------------------+
|movieID|count|movieTitle                   |
+-------+-----+-----------------------------+
|50     |583  |Star Wars (1977)             |
|258    |509  |Contact (1997)               |
|100    |508  |Fargo (1996)                 |
|181    |507  |Return of the Jedi (1983)    |
|294    |485  |Liar Liar (1997)             |
|286    |481  |English Patient, The (1996)  |
|288    |478  |Scream (1996)                |
|1      |452  |Toy Story (1995)             |
|300    |431  |Air Force One (1997)         |
|121    |429  |Independence Day (ID4) (1996)|
+-------+-----+-----------------------------+
only showing top 10 rows
```
So the number one movie is Star Wars.
Quick note: rewriting this to a dataFrame and doing mapping between movie IDs and movie names could result in faster computation of the data. 
Broadcast variables are still an interesting tool to know about.
 