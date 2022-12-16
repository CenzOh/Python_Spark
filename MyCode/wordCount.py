#Lesson 19 my version of the code
#boilerplate
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("WordCount")
sc = SparkContext(conf = conf)

input = sc.textFile("file:///C:/Users/cenzo/SparkCourse/CSV/Book.txt")
#one paragraph per line, lots of words per line

words = input.flatMap(lambda x: x.split())
#here we use the flatmap fcn that takes every individual line of text and breaks it up based on whitespace into individual words and then we place all of that into an RDD

wordCounts = words.countByValue()
#coutnByValue easily gets a count of how many time each unique word occurs (seperated by white space) result stored in wordCounts.

for word, count in wordCounts.items(): #iterate through all words
    cleanWord = word.encode('ascii', 'ignore') #fixes encoding issues and display everything okay by converting to ascii format and ignore any conversion errors. For instance fix the word if we have special characters.
    if (cleanWord):
        # print(cleanWord, count) #again here we print out the unique words and how many times they occur
        #note that since we split based on WORDS we get weird 'words' like click" and webpage, punctuation should not count.
        #idea is combine words together doesnt matter aout capitilization or puncutaiton. 
        print(cleanWord.decode() + " " + str(count)) #this version looks better, first version for some reason is formatted strange
    