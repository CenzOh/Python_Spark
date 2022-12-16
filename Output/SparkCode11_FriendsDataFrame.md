### Lesson / Exercise 28 and 29, use friends example to create a dataFrame

**PROBLEM:** Revisit the friends by age example but this time, use a dataframe.
ID, name, age, num of friends
0, Will, 33, 385
Find the average number of frineds that each age has.

**TIPS:**
- use the fakefriends-headers csv, already has headers. DONE
- use select("col1", "col2") statement to aquire the columns we need.
- some good data frame fcns to use are avg("colName"), groupBy("colName"), show()
- Look at the spark-sql-dataframe.py file for extra help

First column uses the following code: ```people.groupby("age").avg("friends").show()```
```
(base) C:\Users\cenzo\SparkCourse\MyCode>spark-submit friendsDataFrame.py
+---+------------------+
|age|      avg(friends)|
+---+------------------+
| 31|            267.25|
| 65|             298.2|
| 53|222.85714285714286|
| 34|             245.5|
| 28|             209.1|
| 26|242.05882352941177|
| 27|           228.125|
| 44| 282.1666666666667|
| 22|206.42857142857142|
| 47|233.22222222222223|
| 52| 340.6363636363636|
| 40| 250.8235294117647|
| 20|             165.0|
| 57| 258.8333333333333|
| 54| 278.0769230769231|
| 48|             281.4|
| 19|213.27272727272728|
| 64| 281.3333333333333|
| 41|268.55555555555554|
| 43|230.57142857142858|
+---+------------------+
only showing top 20 rows
```
Next we sort it by age ascending, so 18 is at the top. DO this by addining after .avg, ```.sort("age")```
```
+---+------------------+
|age|      avg(friends)|
+---+------------------+
| 18|           343.375|
| 19|213.27272727272728|
| 20|             165.0|
| 21|           350.875|
| 22|206.42857142857142|
| 23|             246.3|
| 24|             233.8|
| 25|197.45454545454547|
| 26|242.05882352941177|
| 27|           228.125|
| 28|             209.1|
| 29|215.91666666666666|
| 30| 235.8181818181818|
| 31|            267.25|
| 32| 207.9090909090909|
| 33| 325.3333333333333|
| 34|             245.5|
| 35|           211.625|
| 36|             246.6|
| 37|249.33333333333334|
+---+------------------+
only showing top 20 rows
```
Next column we formatted so the column would only have two decimal places, we did this by updating the avg with an aggregate function. Had to include funcitons in the pyspark.sql import. The aggregate fcn is as follows right after groupby: ```.agg(func.round(func.avg("friends"), 2))```
```
+---+----------------------+
|age|round(avg(friends), 2)|
+---+----------------------+
| 18|                343.38|
| 19|                213.27|
| 20|                 165.0|
| 21|                350.88|
| 22|                206.43|
| 23|                 246.3|
| 24|                 233.8|
| 25|                197.45|
| 26|                242.06|
| 27|                228.13|
| 28|                 209.1|
| 29|                215.92|
| 30|                235.82|
| 31|                267.25|
| 32|                207.91|
| 33|                325.33|
| 34|                 245.5|
| 35|                211.63|
| 36|                 246.6|
| 37|                249.33|
+---+----------------------+
only showing top 20 rows
```
Last thing we did was give a differnt column header name with the alias function. This can go right before .sort and inside the aggregate function: ```.alias("avg_num_of_friends")```
```
+---+------------------+
|age|avg_num_of_friends|
+---+------------------+
| 18|            343.38|
| 19|            213.27|
| 20|             165.0|
| 21|            350.88|
| 22|            206.43|
| 23|             246.3|
| 24|             233.8|
| 25|            197.45|
| 26|            242.06|
| 27|            228.13|
| 28|             209.1|
| 29|            215.92|
| 30|            235.82|
| 31|            267.25|
| 32|            207.91|
| 33|            325.33|
| 34|             245.5|
| 35|            211.63|
| 36|             246.6|
| 37|            249.33|
+---+------------------+
only showing top 20 rows
```