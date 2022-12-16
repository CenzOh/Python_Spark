## Lesson 36 & 37, find the most popular superHero in social graph.

We have two text files. `Marvel-graph.txt` and `marvel-names.txt`.
The way this works is this tells us what superheros appear together within comic books. We will be using the fact that any two superheroes that appear together in the same comic book know each other.
This is like a social network but with comic book superheroes.

Example of input in `marvel-graph.txt`:
4395 2237 1767 ...
3518 5409

Example of input data in `marvel-names.txt`:
5300 "SPENCER, TRACY"
5301 "SPERZEL, ANTON"

In the input data, the `graph.txt` file is a list of numbers which represent the IDs associated with each super hero. The first number in the graph is the super hero we are talking about, then followed by superhero IDs of every superhero that hero has appeared with in other comic books. 
Nitpick detail, a hero may actually span multiple lines. For instance, with spider man who is a popular hero, we may see spider man's ID appearing first on multiple lines.
Our code MUST take this into account. Each super hero ID on a line is not necessarily unique! We may need to combine together multiple lines.
`names.txt` file maps super hero IDs to readable names. Spider man peter parker is 5306 for instance.

TASKS:
- split off hero ID from the beginning of the line so we know which hero we are talking about.
- count how many space-seperated numbers are in the line (we can do this by subtracting one to get the total number of connections. Subtract one to remove the ID of the super hero we are looking for the number of connections. Find out HOW many they are not WHO they are)
- group by hero IDs to add up connections split into multiple lines. Group into single entry
- Sort by total connections.
- Filter the name lookup dataset by the most popular hero ID to look up the name of the most popular hero.

Reviewing the code:
Boilerplate
```
from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.appName("MostPopularSuperhero").getOrCreate()
```
Next we define a schema for the `marvel names` data that maps super hero IDs to names.
```
schema = StructType([ \
                     StructField("id", IntegerType(), True), \
                     StructField("name", StringType(), True)])
```
Two fields, the ID as integer and name as string type.
Next we read in the names using the schema. The seperator is a space not a comma. Read in with spark.read and givne seperator. Names is the dataFrame name.
```
names = spark.read.schema(schema).option("sep", " ").csv("file:///c:/users/cenzo/SparkCourse/csv/Marvel-names.txt")
```
Next we need to load up the `marvel graph` data. This is simply just a bunch of integers. Now, we DO NOT care about the schema here because all we have to do is count up HOW many columns are in each row of data. No need for schema here.
Doing `spark.read.text` is going to take each whole line of the text file and throw it into a single column called value.
```
lines = spark.read.text("file:///c:/users/cenzo/SparkCourse/csv/Marvel-graph.txt")
```
Instead of using schema and looking at this as CSV, we will simply use the SPLIT function to split up into multiple rows. So we create a new `connections` dataFrame and will be composed from the `lines` dataFrame which simply contains all those raw lines of input data. `withColumn()` will let us create a new column called ID. This will be the first column / first number in that line of data. Do this with `func.split` and inside use `func.col("value")` this value column contains that ENTIRE row of info from that `marvel.graph.text` file. SPlit based on spaces and split into individual numbers. Now pull off the VERY first number with `[0]` to extrat the first element in the array of numbers that appear in that row. 

```
connections = lines.withColumn("id", func.split(func.trim(func.col("value")), " ")[0]) \
```
Okay now we create another column using `.withColumn()` and this column is called connections. Again, we will split the value column by spaces and take the size of that and count up how many split results we got after we split up the row by spaces. Again, this will count HOW many individual numbers appear in that row of information. Lastly, we will subtract 1 at the end so that we do not count the very first entry. This is because that first entry is identifying WHO we are talking about on this row. This will give us a count of how many connections are associated with that hero ID with this line of information. 
```
    .withColumn("connections", func.size(func.split(func.trim(func.col("value")), " ")) - 1) \
```
Next, we have to account for the issue of there being multiple lines for a given super hero ID. To do this, simply, we `groupby` the ID and will groupby all the entries by a superhero ID so we can count them all up together. Next, we add `.agg()` because we will apply some function to that aggregated group result. This function will take a sum of the columns and add them together. We will call the result of that operation the connections column again with `.alias()`. This will basically replace the connections column we originaly had with this new column that will have the grand total across multiple lines throughout the data.
```
    .groupBy("id").agg(func.sum("connections").alias("connections"))
```
To find the mos popular super hero, we will take the connections column and `.sort()` by the connections column. We will also add `.desc()` so that the most amount of connections will appear at the top of the sort. Also extracting the number one most popular super hero is done by using `.first()`. 
```
mostPopular = connections.sort(func.col("connections").desc()).first()
```
Now, we need to extrac the name of that super hero. Again, we got back the `mostPopular` which is a dataFrame that contains one row containing the most popular super hero. Now we can take the names dataFrame we created and apply the filter function to extract just the row associated with that superhero ID. So we will check that the ID column and the names DataFrame matches the ID from our most popular result. Do this with `[0]` which represents the FIRST column of that result, this contains the super hero ID. Now we will do `.select("name")` to get back the names DataFrame and call `.first()` to retrieve the one row that we got back from that. 
```
mostPopularName = names.filter(func.col("id") == mostPopular[0]).select("name").first()
```
Finally we print out the results. `[0]` in `mostPopularName` will be the name of the super hero and `[1]` will be the count of occurances. 
```
print(mostPopularName[0] + " is the most popular superhero with " + str(mostPopular[1]) + " co-appearances.")
```
**OUTPUT:**
```
C:\Users\cenzo\SparkCourse\MyCode>cd../

C:\Users\cenzo\SparkCourse>cd instructorcode

C:\Users\cenzo\SparkCourse\InstructorCode>spark-submit most-popular-superhero-dataframe.py

CAPTAIN AMERICA is the most popular superhero with 1933 co-appearances.
```
