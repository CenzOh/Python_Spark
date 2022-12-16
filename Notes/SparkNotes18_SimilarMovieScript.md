## Lesson / Exercise 45, imrpove the quality of the Similar Movies DataFrame script.

Improve the results! We are using a very naive algorithm here wih the cosine similarity metric. The results are not bad, they can be better. 

Here are some pointers:
- Discard the bad ratings. Remember, in the `u.data` we have user ratings. Ex, if someone rates somethign ONE STAR will that really be useful for our purposes? prob not. Maybe we can see that bad movies are similar to each other but do you really want to recommend bad movies to people? So try to filter out the bad ratings.
- We can try different similarity metrics. There are many such as Pearson Correlation Coefficient, Jaccard Coefficient, Conditional Probaility. We can replace the cosine metric with and see what we get. Some may be better or worse. 
- We can also adjust the thresholds for min co-raters or min score. Maybe we are not being picky enough.
- Maybe we should invent our own similarity metric that can take the number of co-raters into account. Maybe we do not need the minimum threhold or the min co-raters. Maybe we can take that into account as part of the actual similarity itself and automatically account how much confidence we have in that relationship. 
- DOn't forget, we have the u.items folder in the movieLens dataset that contains things like genre info so it might be interesting to extract that info and give a boost to movies that are in the same genre! Ex - similarities to Star Wars that are science fiction maybe should count a little bit more.

REFRESH ON THE DATA:
`u.data` columns are as follows:
`user id | item id | rating | timestamp`
Also note that there are a total of 100K ratings by 943 users on 1682 different movies. Each user rated AT LEAST 20 movies.
`u.item` columns are as follows:
`movie id | movie title | release date | video release date | IMDb URL | unknown | Action | Adventure | Animation | Children's | Comedy | Crime | Documentary | Drama | Fantasy | Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi | Thriller | War | Western |`
The last 19 columns are the genres. A 1 indicates that movie is of that genre while a 0 indicates it is not. Movies can be in multiple genres. 
Link both tables togehter with `movieID` in `u.item` and `itemID` in `u.data`.


First try, attempted to discard bad ratings. In the function, will ONLy account for ratings that are 4 or 5 / 5. In file `movieSimilaritiesRatings.py` 
```
C:\Users\cenzo\SparkCourse\MyCode>spark-submit moviesimilaritiesratings.py 50
Top 10 similar movies for Star Wars (1977)
Tomorrow Never Dies (1997)      score: 0.9938502871716387       strength: 55
Empire Strikes Back, The (1980) score: 0.9938388064391904       strength: 274
Broken Arrow (1996)     score: 0.993800492219264        strength: 62
Return of the Jedi (1983)       score: 0.9937254331649558       strength: 349
E.T. the Extra-Terrestrial (1982)       score: 0.9936147177559697       strength: 162
Kingpin (1996)  score: 0.9935701614503102       strength: 56
Wrong Trousers, The (1993)      score: 0.9934729807580136       strength: 82
Jackie Chan's First Strike (1996)       score: 0.9931981416725884       strength: 56
Star Trek VI: The Undiscovered Country (1991)   score: 0.9931761357951461       strength: 67
Raiders of the Lost Ark (1981)  score: 0.9930935451237883       strength: 293
```
Results seem to be better. Strength is NOT as high since we are getting more picky. But ALL the scores are 0.99. I didn't even change the score thresholds.  
      