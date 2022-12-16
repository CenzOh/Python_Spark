### Lesson / Exercise 31, Min temp with DataFrame and custom schema

```
(base) C:\Users\cenzo\SparkCourse\MyCode>spark-submit minTempDataFrame.py
root
 |-- stationID: string (nullable = true)
 |-- date: integer (nullable = true)
 |-- type_measure: string (nullable = true)
 |-- temp: float (nullable = true)
```
Above is result from creating our schema and printing it out
```
+-----------+---------+
|  stationID|min(temp)|
+-----------+---------+
|ITE00100554|   -148.0|
|EZE00100082|   -135.0|
+-----------+---------+
```
NExt this table is after  the group by and finding min temp so we only have min temp for each unique station ID
```
ITE00100554     5.36F
EZE00100082     7.70F
```
Finally we created a new column for the temp, converted it to Fahrenheit as well as formatted it to have 2 decimal palces with F next to the values.