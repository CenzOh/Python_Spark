#Lesson Exercise 45, improve the quality of Similar Movies script
# original script is movie-similarities-dataframe.py
# Objective: Second, I want to now only show movies of same genre as the input
from pyspark.sql import SparkSession, functions as func
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, Row, BooleanType
import sys

#Step 2, find the genre(s) of the movie and lets just print out for now

# Get movie name by given movie id 
def getMovieName(movieNames, movieId):
    result = movieNames.filter(func.col("movieID") == movieId) \
        .select("movieTitle").collect()[0]

    return result[0]


spark = SparkSession.builder.appName("MovieSimilarities").master("local[*]").getOrCreate()

movieNamesSchema = StructType([ \
                               StructField("movieID", IntegerType(), True), \
                               StructField("movieTitle", StringType(), True) \
                               ])
genreSchema = StructType([ \
                               StructField("genreName", StringType(), True), \
                               StructField("genreIndex", IntegerType(), True) \
                               ])                              

# def mapper(line):
#     fields = line.split('|')
#     return Row(ID = int(fields[0]),
#                 genreArray = [[fields]] 
#     )
    
# Create a broadcast dataset of movieID and movieTitle.
# Apply ISO-885901 charset
movieNames = spark.read \
      .option("sep", "|") \
      .option("charset", "ISO-8859-1") \
      .schema(movieNamesSchema) \
      .csv("file:///c:/users/cenzo/SparkCourse/ml-100k/u.item")

genre = spark.read \
      .option("sep", "|") \
      .option("charset", "ISO-8859-1") \
      .schema(genreSchema) \
      .csv("file:///c:/users/cenzo/SparkCourse/ml-100k/u.genre")

input = spark.read \
        .option("sep", "|") \
      .option("charset", "ISO-8859-1") \
      .csv("file:///c:/users/cenzo/SparkCourse/ml-100k/u.item")

#   Currnet input, trying to see how we can make all the genres into some form of array so we can map it to the genre name? WIll come back to
# UNFINISHED WILL COME BACK TO

# _c0|                 _c1|        _c2| _c3|                 _c4|_c5|_c6|_c7|_c8|_c9|_c10|_c11|_c12|_c13|_c14|_c15|_c16|_c17|_c18|_c19|_c20|_c21|_c22|_c23|
# +---+--------------------+-----------+----+--------------------+---+---+---+---+---+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
# |  1|    Toy Story (1995)|01-Jan-1995|null|http://us.imdb.co...|  0|  0|  0|  1|  1|   1|   0|   0|   0|   0|   0|   0|   0|   0|   0|   0|   0|   0|   0|
# movieAndGenre = input.select(
#     func.explode(
#         input
#     )
# )
# input.show()

if (len(sys.argv) > 1):


    movieID = int(sys.argv[1])

    
    print ("The movie name is " + getMovieName(movieNames, movieID))
    movieNames.show()
    
    # for result in results:
    #     # Display the similarity result that isn't the movie we're looking at
    #     similarMovieID = result.movie1
    #     if (similarMovieID == movieID):
    #       similarMovieID = result.movie2
        
    #     print(getMovieName(movieNames, similarMovieID) + "\tscore: " \
    #           + str(result.score) + "\tstrength: " + str(result.numPairs))
        
