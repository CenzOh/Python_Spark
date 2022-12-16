## Lesson 52, Troubleshooting Spark on a Cluster

We will look at tips to troubleshoot or debug Spark on a cluster. This is a dark art. Our Master will run on a console and port `4040`. In EMR it is IMPOSSIBLE to actually connect to it from outside. If we have our own cluster running on our own network, it is much easier.

Okay so we are running on an admin instance of the command prompt and we submit a query with the following comand:
```c:\SparkCourse> spark-submit movie-similarities.py 50```
As ssonn as this starts, we open up a browser, go to `localhost:4040`
This brings us to a web page and we can see Spark Jobs. Displays active job currently running. We can click on that to drill in and see some interesting stuff like an actual visualization of the directed graph as well as a timeline of each stage. We can see what we need to optimize or parition better etc.
We have other tabs like Jobs, Stages, Storage, Enviornment, Executors. Enviornment tells us all the various passing dependencies. Software versions, passive dependencies, etc. Executors shows the individuals executors and we can drill into thread dumps and see whats going on.
Stages tab displays details on each individual stage running.