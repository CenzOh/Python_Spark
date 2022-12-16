## Lesson 59, going over the solution for the Decision Trees in Spark for real estate problem

I wrote some notes in my version. Borrowed a couple aspects from solution. I will give more explanation here about solution code and how it works. 
Import is usual except for this line:
```
from __future__ import print_function
```
This ensures we have backwards compatability with Python 3 and 2 print fcn. Dont really need it. Also this one as well:
```
if __name__ == "__main__":
```
This one will ask the script to NOT run on a different context than just running it as a standalone script. Again, dont really need this but good safeguard.
Afterwards we have our usual boilerplate of creating spark session, app name, 
```
    spark = SparkSession.builder.appName("DecisionTree").getOrCreate()
```
load up the DF, we have header row so load the data directly into DF as opposed to RDD. Use inferschema true to auto figure out the schema, update path if differnt
```
    data = spark.read.option("header", "true").option("inferSchema", "true")\
        .csv("file:///c://users/cenzo/SparkCourse/csv/realestate.csv")
```

Next up, change the data into format the function expects. Easy way is using `VectorAsembler` cant forget the import statement for it (assuming it has been done, but the import statement is): `from pyspark.ml.feature import VectorAssembler`. 
Construct new vector assembler object and now set names of input columns with `.setInputCols`. The input columns are the list of column names. These are our features. The data we will use for our prediction of price of unit area. THe features / col names are house age, distance to transportation, and num of convienent stores.
Then set the output column. This is our label. Call it features. 
```
assembler = VectorAssembler().setInputCols(["HouseAge", "DistanceToMRT", \
                               "NumberConvenienceStores"]).setOutputCol("features")
```

Next up, pass our data with the transform function so that we will construct that vector of feature data with the output column. Select the column `price of unit area`, the thing we are predicting. Second col is `features`, what is in our assembler / the vector of feature data.
```
    df = assembler.transform(data).select("PriceOfUnitArea", "features")
```

Now we can split the data into training in testing data. Optional but can help with some accuracy.
```
    trainTest = df.randomSplit([0.5, 0.5])
    trainingDF = trainTest[0]
    testDF = trainTest[1]
```

Next, construct the decision tree regressor model. Tell it the name of our features column using the function `.setFeaturesCol()`. Also write price of unit area as the label column in the function `.setLabelCol()`. REMEMBER - label is what we are predicting. Features are the attributes we use to make the prediction from.
```
    dtr = DecisionTreeRegressor().setFeaturesCol("features").setLabelCol("PriceOfUnitArea")
```

Once we have the model defined, fit it using the training data. Pass in the training dataFrame, and fit it onto the decision tree regressor.
```
    model = dtr.fit(trainingDF)
```

Now we make the predictions, call the `.transform()` function onto our model, pass in the testing dataset this time. Cache the results, save it to full predictions.
```
    fullPredictions = model.transform(testDF).cache()
```

Now we have a set of predictions for our test data set of what th emodel says the price of unit area SHOULD be given the three input columns.
Extract the predictions and correct labels, and print them out. Do this by converting back to an RDD to make it simplier. Extracting data out of a DF is a bit more complicated. RDDs are a bit easier to deal with on that stand point.
```
    predictions = fullPredictions.select("prediction").rdd.map(lambda x: x[0])
    labels = fullPredictions.select("PriceOfUnitArea").rdd.map(lambda x: x[0])
```

Now to compare them, zip them toegether based on the labels. Finally, iterate and print. Stop session when finished.
```
    predictionAndLabel = predictions.zip(labels).collect()

    for prediction in predictionAndLabel:
      print(prediction)

    spark.stop()
```
So in the real world we would not be printing out the org and pred values. We may compare on a mathematical basis maybe with ML.

