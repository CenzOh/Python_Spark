#Lesson 21 my version of the code
import re #regular expression import
from pyspark import SparkConf, SparkContext
def normalizeWords(text): #defining our normalize words function
    return re.compile(r'\W+', re.UNICODE).split(text.lower())

conf = SparkConf().setMaster("local").setAppName("BetterWordCOuntSorted")
sc = SparkContext(conf = conf)

input = sc.textFile("file:///C:/Users/cenzo/sparkCourse/CSV/book.txt")
words = input.flatMap(normalizeWords)

#change is below. 
wordCount = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
# so first, we are going to do a mapper where we transform every word into a key value pair of the word and the number one and then in reduce by key, we add them all up. Add up every instance.

wordCountSorted = wordCount.map(lambda x: (x[1], x[0])).sortByKey()
#wordCount.map(lambda (x,y): (y,x)).sortByKey() # this did not work becuase y is undefined
# in the above, we want to switch it around so that the num of occurrances are the keys, or in the first column, and the actual word itself is the value, in the second column. After the flip, we sort by key to get a sorted list of how many times each word occurrs.

results = wordCountSorted.collect()

for result in results:
    count = str(result[0]) #remember, the first index in the result (which is from the sorted word count) is the number of occurrances.
    word = result[1].encode('ascii', 'ignore') #same as before where we encode the word 
    if(word):
        print(word.decode() + ":\t\t" + count)
        #output format simply is taking the word, adding a few tabs, then lisitng the number of occurances. 
