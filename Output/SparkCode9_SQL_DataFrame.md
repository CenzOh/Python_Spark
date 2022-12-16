### Lesson 26, using Spark SQL and DataFrames

Running our code we are given two sets of results. First is a collect, given from the sql command. Given by Row Objects. **This is a DataFrame.** May have to do extra work to gather exactly what we want out of these values.

The second results are given in this cool tabular format. We did not collect the results we just called show so thats why we did not get the dataFrame back. THis gave us back first 20 rows. We can pass in parameter to display certain amount of rows. We built our dataFrame FROM an RDD. This is one way to do it, other ways to do it as well.

```
(base) C:\Users\cenzo\SparkCourse\MyCode>spark-submit sparkSql.py
Row(ID=21, name="b'Miles'", age=19, numFriends=268)
Row(ID=52, name="b'Beverly'", age=19, numFriends=269)
Row(ID=54, name="b'Brunt'", age=19, numFriends=5)
Row(ID=106, name="b'Beverly'", age=18, numFriends=499)
Row(ID=115, name="b'Dukat'", age=18, numFriends=397)
Row(ID=133, name="b'Quark'", age=19, numFriends=265)
Row(ID=136, name="b'Will'", age=19, numFriends=335)
Row(ID=225, name="b'Elim'", age=19, numFriends=106)
Row(ID=304, name="b'Will'", age=19, numFriends=404)
Row(ID=341, name="b'Data'", age=18, numFriends=326)
Row(ID=366, name="b'Keiko'", age=19, numFriends=119)
Row(ID=373, name="b'Quark'", age=19, numFriends=272)
Row(ID=377, name="b'Beverly'", age=18, numFriends=418)
Row(ID=404, name="b'Kasidy'", age=18, numFriends=24)
Row(ID=409, name="b'Nog'", age=19, numFriends=267)
Row(ID=439, name="b'Data'", age=18, numFriends=417)
Row(ID=444, name="b'Keiko'", age=18, numFriends=472)
Row(ID=492, name="b'Dukat'", age=19, numFriends=36)
Row(ID=494, name="b'Kasidy'", age=18, numFriends=194)
+---+-----+
|age|count|
+---+-----+
| 18|    8|
| 19|   11|
| 20|    5|
| 21|    8|
| 22|    7|
| 23|   10|
| 24|    5|
| 25|   11|
| 26|   17|
| 27|    8|
| 28|   10|
| 29|   12|
| 30|   11|
| 31|    8|
| 32|   11|
| 33|   12|
| 34|    6|
| 35|    8|
| 36|   10|
| 37|    9|
+---+-----+
only showing top 20 rows
```