### First lesson, in CMD

```
(base) C:\Users\cenzo>cd scripts
The system cannot find the path specified.

(base) C:\Users\cenzo>cd spark

(base) C:\Users\cenzo\Spark>cd spark-3.2.2-bin-hadoop3.2

(base) C:\Users\cenzo\Spark\spark-3.2.2-bin-hadoop3.2>pyspark
Python 3.8.8 (default, Apr 13 2021, 15:08:03) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.2.2
      /_/

Using Python version 3.8.8 (default, Apr 13 2021 15:08:03)
Spark context Web UI available at http://H17NGSFI13P0151.nam.nsroot.net:4040
Spark context available as 'sc' (master = local[*], app id = local-1666289618817).
SparkSession available as 'spark'.
```
***NOTE*** Our first spark program will be working with the README text file. First we will find how many lines are in the file.
```
>>> rdd = sc.textFile("README.md") 
>>> rdd.count()
109
>>> quit()

(base) C:\Users\cenzo\Spark\spark-3.2.2-bin-hadoop3.2>ERROR: The process with PID 26532 (child process of PID 27180) could not be terminated.
Reason: The operation attempted is not supported.
ERROR: The process with PID 27180 (child process of PID 27872) could not be terminated.
Reason: There is no running instance of the task.
SUCCESS: The process with PID 27872 (child process of PID 5192) has been terminated.
```