## Lesson 51, Similar movies 1 million ratings results

Last time we submitted our query to have our similarities to one million ratings and we will now see the results. 
When finished we can scroll up a little bit and we will see the following:
```INFO DAG Scheduler: Job 7 finished: runJob at PythonRDD.scala:153, took 0.042653 s
Top 10 similar movies for Star Wars: Episode IV - A New Hop (1977)
Star Wars: Episode V - The Empire Strikes Back (1980)   score: 0.98979  strength: 2355
Sanjuro (1962) score 0.98771    strength: 60
Raiders of the Lost Ark (1981)  score: 0.98555  strength: 1972
```
Not going to write all the top 10 results. This is just some of it. First result of Star Wars Episode V makes sense. Sanjuro is an interesting result. Look at strength scores, we can see the Episode 5 had a very strong strength of 2355 common raters. Sanjuro is only based on 60 people. That may sound like a lot but in the context of 1 million ratings, not so much.
Takeaway here is that even though we threw more data at it, that does not necessarily mean the results are better. This may mean we ahve to tune the hyper parameters and in this case, the min strength we are actually enforcing prior to displaying a given result.
Again, more ratings may mean we need to increase min strength parameter as well.
Raiders of the Lost Ark is reasonable and has a good strength score of 14972 common raters. Star Wars Episode VI, makes sense. However, it is strange that Raiders of the Lost Ark came **BEFORE** Star Wars Episode VI. However, Frank thinks it actually does make sense since he feels EPisode VI was the weakest of that trilogy.
Run Silent, Run Deeep is another weird result as well as Laura. Both movies have low strength scores (both under 200). Again, we may just need to filter those out better and raise our min threshold on the number of common raters prior to displaying results and we may see better resutls.
However, this worked! We processed similarities for one million ratings on actual EMR cluster running Spark with 3 nodes, one master and two child nodes.

Finally, remember to shut down the cluster!!!!!!!!!!!!!!!
In the terminal type `exit` to exit. In AWS, click on CLusters, select the `One Million SIm` cluster which should have this big green circle next to it and status is `Waiting CLuster Ready`. Click the check box next to it, then click the termiante method. After a bit it will shut down and we will not be charged anymore. Now there should be an orange unfilled circle and status should say `Terminating User Request`.
    