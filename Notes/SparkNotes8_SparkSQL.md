## Lesson 25, start of Section 2. Spark SQL, DataFrames, DataSets

**Most important component of Apache SPark** This is important because many people are using dataframes whenever possible instead of RDDs.
Working with structured data. Extends RDD to a DataFrame object. About Dataframes:
Contains Row objects, can run SQL queries, can have a schema (which leads to more efficient storage), can read and write to JSON, Hive, parquet, csv, etc), and communicates with Java / Open Database Connectivity JDBC / ODBC (database APIs), Tableau.

**In other words,** dataframe are big database tables. They are more powerful though. We can do any data analysis job we can think of. Most likely able to express naything we want to do in SQL language. This is powerful since we can take SQL commands and dsitrbiute them across an entire cluster that would be too large to run on a traditional vertically scaled relational database.

**Example of using real Spark SQL code in Python:**
``
from pypsark.sql import SparkSession , Row
spark = SparkSession.builder.appName("SparkSQL").getOrCreate()
inputData = spark.read.json(dataFile)
inputData.createOrReplaceTempView("myStructuredStuff")
myResultDataFrame = spark.sql("SELECT foo FROM bar ORDER BY foobar")
``

Building a Spark session instead of context exposes Spark SQL interface. `.getOrCreate` because we can have a persistant spark session we can reconnect back into. `spark.read.json` easy as that to read the data. `inputData` is a dataframe with a bunch of row objects so we can think of it as that. The database table here is a view and we give it the name of myStructuredStuff. Once setup, just do a SQL command after `spark.sql`, results are another dataframe. Using dataframe is no brainer!!!
Note that we do not have to use the SQL language, we can call methods on the dataframe directly! More code example:
```
myResultDataFrame.show()
myResultDataFrame.select("someFieldName")
myResultDataFrame.filter(myResultDataFrame("someFieldName" > 200))
myResultDataFrame.groupBy(myResultDataFrame("someFieldName")).mean()
myResultDataFrame.rdd().map(mapperFunction)
```
`.select()` will return a new dataframe with just that info you selected. `.show()` displasy the result, can pass in how many rows we want to show. Default is about 10-20. Can convert back to an RDD if we want with `dataframe.rdd`. Can mix and match!

**Dataframes are the new hotness.** Trend in Spark is to use RDDs less and DataFrames more!! DataFames alow for better interoperability, MLLib and Spark Streaming are moving towards using DataFrames instead of RDDs for their primary API. DataFrames simplify development, we can perform most SQL operations on a DataFrame with one line.
Spark Streaming -> Structured Streaming.
MLLib -> Spark.ML
DataFrames are the structure we are using to pass info between different components. DataFrames simplify our development as well.

**DataFrames vs DataSets.** In Spark 2 and beyond, a DataFrame is essentially a DataSet of Row objects. DataSets can wrap known, typed data as well. This is mostly transparent to us in Python since Python is untyped. We do not hae to worry about this with Python. However, in Scala we would prefer to use DataSets whenever possible! Since they are typed, DataSets can be stored more efficiently. They can also be optimized at compile time!
This is one good reason to explore using Spakr with Scala. Maybe I should check this out at some point. Again data that is typed means it can be stored more efficiently and some optimiziation and errors detected at compile time.

**SHell Access**. Spark SQL exposes a JDBC / ODBC server (if we built Spark with Hive support). Start it with `sbin/start-thriftserver.sh`. Listens on port 10000 by default. COnnect using `bin/beeline -u jdbc:hive2://localhost:10000`. We would then have a SQL shell to Spark SQL!! We can also create new tables, or query existing ones that were cached using `hiveCtx.cacheTable("tableName")`.

**User-Defined Functions UDFs**
`
from pyspark.sql.types import IntegerType

def square(x):
    return x*x

spark.udf.register("square", square, IntegerType())
df = spark.sql("SELECT square('someNumericalField') FROM tableName)
`
We can use our UDFs in our SQL commands. Can use them outside direct SQL as well.
Now le us test Spark SQL and DataFrames. We will be using our fake social network data from earlier, query it with SQL and use DataFrames w/o SQL and then we will finally redo our RDD xamples with DataFrames. Please refer to spark.py and spark-sql.py files.