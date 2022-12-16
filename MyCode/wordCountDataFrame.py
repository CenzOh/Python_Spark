# Lesson 30, word count with dataframe my code
from pyspark.sql import functions as func, SparkSession  #boilerplate

spark = SparkSession.builder.appName("DataFrameWordCOunt").getOrCreate() #remember spark session so we can use sql interface
input = spark.read.text("file:///c:/users/cenzo/SparkCourse/csv/book.txt")# putting into a dataFrame, remember this is unstructured. How does this work? Dataframe is row objects, each row has one column with the words. Default name is value

#okay now we will do a split using regex to EXTRACT words / individual words

words = input.select(
    func.explode( #explode like flatmap, make multiple rows based on the split op
        func.split(input.value, "\\W+") #regex to extract into individual word based on spaces, puncutation, whatever makes sense.
    ).alias("word")) #change the column name to be word since each row in here will be one word

notEmptyWords = words.filter(words.word != "") #this is filtering out empty strings, we dont want this. Lots of words can be empty text. This helps CLEAN DATA. We ensure all our data has something in it, isNotEmpty

lowercaseWords = notEmptyWords.select( #pulling from the DF that has no empty words and placing inside new DF called lowercaseWords
    func.lower(notEmptyWords.word) #make all the words lowercase. HellO => hello
    .alias("word")) #again give it an alias so we know name of column, but this name already exists so what happens is this new one repalces the original word column

countWords = lowercaseWords.groupBy("word").count() #count the occurances of the words. Using groupby allows us to consolidate and check the occurances of each unique word like before. grouping what is in word column, groups every instance of unique word

countWordsSorted = countWords.sort("count") #sorting by the count variable so highest count will be at bottom (for some reason) and it will go bottom up. To sort alphabetically we will have to input "word" instead of "count"

countWordsSorted.show(countWordsSorted.count()) #showing results. We are passing parameter to show how many rows to show. Default is 20, here we are getting count so we can display ALL THE ROWS
  