## Lesson 21 Sort the better word count results

Okay, so we can sort what ``countByValue()`` returns, however, we will stick to RDD's so we can make this very simple. To show what we mean, the following is the **hard way**:

`wordCounts = words.map(lambda x: (x,1)).reduceByKey(lambda x, y: x + y)`

Here we will be converting each word to a key/value pair with a val of 1 and then we count them ALL up with `reduceByKey()`. Stck the results in an RDD instead of just a Python object. We also use a mapper to ``words.mapp`` that converts each individual word and the value of one. Think of the avg number of friends by age. The extra 1 is sued to count up the number of occurrences. \
We then use `reduceByKey` and remember, the keys are the individual words and everytime that word occurs, the 1 gets added in the reduction `lambda x, y: x + y`. 1+1+1... for however many times that word occurrs. 
Same effect as countByValue but this time we store it into a new RDD object. 

Flip the (word, count) pairs to (count, word) pairs, use `sortByKey()` to sort by count (now that count is our NEW key).

`wordCountsSorted = wordCOunts.map(lambda (x,y): (y,x)).sortByKey()`

Again, here we flip it around so we can sort it by number of times it has occurred. 