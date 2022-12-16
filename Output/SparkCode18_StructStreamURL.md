### Lesson 63, Going over output of struct stream python code

Refer to python files `structStreamURL.py` and `top-urls.py` based on `structured-streaming.py`.

Regex part is pretty much the same so let us skip ahead.
First thing that our instructor, Frank, has did was create this new column called `Event TIme`. It is equal to the `current_timestamp()`. Will be populated with the time at which this data was ingested. Wouldnt have to do this in real world since we are using old access logs. 
```
logsDF2 = logsDF.withColumn("eventTime", func.current_timestamp())
```

Rememebr we want 30 second window with 10 second slide interval. Set this up in the `.window()` function. First paraemeter is which column to look for, that is `eventTime`. Then second parameter is the window (30 seconds), and the third parameter is the slide interval (10 seconds). Also recall that endpoint is our column with URLs. FInally get the `count` .
```
endpointCounts = logsDF2.groupBy(func.window(func.col("eventTime"), \
      "30 seconds", "10 seconds"), func.col("endpoint")).count()
```

Next up is to sort it. Use the `orderBy()` function and select the count column with the `func.col()` function. Then display the stream 
```
sortedEndpointCounts = endpointCounts.orderBy(func.col("count").desc())
```

Now display the stream to the console with `.outputMode("complete")` and `.format("console")`, etc. The query is called counts and then this kicks off. Will start streaming and run forever until we stop the script.
```
query = sortedEndpointCounts.writeStream.outputMode("complete").format("console") \
      .queryName("counts").start()
```
To recap, new query named Counts. Runs forever until we stop it. Writes to stream in `complete .outputMode()` to the console the results of `sortedEndpointCounts`.
In real world we wouldnt write to console we could do something with this output such as saving it. Maybe instead of console, format as text file to save on file system or save it to a DB. Look at apache documentation for `writeStream()`  to see where we could write this stuff to!

Run forvever until we stop it.
```
query.awaitTermination()
spark.stop()
```

Output: Mine wasnt working so I typed an example of what it would look like
```
C:\Users\cenzo\SparkCourse\InstructorCode>spark-submit top-urls.py

+--------------------+-------------+-----+
|[2020-09-14 16:10...|  /xmlrpc.php|68494|
|[2020-09-14 16:10...|  /xmlrpc.php|68494|
|[2020-09-14 16:10...|  /xmlrpc.php|68494|
|[2020-09-14 16:10...|  /xmlrpc.php|68494|
|[2020-09-14 16:10...|  /xmlrpc.php|68494|
|[2020-09-14 16:10...|  /xmlrpc.php|68494|
|[2020-09-14 16:10...|/wp-login.php| 1923|
|[2020-09-14 16:10...|/wp-login.php| 1923|
|[2020-09-14 16:10...|/wp-login.php| 1923|
|[2020-09-14 16:10...|/wp-login.php| 1923|
|[2020-09-14 16:10...|/wp-login.php| 1923|
|[2020-09-14 16:10...|/wp-login.php| 1923|
+--------------------+-------------+-----+
```
Just a snippet. Can also try to copy and paste that file so we can double our stream input and see double results like last time. Gives top URLs for EACH WINDOW. `/xmlrpc.php` and `wp` are the most that was being hit. According to Frank, at this time someone was trying to hack into his website and break into the site with a hacking vulnerability and WordPRess. They didnt do it but slowed down his website by hitting it this hard. 
This is a real world example where this sort of analysis in real time can alrert us or help diagnose what is going on!