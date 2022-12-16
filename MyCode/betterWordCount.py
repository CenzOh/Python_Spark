#Lesson 20 my version of the code

import re #regular expression import
from pyspark import SparkConf, SparkContext
def normalizeWords(text): #defining our normalize words function
    return re.compile(r'\W+', re.UNICODE).split(text.lower())
# what this does is, we set up a regular expression (the re at the beginning). Regex is pretty much a language on its own for text processing, its a string that defines how to split up a string into other values and transform it.
#we then call re.compile. r'\W+' means we want this text to be broken up based on words. W+ means break it up on words. Regex will strip things not part of words. UNICODE will ensure the no errors issue that we also addresses with word.encode. tetx.lower() will transform all of the words to be lower case. So for instance: HellO => hello.

conf = SparkConf().setMaster("local").setAppName("BetterWordCOunt")
sc = SparkContext(conf = conf)

input = sc.textFile("file:///C:/Users/cenzo/sparkCourse/CSV/book.txt")
words = input.flatMap(normalizeWords)
wordCount = words.countByValue()

for word, count in wordCount.items():
    cleanWord = word.encode('ascii', 'ignore')
    if(cleanWord):
       print(cleanWord.decode() + " " + str(count))