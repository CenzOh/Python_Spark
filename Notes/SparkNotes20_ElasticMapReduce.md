## Lesson 46 Intro to elastic map reduce

We will now deploy our scripts on a cluster rather than local machine. Easiest way to get this up and running is using Amazon's Elastic Map Reduce (EMR). Even though it says map reduce, we can configure this to run a spark cluster and run on top of Hadoop. SUper flexible tool. 

Hadoop is underlying enviornment as cluster manager.

Hadoop YARN - yarn is hadoops cluste manager, spark runs on top of this. 
This service is being served from Amazon, we are essentially renting time in there. THey have big data centers and you are saying 'I want to rent 6-7 different instances of computers to run my cluster across' Instead of buying the computers, you pay by the hour. 

Spark has its own built in standalone cluster manager. We can use that to run on EC2, it has scripts to support this as well. If we will use EC2, may as well use Amazon Web Services (AWS) console applicaiton on the web to launch a smart cluster that is already preconfiged. 

Note that Spark on EMR is not really expensive but not that cheap either. Unlike MapReduce with the `MRJob`, we wull use `m3.xlarge` instances. Prices can add up really quick. Make sure to manually shut down the clusters when finished.

Good idea to ensure that things can run locally on our desktop using a subset of the data first! Remember, we have operations on RDD like `top` and `sample` that we can use to create a smaller sample of a dataset so we can work out the initial kinks or bugs.
  