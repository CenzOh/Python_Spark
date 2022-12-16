## Lesson 55 Spark ML to produce movie recommendations

REviewing the file `movie-recommendations-als-dataframe.py`. There is not a lot of code byt ut us applying a sophisticated model called `sophisticating least squares`. THis model does the movie recommendations!! The complexity is hidden from us, using the algorithm is easy. 
Our import is same as usual exxcept for the following line:
```
from pyspark.ml.recommendation import ALS
```
Here we import the ALS module from ML recommendation. We create the Spark session later down per usual. Next up we construct a schema for use in loading up the u.data file. 
```
moviesSchema = StructType([ \
                     StructField("userID", IntegerType(), True), \
                     StructField("movieID", IntegerType(), True), \
                     StructField("rating", IntegerType(), True), \
                     StructField("timestamp", LongType(), True)])
```
We load the u.data file from the ml-100k datasets this is because that file does not have the header row to specify the types. Next, load the movie Name file
```
names = loadMovieNames()
```
This does not do anythign with Spark, it simply uses the sys and codec libraries so we can open the file locally on our system (from where we run the driver script). We want to keep this in memory as a dictionary in Python script. Samll file so this is okay.May do this in real world. Feewer items than people. Not a lot of movies in the world. DOnt distribtue soemthing if you do not have to. DOnt waste resources on the cluster. 
```
def loadMovieNames():
    movieNames = {}
    # CHANGE THIS TO THE PATH TO YOUR u.ITEM FILE:
    with codecs.open("C:/Users/cenzo/SparkCourse/ml-100k/u.ITEM", "r", 
    encoding='ISO-8859-1', errors='ignore') as f:
```
Here we load up the u.item file, specified in character encoding `ISO-8859...` and we want to ignore errors with the encoding as well.
```
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames
```
Next up, iterate through every line in the file, split based on the pipe `|` character and build up the movie names dictionary. Do this by assigning movie IDs to their movie name. Return the resulting dictionary as movieNames. Remember before when we called the `loadMovieNames()` funciton we loaded it into this new variable `names`. 
```
ratings = spark.read.option("sep", "\t").schema(moviesSchema) \
    .csv("file:///C:/Users/cenzo/SparkCourse/ml-100k/u.data")
```
Next up, load up the ratings data. THis is what we call our Big Data. Put this into a dataframe so it can be distributed. Use spark.read to do this, specify that this file is separated by tabs with `\t`. Pass schema in as well. 
```
als = ALS().setMaxIter(5).setRegParam(0.01).setUserCol("userID").setItemCol("movieID") \
    .setRatingCol("rating")
```
This is the meat of recommednations and usign SPakr ML. HEre, we create a new ALS object `(Alternating LEast Squares)`. Remember, ALS is a specific recommendation algorithm. This is the only one that Spark ML afraids so we are a bit limtied in our choice unfortunately. Set the hyper parameters which are `.setMaxIter()` and `.setRegParam()`. Respectfully set these to 5 and 0.01. 
Now we tell it what the names of the User, Item, and Rating columns with `.setUserCol()`, `.setItemCol()`, and `.setRatingCol()`. Remember, we assigned this all the way up in our `Struct Type` and `Struct Fields`. Now load it in. We have an ALS model that knows how to deal with training data. 
```
model = als.fit(ratings)
```
Now we call `.fit()`. In real world, we would want to split this into a training set and a testing set. We saw these in other examples. For now, we will keep it simple and train the model using this. If you want to review the results, you could reserve some of that data for testing purposes and see if you can predict those ratings that peopel actually gave. 
Now we need to get a rpediction from this. THis is actually one of the hardest parts of using this code. What we want to do is construct a dataframe of user IDs that we want to generate recommednations FOR. No simple API here. First thing to figure out is which User ID do we want to get recommendations for. WE will pass that in as a command-line argument to this script.
```
userID = int(sys.argv[1])
```
Extract the argument with `sys.argv[1]` this gets the first parameter that was passed on the command line when we invoked the script. 0 woul dbe the name of the script itself. Next, convert to an integer because User IDs are integers as specified in the cosntruction of the schema. 
Okay, now which user ID should we actually look at? Maybe pick a user that reflect us and our recommendations. Franks hsows us in the `u.data` file that he has modified it to include a user 0 and included some fake ratings. It reads as followed:
```
UserID  movieID rating  timestamp
0       50      5       001250949
0       172     5       001250949
0       2       1       001250949
```
This is the test case. What this data is saying is that user 0 loved Star Wars adn the Empire Strikes back, but hated the movie Gone with the Wind. That is what the movieIDs correspond to. Can look them up in the u.item file. 
We can pretty much say that user 0 likes sci fi movies but doesnt like classic romance. Adding in this fake user 0 we will pass that in as our parameter and see if the prediction analysis makes sense.
NExt up, construct a schema because remember, everything has to be a schema now. 
```
userSchema = StructType([StructField("userID", IntegerType(), True)])
```
Only one field in this structure, simply just the userID. One column in this dataframe that we fabricate for creating recommendations. Next, create a dataframe from that user ID.
```
users = spark.createDataFrame([[userID,]], userSchema)
```
The syntax is a bit strange here but we need to display a list of columns, not one single column. SO our 'list' of columns is `[[userID,]]`. This tricks Spark into thinking this a dataframe we are constructing here. We have a list of rows and within each row we have a list of columns. That explains the double bracket. Then we pass in the `userSchema` to apply that schema to the data as we convert it to a dataframe. THis dataframe consists of a userID column with a single row consisting of the value 0. We pass this into `model.reccomendForUserSubset()` below:
```
recommendations = model.recommendForUserSubset(users, 10).collect()
```
WHat we say here is, I want you to generate recommendations for all the users in this user's dataframe. This has only one user, so we want recommednations for just user 0. The `10` is specifying how many recommendations, so we want 10 recommendatins to be generated. Then we `.collect()` that back to the driver script, so it will essentially take all that back from the cluster and return the final results to our `recommendations` structure. 
Next up, print it out.
```
print("Top 10 recommendations for user ID " + str(userID))
```
Then we iterate through each recommendation that comes back.
```
for userRecs in recommendations:
```
Extract the row.
```
    myRecs = userRecs[1]  #userRecs is (userID, [Row(movieId, rating), Row(movieID, rating)...])
```
`UserRecs` will be in the tuple format of the User ID and a list of row objects associated with that user ID. This consits of a `(movieID, rating)` and so forth.
For every user ID we get back a list of rows for every unique rating prediction for that user ID. Now go through each one of thsoe individual recommendations.
```
    for rec in myRecs: #my Recs is just the column of recs for the user
```
Again, in our case we will get back a single userID row for a user ID 0. Then iterate through each movieID rating tuple row and extract that movieID and that rating from that row. 
```
        movie = rec[0] #For each rec in the list, extract the movie ID and rating
        rating = rec[1]
```
Make this human readable by using that names dictionary from earlier, convert that movie ID into a name and print out the result!
```
        movieName = names[movie]
        print(movieName + str(rating))
```
Print out movie name, print out predicted rating. 
Output in  `SparkCode16` file/
