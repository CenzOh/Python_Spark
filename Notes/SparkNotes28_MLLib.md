## Lesson 54, Introducing Spark's Machine Learning Library

Or Spark.ML or MLLib. We will be using movie recommendations with Spark's machine learning library.

High level of ML capabilities: 
- Feature extraction, term frequency or inverse document frequency is useful for search engine.
- Basic statistics such as chi-squared test, pearson or spearman correlation, min, max, mean, variance.
- linear and logistic regression. Think predicitng a category or true/false thing.
- support vector machines.
- naive bayes classifier. Think spam classifying examples.
- decision trees. Powerful for classification and regression.
- k-menas clustering. Think clustering data together.
- principal component analysis, singular value decomposition. DImensionality reduction techniques.
- recommendation using alternating least squares. This is the one we will be using.

Lots of algorithms outside the box, short of neural networks. A lot of these algorithms were not developed with parrallelization in mind. Spark has come up with some clever ways of distributing these algorithms across an entire cluster. This is very useful.

ML uses dataframes. THe previous API was called `MLLib` and used RDD's and some specialized data structures. THis was depricated in SPark 3, the newer ML library uses dataframes for EVERYTHING. 
This is great because we can create a dataframe and SparkSQL. Or we could do things with it in Spark streaming/structured streaming and pass that into the ML library using the same API. This, overall, allows for more interoperability between the different components of Spark.

For more depth, there is a book from O'Reilly called `Advanced Analytics with Spark`. This gives more of an intro into what these algorithms do. That was written with the original MLLib library and they ahve updated it to the new ML library since then. If you get this, get the second edition.
More examples are provided with Spark SDK itself, providing general guidance on how to use these algorithms. There are a lot of little nuances in how to prepare the data to feed into the models. They are really documented in the examples.

Some recommendations:
```
ratings = spark.read.option("sep", "\t").schema(moviesSchema) \
    .csv("file:///SparkCourse/ml-100k/u.data")

als = 
ALS().setMaxIter(5).setRegParam(0.01).setUserCol("userID").setItemCol("movieID") \
    .setRatingCol("rating")

model = als.fit(ratings)
```
It is that easy. That is the secret of machine learning (ML) in general. A lot of these algorithms are black boxes and simply jsut feed the methods data in the format it expects. Feed it quality data is the hard part. Setting the appropriate knobs and dials on the algorithms (hyper parameters).
In essence, all of these models ahve the same job of applying some sort of learning to a set of data and making predicitions based on that data.
Think of movie recommendations. The above code is the core of this. WHat we do is load up the data set `u.data` 100K ratings. Now pass into the ALS model by simply saying also, `max iterations` and `regulation parameter` are hyper parameters. A lot of the work is in hyper parameter tuning. Simply trial and error. Not good guidance in terms of what to set for the values. People often run the algorithm repeatedly trying out different algorithms until they converge on the set of values that works the best. 
ML is pretty much trial and error. Beyond that, specify the column names with `user IDs`, `ratings`, and `movie IDs`. As long as we have column for those three, pass in as parameters to `set user column`, `set item column`, and finally `set rating column`. This creates a model object we can train. TO do that simply just call `.fit()` on it! Pass in the dataframe as training data and use that model to predict how much a user would like a movie that they ahve not even seen yet. 
  