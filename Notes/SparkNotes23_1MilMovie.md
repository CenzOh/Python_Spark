## Lesson 49, code review for 1 million movie ratings

Refer to python file `MovieSimilarities1M.py`. 
Also downloaded the 1 million movie ratings file from grouplens.org
First thing we do in the script is we name the movie ID the movie name lookup table is now in a file called `movies.dat`. We will ensure that the file exists in the same dierctory as the script when running on the master node of the cluster. We look for the dictionary locally in our directory or redirect asneeded with the `with open()` function.
```
def loadMovieNames():
    movieNames = {}
    with open("movies.dat",  encoding='ascii', errors='ignore') as f:
```
The file itself is limited by a double colon `::` so we will specify that in the `.split()` function. Otherwise same as before.
```
        for line in f:
            fields = line.split("::")
            movieNames[int(fields[0])] = fields[1]
    return movieNames
```
Next change, we are loading the actual ratings from `s3` this is amazon's simple storage service. This is telling Spark to go out to Amaon's S3 service with this S3 URL. The `sundog-spark` is the bucket that our instructor, Frank, ahs created.
```
data = sc.textFile("s3n://sundog-spark/ml-1m/ratings.dat")
```
Next up, change the format of the data file for ratings. It is also dilimited by the double colon.
```
ratings = data.map(lambda l: l.split("::")).map(lambda l: (int(l[0]), (int(l[1]), float(l[2]))))
```
When we create our spark context, note how the `spark conf` object is empty, we are not putting anything in there. We will instead pass the info on the command line. When we run the script on the master. DOing this allows us to take full advantage of some pre configged stuff on the EMR (elastic map reducer) that will auto tell Spark to run on top of Hadoop Yarn off the cluster we created using EMR. 
If we were to keep the master equals local here, it would ONLY run on the master node (which is not what we want). Leaving `SparkCOnf()` empty, it will fall back to the command line argument and the built in config files for Spark taht Amazon auto sets up for us.
```
conf = SparkConf()
sc = SparkContext(conf = conf)
```
Note that because our data is different, the movie ID for Star Wars is 260.