### Lesson 27, more of using Spark SQL DataFrame. 

```
(base) C:\Users\cenzo\SparkCourse\MyCode>spark-submit sparkSqlDataFrame.py
Here is our inferred schema:
root
 |-- userID: integer (nullable = true)
 |-- name: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- friends: integer (nullable = true)
 ```

 First thing we see is the infered schema. We can see how it figured out that our dataframe consists of four columns as well as their type! All based on the different data within the file itself. We can provide our own explicit schema which we will see later. By using Print Schema, we can confirm that yes, it did the right thing.

```
Displaying the name column:
+--------+
|    name|
+--------+
|    Will|
|Jean-Luc|
|    Hugh|
|  Deanna|
|   Quark|
|  Weyoun|
|  Gowron|
|    Will|
|  Jadzia|
|    Hugh|
|     Odo|
|     Ben|
|   Keiko|
|Jean-Luc|
|    Hugh|
|     Rom|
|  Weyoun|
|     Odo|
|Jean-Luc|
|  Geordi|
+--------+
only showing top 20 rows
```

This is having the first twnety names being displayed, only showing the name column.

```
Filter out anyone over 21:
+------+-------+---+-------+
|userID|   name|age|friends|
+------+-------+---+-------+
|    21|  Miles| 19|    268|
|    48|    Nog| 20|      1|
|    52|Beverly| 19|    269|
|    54|  Brunt| 19|      5|
|    60| Geordi| 20|    100|
|    73|  Brunt| 20|    384|
|   106|Beverly| 18|    499|
|   115|  Dukat| 18|    397|
|   133|  Quark| 19|    265|
|   136|   Will| 19|    335|
|   225|   Elim| 19|    106|
|   304|   Will| 19|    404|
|   327| Julian| 20|     63|
|   341|   Data| 18|    326|
|   349| Kasidy| 20|    277|
|   366|  Keiko| 19|    119|
|   373|  Quark| 19|    272|
|   377|Beverly| 18|    418|
|   404| Kasidy| 18|     24|
|   409|    Nog| 19|    267|
+------+-------+---+-------+
only showing top 20 rows
```

Next we filtered out anyone over 21, again, it did this and displays first twenty rows. We can refer to column names within the code.

```
Group by age
+---+-----+
|age|count|
+---+-----+
| 31|    8|
| 65|    5|
| 53|    7|
| 34|    6|
| 28|   10|
| 26|   17|
| 27|    8|
| 44|   12|
| 22|    7|
| 47|    9|
| 52|   11|
| 40|   17|
| 20|    5|
| 57|   12|
| 54|   13|
| 48|   10|
| 19|   11|
| 64|   12|
| 41|    9|
| 43|    7|
+---+-----+
only showing top 20 rows
```

The group by age also works, finding all of the unique age numbers and displaying the total count of records with that specific age.

```
Making everyone 10 years older:
+--------+----------+
|    name|(age + 10)|
+--------+----------+
|    Will|        43|
|Jean-Luc|        36|
|    Hugh|        65|
|  Deanna|        50|
|   Quark|        78|
|  Weyoun|        69|
|  Gowron|        47|
|    Will|        64|
|  Jadzia|        48|
|    Hugh|        37|
|     Odo|        63|
|     Ben|        67|
|   Keiko|        64|
|Jean-Luc|        66|
|    Hugh|        53|
|     Rom|        46|
|  Weyoun|        32|
|     Odo|        45|
|Jean-Luc|        55|
|  Geordi|        70|
+--------+----------+
only showing top 20 rows
```

This whole new column with adding 10 years also worked. This select the existing names in the DataFrames. For context, Will's original age is 33. 