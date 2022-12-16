## Lesson 19, Map vs Flatmap and counting word occurrences exercise.

We will be starting off simple first and work our way up to make the exerciwe more complicated.

**Map()** transforms each element of an RDD into **ONE** NEW ELEMENT. Example:
The quick red 
fox jumped 
over the lazy 
brown dogs =>
`` lines = sc.textFile("redfox.txt")
rageCaps = lines.map(lambda x: x.upper())
``
=> THE QUICK RED 
FOX JUMPED 
OVER THE LAZY 
BROWN DOGS

One to one relationship with map. The lines have been transformed in some way, in this case, it is by uppercasing the letters.

**FlatMap()** in contrast, can create **MANY** NEW ELEMENTS from each one. Example:
The quick red
fox jumped
over the lazy
brown dogs =>
`` lines = sc.textFile("redfox.txt")
words = lines.flatMap(lambda x: x.split())
``
=> The
quick
red
fox
jumped
over
the
lazy
brown
dogs

With flatMap(), we can end up with MORE RDDs than the amount we initially started with. 
Please refer to wordcount.py and word-count.py