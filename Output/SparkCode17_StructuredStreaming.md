### Lesson / Exercise / Activity 61 looking at Structured Streaming in Python

Since I am going over code, I thought it might make more sense to go over the code in the Output folder.
Refer to the file `structured-streaming.py`. The `access_log.txt` file is an actual Apache access log from one of the websites our instructor, Frank, ran.
We will write a script that monitors a directory that has access logs being dumped into it. Could be on real web server. Keep running count of how many status codes appear over time. We can alert if we recieve too many error codes.

First, we import the various packages we need including `SparkContext` and `StreamingContext` from `pyspark.streaming`. We will also import some functions to do regular expressions so we import `regexp_extract`. 
Next up, create the spark session. 
```
spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName("StructuredStreaming").getOrCreate()
```
So we call spark sessions `.builder()`. The `.config()` is only necessary on windows. Ensure the `C:/temp` directory is already created. We call this structured streaming and then we call getOrCreate to create  a new session or reuse an existing one. 
Think of this, if terminated unexpectidly, Spark can recreate the previous session based on the checkpoint.
Next we call `.readStream()`
```
accessLines = spark.readStream.text("logs")
```
This creates a new stream of data coming from the logs directory here on the file system. It looks at the logs direcotry waiting for new files to be dumped into it and will stream the new data as it is found into access lines. 
In development we can say `spark.readStream` and write the same code with static data. Very useful for dev purposes. Can switch from static DF to streaming one. 

Next up, convert into a DF that has the structure we are looking for. This is problematic, right now we have individual lines from the access log and they are super messy to look at. Just look at the `access_log.txt` to see what we are up against. 
Here is an example of the input:
```
66.249.75.159 - - [29/Nov/2015:03:50:05 +0000] "GET /robots.txt HTTP/1.1" 200 55 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
```
Starts pff with an IP address of requestor, time stamp. HTTP request like GET. Status code. 200 means success. Parse these lines into their own structure.  
```
contentSizeExp = r'\s(\d+)$'
statusExp = r'\s(\d{3})\s'
generalExp = r'\"(\S+)\s(\S+)\s*(\S*)\"'
timeExp = r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} -\d{4})]'
hostExp = r'(^\S+\.[\S+\.]+\S+)\s'
```
Explaining what the regex does is a whole other course in itself to explain. The below code essentially will parse out each individual log line and break it up into individual components. 
```
logsDF = accessLines.select(regexp_extract('value', hostExp, 1).alias('host'),
                         regexp_extract('value', timeExp, 1).alias('timestamp'),
                         regexp_extract('value', generalExp, 1).alias('method'),
                         regexp_extract('value', generalExp, 2).alias('endpoint'),
                         regexp_extract('value', generalExp, 3).alias('protocol'),
                         regexp_extract('value', statusExp, 1).cast('integer').alias('status'),
                         regexp_extract('value', contentSizeExp, 1).cast('integer').alias('content_size'))
```
So by saying `accessLines.select` we are saying to use the regex patterns a few lines above to match patterns in the access log line to extract the hosts, timestamp, the method, the endpoint, the protocol, the status code, and the content size based on the aptterns defined. 
We know what it is extracting INTO via the alias. We know what pattern to look for with the `Exp` variables. SO for example, the first one the column name is `host` and we will be looking for the `hostExp` pattern there.
As we do this we generate a new DF `logsDF` that contain all of these methods aliases as column names. At this point, we can refer to this DF as we would with any other DF.
What is the difference? Well, because it is streaming, we are appending new info to it over time continuously. 
Now that we have it, group that DF by the status code and keep it running.
```
statusCountsDF = logsDF.groupBy(logsDF.status).count()
```
With one line of code we said keep track of everything by status code with the `group By` command and count them up over time. Very SQL style format. If we wanted to, we could simply make that a SQL command.
Now that we told it what to do, simply kick it off with the following: 
```
query = ( statusCountsDF.writeStream.outputMode("complete").format("console").queryName("counts").start() )
```
We say, take that `statusCountsDF` that we have defined, call `writeStream` to dump the results somewhere. In this case, we dump the complete output defined by `.outputMode()` to the console as defiend by `.format()`. We will query a name called counts with the `.query()` function. Finally, kick this off with `.start()`.
THis will start our structured streaming application where we have this `statusCOuntsDF` that keeps epxanding and changing over time based on waht status codes that it sees coming. Run it forever until termination is detected. 
```
query.awaitTermination()
```
At that point of termination, we have to shut down the Spark session:
```
spark.stop()
```
TESTING IF THIS WORKS: GO to command prompt and do our usual command. However, note that make sure we have a log structure in the directory so it can be monitored, otherwise the code wont work. In the course materials I added a new logs folder `SparkCourse/logs`. Nothing is in it as of now. After we do the initial run, paste a copy of the `access_log.txt` file into the log folder.
Once it picks up, we should see the following:
```
C:\Users\cenzo\SparkCourse\InstructorCode>spark-submit structured-streaming.py
------------------------------
Batch: 0
------------------------------
+------+-----+
|status|count|
+------+-----+
|   500|10714|
|   301|  271|
|   400|    2|
|   404|   26|
|   200|64971|
|   304|   92|
|   302|    2|
|   405|    1|
+------+-----+
```
QUICK NOTE, mine was not working, running into an error. Unsure why will attempt to debug.
First batch of info shows a lot of 500s so something is going wrong here. There is about 10k of info there. We can get FURTHER data and show that it is streaming.
To do this, We renamed `access_log.txt` to something else (I made another copy). THis new copy has the name `access_log_1.txt`. We put that file into the `logs` folder. 
We expect the counts to double. The terminal is still monitorign the folder so it should be thinking 'hey I found new info come into this directory'. It will process it and after some time, everything is doubled what it was so we see: ALSO NOTE - we did NOT rerun the terminal. The terminal was still going / still running
```
------------------------------
Batch: 1
------------------------------
+------+------+
|status| count|
+------+------+
|   500| 21428|
|   301|   542|
|   400|     4|
|   404|    52|
|   200|129942|
|   304|   184|
|   302|     4|
|   405|     2|
+------+------+
```
We have this giant DF keeping track of all the info coming in, distilling it down to the count DF that keeps track of status codes and how often they occur.
Easy, clean API. This is a handy reference as the SDK does not have a spark streming example for some reason.
In terminal, when finished hit CTRL C to termiante. 