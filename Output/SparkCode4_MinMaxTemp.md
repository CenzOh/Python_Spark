### Lesson 17, Running min temp example
```
(base) C:\Users\cenzo>cd sparkcourse

(base) C:\Users\cenzo\SparkCourse>cd mycode

(base) C:\Users\cenzo\SparkCourse\MyCode>spark-submit minTemp.py
ITE00100554     5.36F
EZE00100082     7.70F
```

### New task, do the same idea but this time find the MAX TEMP instead of MIN TEMP
First I will make a new file called max temp just so I can still keep min temp.
All we had to do was change the fcn looking for TMIN to be TMAX and change the min() fcn that grabs the absolute min value for each station ID to be a max() fcn instead.

```
(base) C:\Users\cenzo\SparkCourse\MyCode>spark-submit maxTemp.py
ITE00100554     90.14F
EZE00100082     90.14
```