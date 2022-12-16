## Lesson 30, Word COunt using the dataFrame

Trick is to find SQL fcns that do same thing we did with RDDs. Not straihgt forward. Remember that before we read EVERY line from a book, count it up, and count how many times a unique word appears. IE, this is unstructured data.

- ```func.explode()``` - similar to the flatmap in which it explodes cols into rows
- ```func.split()``` - actual split operation, finding individual words 
- ```func.lower()``` - make sure everything is lower case so individual words are not coutned as variations of capitalization
Passing cols as parameters:
   - ```func.split(inputDF.value, "\\W+")``` #refer to dataframe value of that column with df.value.
   - ```filter(wordsDF.word != "")```
   - We can also do ```fnc.col("colName")``` to refer to a column

**DataFrames work best with structured data!!** Using dataFrames with this unstructured text data is not really a great fit. Our initial DataFrame will have row objects with a column named value for each line of text. In this case, RDD would be more straightfoward. Not every problem is a SQL problem.

**Good thing is we can use BOTH**, remember, RDDs can be converted to DataFrames. sometimes it makes sense for us to load the data as an RDD then convert to a DataFrame for further processing later. Vice versa also true. RDD better for map reduce kind of problem!!

Now refer to the ```word-count-better-sortedodataframe.py``` and ```wordCountDataFrame.py``` files