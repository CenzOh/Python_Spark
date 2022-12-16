## Lesson 64 GraphX

Our final lesson. We will take a look at GraphX, another main block that sits on top of Spark Core. 
Graphs such as our social network of superheroes - graphs in the comp sci / network sense. Currently Scala only. Python doesnt appear to support this forthcoming :( Useful for specific things. Would not have helped the degrees of separation example. Can measure things like connectedness, degree of distribution, avg path length, triangle countss - high lvl measures of a graph. Can also join graphs together and transform graphs quick. 
Underhood, introduces VertexRDD and EdgeRDD. Otherwise, GraphX look slike any other Spark code for most part. If job or task focuses on network analysis, this may be helpful and it be worth learnign Scala. 

Spark Book recommendations:
O'Reiley Series, Learning Spark. Snippets and code examples.
Advanced Analytics with Spark. Teaches ML and data mining. Also from O'Reilly press. K Means clustering, Piercing Correlation Metrics. Conversational tone.
Data Algorithms by O'Reilly. Written for Hadoop and map reduce with Spark. Not too much with Spark in that case.