Output:
How to read: Prediction | Real value
Overall we have a mixed bag of values. Ex - real value is 61.5 but prediction is 39.47. No where near close. Another example is predicitng 22.79 when real value is 62.9. 
Some were good like predicting 65.0 when actual was 63.3. So obv a lot more goes into predicting the value of a house. 
We can put this into massive dataset across a whole cluster!! Also this decision tree allows us to avoid scaling down our data.
```
C:\Users\cenzo\SparkCourse\MyCode>spark-submit realestateml.py
(37.88947368421052, 7.6)
(18.099999999999998, 12.2)
(19.4, 12.8)
(25.980769230769223, 12.9)
(22.6, 13.2)
(19.4, 13.7)
(25.980769230769223, 14.7)
(11.200000000000003, 15.0)
(18.266666666666666, 15.4)
(22.6, 15.5)
(22.6, 15.6)
(22.6, 17.4)
(19.4, 18.3)
(16.03333333333333, 18.6)
(14.325, 18.8)
(19.4, 19.1)
(25.980769230769223, 20.5)
(25.980769230769223, 20.7)
(25.980769230769223, 20.9)
(24.384615384615383, 20.9)
(25.980769230769223, 21.4)
(31.183333333333334, 22.0)
(22.6, 22.1)
(31.183333333333334, 22.3)
(24.384615384615383, 22.8)
(25.980769230769223, 22.9)
(37.88947368421052, 23.0)
(25.980769230769223, 23.1)
(41.19999999999999, 23.5)
(24.384615384615383, 23.8)
(19.4, 23.8)
(31.183333333333334, 23.9)
(25.980769230769223, 24.4)
(37.88947368421052, 24.5)
(25.980769230769223, 24.6)
(25.980769230769223, 24.8)
(39.94, 25.3)
(19.4, 25.3)
(39.94, 25.5)
(31.183333333333334, 25.6)
(24.384615384615383, 25.6)
(24.384615384615383, 25.7)
(41.685714285714276, 26.5)
(37.88947368421052, 26.5)
(19.4, 26.5)
(19.4, 26.6)
(44.541666666666664, 26.9)
(31.183333333333334, 27.0)
(31.183333333333334, 27.7)
(25.980769230769223, 27.7)
(24.384615384615383, 27.7)
(24.384615384615383, 28.1)
(31.183333333333334, 28.4)
(25.980769230769223, 28.4)
(33.150000000000006, 28.5)
(37.88947368421052, 28.8)
(31.183333333333334, 28.9)
(25.980769230769223, 28.9)
(31.183333333333334, 29.3)
(25.980769230769223, 29.3)
(25.980769230769223, 29.3)
(37.88947368421052, 30.5)
(34.30000000000001, 30.6)
(25.980769230769223, 30.7)
(25.980769230769223, 30.8)
(31.183333333333334, 31.1)
(48.86666666666667, 31.3)
(37.88947368421052, 31.6)
(41.19999999999999, 31.9)
(31.183333333333334, 32.1)
(34.30000000000001, 32.2)
(74.66666666666667, 32.4)
(37.88947368421052, 32.5)
(37.88947368421052, 32.9)
(31.183333333333334, 33.4)
(52.650000000000006, 33.6)
(37.88947368421052, 34.0)
(34.30000000000001, 34.1)
(37.88947368421052, 34.1)
(37.88947368421052, 34.2)
(37.88947368421052, 34.2)
(37.88947368421052, 34.7)
(37.88947368421052, 35.3)
(37.88947368421052, 35.7)
(37.88947368421052, 36.5)
(37.88947368421052, 36.6)
(34.30000000000001, 36.7)
(41.685714285714276, 36.8)
(37.88947368421052, 36.8)
(51.58695652173913, 36.9)
(37.88947368421052, 37.5)
(37.88947368421052, 37.5)
(37.88947368421052, 37.5)
(37.88947368421052, 38.1)
(37.88947368421052, 38.1)
(51.58695652173913, 38.4)
(41.685714285714276, 38.6)
(37.88947368421052, 38.8)
(48.86666666666667, 38.9)
(40.71666666666666, 39.0)
(44.541666666666664, 39.1)
(44.541666666666664, 39.3)
(40.71666666666666, 39.3)
(40.71666666666666, 39.4)
(41.685714285714276, 39.5)
(44.541666666666664, 39.7)
(44.541666666666664, 39.7)
(48.86666666666667, 40.1)
(37.88947368421052, 40.2)
(44.541666666666664, 40.2)
(40.71666666666666, 40.3)
(37.88947368421052, 40.3)
(58.57272727272729, 40.5)
(46.90000000000001, 40.8)
(41.685714285714276, 40.8)
(44.541666666666664, 40.9)
(37.88947368421052, 41.0)
(44.541666666666664, 41.2)
(37.88947368421052, 41.4)
(44.541666666666664, 41.5)
(40.71666666666666, 42.0)
(44.541666666666664, 42.2)
(37.88947368421052, 42.2)
(44.541666666666664, 42.2)
(31.183333333333334, 42.3)
(40.71666666666666, 42.3)
(37.88947368421052, 42.3)
(44.541666666666664, 42.4)
(40.71666666666666, 42.5)
(37.88947368421052, 42.5)
(47.8, 42.7)
(33.150000000000006, 42.9)
(41.685714285714276, 43.1)
(44.541666666666664, 43.4)
(51.58695652173913, 43.5)
(51.58695652173913, 44.0)
(37.88947368421052, 44.2)
(74.66666666666667, 44.3)
(46.90000000000001, 44.8)
(51.58695652173913, 45.1)
(117.5, 45.3)
(51.58695652173913, 45.4)
(40.50000000000001, 45.5)
(44.541666666666664, 46.1)
(37.88947368421052, 46.4)
(25.980769230769223, 46.6)
(37.88947368421052, 46.6)
(44.541666666666664, 46.7)
(40.71666666666666, 46.8)
(37.88947368421052, 47.0)
(44.541666666666664, 47.1)
(48.86666666666667, 47.3)
(44.541666666666664, 47.4)
(40.50000000000001, 47.7)
(31.183333333333334, 48.0)
(44.541666666666664, 48.0)
(44.541666666666664, 48.2)
(44.541666666666664, 48.2)
(37.88947368421052, 48.5)
(51.58695652173913, 48.6)
(44.541666666666664, 49.3)
(46.90000000000001, 49.5)
(58.57272727272729, 49.8)
(51.58695652173913, 50.0)
(33.150000000000006, 50.2)
(37.88947368421052, 50.5)
(58.57272727272729, 50.8)
(44.541666666666664, 51.0)
(44.541666666666664, 51.0)
(51.58695652173913, 51.6)
(52.650000000000006, 51.6)
(58.57272727272729, 51.7)
(51.58695652173913, 51.8)
(51.58695652173913, 52.2)
(51.58695652173913, 52.5)
(51.58695652173913, 52.7)
(44.541666666666664, 53.0)
(44.541666666666664, 53.0)
(51.58695652173913, 53.7)
(40.50000000000001, 53.9)
(51.58695652173913, 54.4)
(58.57272727272729, 54.4)
(40.50000000000001, 55.0)
(44.541666666666664, 55.1)
(51.58695652173913, 55.2)
(37.88947368421052, 55.3)
(44.541666666666664, 55.9)
(51.58695652173913, 56.3)
(46.90000000000001, 57.1)
(51.58695652173913, 57.8)
(51.58695652173913, 58.0)
(51.58695652173913, 58.1)
(58.57272727272729, 58.8)
(44.541666666666664, 59.6)
(58.57272727272729, 61.9)
(51.58695652173913, 62.1)
(51.58695652173913, 62.2)
(58.57272727272729, 63.3)
(74.66666666666667, 63.3)
(51.58695652173913, 63.9)
```