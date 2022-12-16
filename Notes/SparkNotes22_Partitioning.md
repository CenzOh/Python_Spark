## Lesson 48, Partitioning

We will be attempting to scale up our movie similarity example with one million ratings. We simply can not run this as is. We have to think how the data will be partitioned, must address this in our script. 
Think about how your data is partitioned, Spark will not auto do this for us.
Running as is will not work because the self-join is quite expensive, Spark will NOT distribute it on its own.
We can use `partitionBY()` on an RDD before running a large scale operation that benefits from paritioning. This tells you how many pieces you want to break this job up into.
Other helpful RDD methods: `join()`, `cogroup()`, `groupWith()`, `Join()`, `leftOuterJoin()`, `rightOuterJoin()`, `gorupByKey()`, `reduceByKey()`, `combineByKey()`, and `lookup()` 
These ops will also preserve our paritioning within their result.

How do we choose a partition size? Too few partitions will not take full advantage of my cluster and too many results in too much overhead from shuffling data.
We need to have as many partition as we have `cores` or `executors` that fit within our available memory. Ex - `partitionBy(100)` is usually a good place to start for large operations. 
    