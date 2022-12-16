## Lesson 53, more troubleshooting tips and managing dependencies.

We will talk about more tips as well as managing code dependencies within spark jobs.
Troubleshooting cluster jobs. Logs, in standalone mode they are in the web UI. In YARN though, the logs are ditributed. We need to collect them after the fact using `yarn logs --applicationID <app ID>`. 
While our driver script runs, it will log errors like executors fialing to issue heartbeats. THis means we are asking too much of an executor. We may need more of them IE - more machines in the cluster. Or maybe each exectuor needs more memory. Another option is to use `partitionBy()` to demand LESS work from individual executors by using smaller partitions.
Just know that nothing Hadoop does can recover from poorly structured code. Whether it be wrong number of partitions, not enough memory, asking too much of each executor. Identify and fix these issues prior to putting the job into production.

Managing Dependencies. Remember that executors are not necessarily on the same box as our driver script. Use broadcast variables to share dat outside of RDD's. If we need a Python package that is not pre-loaded on EMR, set up a step in EMR to run `pip` for what we need on each worker machine. Could also use `--py-files` with `spark-submit` to add individual libraries that are on the master. Avoid using obscure packages that we do not need in the first place. Time is money with our cluster, better off not fiddling with it.
    