## Lesson 20, improve word count with Regular expressions (regex)

We will be normalizing the data and sorting the results!
So to recap, our issue is that the book text file has word variants with different capitalization and puncutation. Our first word count python script has not accounted for this.
There are fancy natural language processing tools such as NLTK but we will keep it simple and use **regular expressions**.

This is not really Spark specific, already available for Python.

``return re.compile(r'\W+', re.UNICODE).split(text.lower())``
What this does is, we set up a regular expression (the re at the beginning). Regex is pretty much a language on its own for text processing, its a string that defines how to split up a string into other values and transform it.
We then call re.compile. ``r'\W+'`` means we want this text to be broken up based on words. ``W+`` means break it up on words. Regex will strip things not part of words. UNICODE will ensure the no errors issue that we also addresses with word.encode. `text.lower()` will transform all of the words to be lower case. So for instance: HellO => hello.
