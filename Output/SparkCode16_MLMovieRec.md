### Lesson 56, reviewing output of the ALS ML movie recommendation results

ML - machine learning. ALS - alternating least squares
Originally my output was running into an error. Tried it with User ID 1 and it worked. Also removed my input of user ID 0. SO I found out my error was that for some reason my tabs when I input the data myself became spaces. Here is the data for user 0 in u.data
```
0	50	5	001250949
0	172	5	001250949
0	2	1	001250949
```
Below is output:
```
C:\Users\cenzo\SparkCourse\InstructorCode>spark-submit movie-recommendations-als-dataframe.py 0
C:\Users\cenzo\Anaconda3\lib\site-packages\scipy\__init__.py:138: UserWarning: A NumPy version >=1.16.5 and <1.23.0 is required for this version of SciPy (detected version 1.23.4)
  warnings.warn(f"A NumPy version >={np_minversion} and <{np_maxversion} is required for this version of "
Training recommendation model...
C:\Users\cenzo\Spark\spark-3.2.2-bin-hadoop3.2\python\lib\pyspark.zip\pyspark\sql\context.py:125: FutureWarning: Deprecated in 3.0.0. Use SparkSession.builder.getOrCreate() instead.
Top 10 recommendations for user ID 0
Ruby in Paradise (1993)11.272104263305664
Mina Tannenbaum (1994)10.745755195617676
Braindead (1992)9.688284873962402
Welcome To Sarajevo (1997)9.308385848999023
Bride of Frankenstein (1935)9.113158226013184
Denise Calls Up (1995)8.859633445739746
In the Realm of the Senses (Ai no corrida) (1976)8.766009330749512
Alphaville (1965)8.684003829956055
Warriors of Virtue (1997)8.65075969696045
Angel Baby (1995)8.608258247375488
```
Below I will write hte output from Frank's version:
```
Top 10 movie recommendations for user ID 0
Mina Tannenbaum (1994) 7.26
Pollyana (1960) 6.72
Microcosmos: Le peuple de l'herbe (1996) 6.53
Die xue shuang xiong (Killer, The) (1989) 6.36
Unzipped (1995) 6.25
Shiloh (1997) 6.17
Kansas City (1996) 6.12
Boys (1996) 5.98
Low Down Dirty Shame, A (1994) 5.93
Little Princess, A (1995) 5.86
```

From both of our models, movies in BOTH recommendations was Mina Tannenbaum. Thats it. Scores were different too. Mine says Mina will have recommendation of 10.74 while Frank's says 7.26.
Usure if my version of NumPy matters. When I run it again, I get the same results. Exact. 
Frank comments that he is unfamiliar with ALL of the movies from his result and these recommendations are terrible. What do they have to do with sci fi? Nothing. They could have been chosen at random. What went wrong? The model is very confident that Frank will love Mina Tannenbaum! He says he has not heard of that movie. After looking it up on IMDB, he sees that this movie has nothing to do with sci fi which is what Star Wars is classified as and he liked Star Wars. 
What went wrong?
Algorithm is easy to use, but for our dataset is not producing good results. 
Very sensistive to parameters chosen. Our hyper perameters are not the best. Takes more work to find optimal parameters for a data set than to run the recommendations! We can use the 'train/test' to evaluate various premutations of parameters. What are good recommendations anyway?
Convicned that its not working properlly internally. Putting fiath in a black box is dodgy! Get better results using movie similarity results instead. Find similar movies to movies each user liked. Complicated is NOT always better.
Dont EVER blindly trust results when analyzing big data. Small issues in algorithms become ig issues. Often, quality of input data is teh real issue.
Is possible to measure accuracy of rating predictions if we predict a movie that somebody in the test data set already watched and rated. However, this is hard with recommendor systems because this is what is called a `sparse data problem`. Most movies have not been seen by people so we are unable to evaluate whether our prediction for a movie rating is good in many cases.
Better to start with a qualitative assessment which is what we did. Frank tried different hyperparameters, normalize ratings, anything for better results. Overall, there may be an issue with this internally, potential bug somewhere. 
**Lesson** - putting faith in a black box is a dodgy thing to do. Ensure that using a black box algorithm like Spark ALS implementation, to evaluate the results before putting into production. 
**Lesson 2** - complicated is not always better. Alternating these squares is a fancy algorithm that depends on having more data than we gave it.

Dont let this get you down. Spark ML is very useful. Next exmple is linear regression.