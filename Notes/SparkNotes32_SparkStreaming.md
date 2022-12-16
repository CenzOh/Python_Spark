## Lesson 60, Spark Streaming. 
We will talk about other notable spark subsystems like `spark streaming` and `graph x`. Recall that we already talked about `spark core` and `AML lib` and `Spark SQ`L. These last two are built on top of spark core!

`Spark Streaming` - used to analyze continues streams of data. Ex - processing log data from website or server. Data is aggregated and analyzed at some given interval. Can take data fed to some port, think Amazon Kinesis, HDFS, Kafka, Flume, and others. Checkpointing stores tate to disk every so oftern for fault tolerance.
Data not alwasy just sitting there! Monitor in real time or near real time. Maybe keep watch of this code and look for error code. Can deal with low level TCP port or any specific system. Can take results to another stream or database or whatever we would like to do. 

How to do Spark Streaming. A `Dstream` object breaks up the stream into distinct RDDs. Idea is stream is broken up into distintive RDDs. Micro batches, not really real time. Deal with little chunks at a time. Ex:
```
sc = StreamingContext(sc,1)
lines = ssc.textFileStream("books")
counts = lines.flatMap(lambda line: line.split(" ")).map(lambda x: (x,1)) \
    .reduceByKey(lambda a, b: a + b)
counts.pprint()
```
This code looks for text files dropped into the `books` dictionary and counts up how often each word appears over time and updates every one second. Assuming we are dealing with one RDD. One second of data goes into an RDD. Looking for new data into the books dictionary.
Kick the job off explicitly with:
```
scc.start()
ssc.awaitTermination()
```
So we tell it when to start adn stop. Again Dstream is close to real time streaming.

Note - the RDDs contain one little chunk of incoming data. `Windowed operations` can combine results from multiple batches over some sliding time window. `.window()`, `.reduceByWindow()`, `.reduceByKeyAndWindow()`. Over sliding window, say 'past hour'.
`.updateStateByKey()` lets us maintain a state across many batches as time goes on. Think running counts of some event. Refer to `stateful_network_worcount.py` example in SDK. (Spark Development Kit (?)). Ex - keep count of some event or total num of lines processed since beginning of stream, use the update state by key fcn.

NEW WAY - `Structured Streaming`. Models streaming as a DF that keeps expanding. Python support is quite recent for this. Streaming code ends up looking like non-streaming code. DF provide interoperability with MLLib. 
Data Stream -> Unbounded Table. Data stream as an unbounded input table. New data in stream = new rows appended to input table!!
Can start off with static DF and very slight modification to use streaming data.