# exercise 58 my code
# Predict real estate values with decision trees in spark
# the CSV is named `realestate.csv`, real data from Taiwan
# Number,TransactionDate,HouseAge,DistanceToMRT,NumberConvenienceStores,Latitude,Longitude,PriceOfUnitArea
# MRT is transportation terminal. 
# Price per unit area is based on the price sold for

# Objective: 
# Predict the price per unit area based on 
# house age, 
# distance to MRT (public transportation), 
# and num of nearby convenience stores

# Strategy: 
# Use a `DecisionTreeRegressor` instead of LinearRegression. Decision trees can handle data in different scales well
# Start with copy of `spark-linear-regression.py`
# We have header row so dont need to hard code the schema.

# Snippet help:
# Multiple input columns in VectorAssembler
# assembler = VectorAssembler().setInputCols(["col1", "col2",...])
# df = assembler.transform(data).select("labelColumnName", "features")
# .option("header", "true").option("inferSchema", "true")
# DecisionTreeREgresso, can do w/o hyperparameters
# .setLabelCol() specifies a label column (what we are predicting) if its name is NOT 'label'

from __future__ import print_function

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder.appName("DecisionTree").getOrCreate() #boilerplate

    # inputLines = spark.sparkContext.textFile("../csv/realestate.csv") #input file
    realestate = spark.read.option("sep", ",") \
        .option("header", "true") \
        .option("inferschema", "true") \
        .csv("../csv/realestate.csv") #input file
    # realestate.show() #test to see if input worked
#     | No|TransactionDate|HouseAge|DistanceToMRT|NumberConvenienceStores|Latitude|Longitude|PriceOfUnitArea|
# +---+---------------+--------+-------------+-----------------------+--------+---------+---------------+
# |  1|       2012.917|      32|     84.87882|                     10|24.98298|121.54024|           37.9|
# |  2|       2012.917|    19.5|     306.5947|                      9|24.98034|121.53951|           42.2|

    assembler = VectorAssembler().setInputCols(["HouseAge", "DistanceToMRT", "NumberConvenienceStores"]).setOutputCol("features") #here we use the VectorAssembler and select our input columns. Read prompt for our INPUT. set output col changes the name of our output col which we use next. Again output col is the combo of everything in input col
    df = assembler.transform(realestate).select("PriceOfUnitArea", "features") #here we transfrom into new DF. First column is the actual price, what we are comparing to. Second column has an inner DF of [house age, distance to public trans, and num of convience stores]

    # df.show() #another test case
#     |PriceOfUnitArea|            features|
# +---------------+--------------------+
# |           37.9|[32.0,84.87882,10.0]|
# |           42.2| [19.5,306.5947,9.0]

    trainTest = df.randomSplit([0.5, 0.5]) #split data, half training set, half testing set
    trainingDF = trainTest[0] #half to training
    testDF = trainTest[1] #other half to testing

    dec = DecisionTreeRegressor().setFeaturesCol("features").setLabelCol("PriceOfUnitArea") #will leave out hyper parameters for now. Set the label column up here, not on the model object interestingly. Label is what we are predicting, price of unit area. Also set the features col to our inner DF col with the three params
    model = dec.fit(trainingDF) #train the model with training set

    fullPredictions = model.transform(testDF).cache() #generate predictions in test training data using decision tree model

    predictions = fullPredictions.select("prediction").rdd.map(lambda x: x[0])
    labels = fullPredictions.select("PriceOfUnitArea").rdd.map(lambda x: x[0])
    #extract predictions and known labels. Known are correct labels

    predictLabel = predictions.zip(labels).collect() # zip both together

    for prediction in predictLabel: #print 
        print(prediction)

    # fullPredictions.show() #wasnt able to use show method

    spark.stop()
# Output, also for help:
# Prediction | Actual Price of Unit Area
# (37.88947368421052, 7.6)
# (18.099999999999998, 12.2)
# (19.4, 12.8)
# (25.980769230769223, 12.9)
# (22.6, 13.2)
# (19.4, 13.7)
# (25.980769230769223, 14.7)
# (11.200000000000003, 15.0)
# (18.266666666666666, 15.4)
# (22.6, 15.5)
# (22.6, 15.6)
# (22.6, 17.4)
# (19.4, 18.3)
# (16.03333333333333, 18.6)
# (14.325, 18.8)
# (19.4, 19.1)
# (25.980769230769223, 20.5)
# (25.980769230769223, 20.7)
# (25.980769230769223, 20.9)
# (24.384615384615383, 20.9)
# (25.980769230769223, 21.4)
# (31.183333333333334, 22.0)
# (22.6, 22.1)
# (31.183333333333334, 22.3)
# (24.384615384615383, 22.8)
# (25.980769230769223, 22.9)
# (37.88947368421052, 23.0)
# (25.980769230769223, 23.1)
# (41.19999999999999, 23.5)
# (24.384615384615383, 23.8)
# (19.4, 23.8)
# (31.183333333333334, 23.9)
# (25.980769230769223, 24.4)
# (37.88947368421052, 24.5)
# (25.980769230769223, 24.6)
# (25.980769230769223, 24.8)
# (39.94, 25.3)
# (19.4, 25.3)
# (39.94, 25.5)
# (31.183333333333334, 25.6)
# (24.384615384615383, 25.6)
# (24.384615384615383, 25.7)
# (41.685714285714276, 26.5)
# (37.88947368421052, 26.5)
# (19.4, 26.5)
# (19.4, 26.6)
# (44.541666666666664, 26.9)
# (31.183333333333334, 27.0)
# (31.183333333333334, 27.7)
# (25.980769230769223, 27.7)
# (24.384615384615383, 27.7)
# (24.384615384615383, 28.1)
# (31.183333333333334, 28.4)
# (25.980769230769223, 28.4)
# (33.150000000000006, 28.5)
# (37.88947368421052, 28.8)
# (31.183333333333334, 28.9)
# (25.980769230769223, 28.9)
# (31.183333333333334, 29.3)
# (25.980769230769223, 29.3)
# (25.980769230769223, 29.3)
# (37.88947368421052, 30.5)
# (34.30000000000001, 30.6)
# (25.980769230769223, 30.7)
# (25.980769230769223, 30.8)
# (31.183333333333334, 31.1)
# (48.86666666666667, 31.3)
# (37.88947368421052, 31.6)
# (41.19999999999999, 31.9)
# (31.183333333333334, 32.1)
# (34.30000000000001, 32.2)
# (74.66666666666667, 32.4)
# (37.88947368421052, 32.5)
# (37.88947368421052, 32.9)
# (31.183333333333334, 33.4)
# (52.650000000000006, 33.6)
# (37.88947368421052, 34.0)
# (34.30000000000001, 34.1)
# (37.88947368421052, 34.1)
# (37.88947368421052, 34.2)
# (37.88947368421052, 34.2)
# (37.88947368421052, 34.7)
# (37.88947368421052, 35.3)
# (37.88947368421052, 35.7)
# (37.88947368421052, 36.5)
# (37.88947368421052, 36.6)
# (34.30000000000001, 36.7)
# (41.685714285714276, 36.8)
# (37.88947368421052, 36.8)
# (51.58695652173913, 36.9)
# (37.88947368421052, 37.5)
# (37.88947368421052, 37.5)
# (37.88947368421052, 37.5)
# (37.88947368421052, 38.1)
# (37.88947368421052, 38.1)
# (51.58695652173913, 38.4)
# (41.685714285714276, 38.6)
# (37.88947368421052, 38.8)
# (48.86666666666667, 38.9)
# (40.71666666666666, 39.0)
# (44.541666666666664, 39.1)
# (44.541666666666664, 39.3)
# (40.71666666666666, 39.3)
# (40.71666666666666, 39.4)
# (41.685714285714276, 39.5)
# (44.541666666666664, 39.7)
# (44.541666666666664, 39.7)
# (48.86666666666667, 40.1)
# (37.88947368421052, 40.2)
# (44.541666666666664, 40.2)
# (40.71666666666666, 40.3)
# (37.88947368421052, 40.3)
# (58.57272727272729, 40.5)
# (46.90000000000001, 40.8)
# (41.685714285714276, 40.8)
# (44.541666666666664, 40.9)
# (37.88947368421052, 41.0)
# (44.541666666666664, 41.2)
# (37.88947368421052, 41.4)
# (44.541666666666664, 41.5)
# (40.71666666666666, 42.0)
# (44.541666666666664, 42.2)
# (37.88947368421052, 42.2)
# (44.541666666666664, 42.2)
# (31.183333333333334, 42.3)
# (40.71666666666666, 42.3)
# (37.88947368421052, 42.3)
# (44.541666666666664, 42.4)
# (40.71666666666666, 42.5)
# (37.88947368421052, 42.5)
# (47.8, 42.7)
# (33.150000000000006, 42.9)
# (41.685714285714276, 43.1)
# (44.541666666666664, 43.4)
# (51.58695652173913, 43.5)
# (51.58695652173913, 44.0)
# (37.88947368421052, 44.2)
# (74.66666666666667, 44.3)
# (46.90000000000001, 44.8)
# (51.58695652173913, 45.1)
# (117.5, 45.3)
# (51.58695652173913, 45.4)
# (40.50000000000001, 45.5)
# (44.541666666666664, 46.1)
# (37.88947368421052, 46.4)
# (25.980769230769223, 46.6)
# (37.88947368421052, 46.6)
# (44.541666666666664, 46.7)
# (40.71666666666666, 46.8)
# (37.88947368421052, 47.0)
# (44.541666666666664, 47.1)
# (48.86666666666667, 47.3)
# (44.541666666666664, 47.4)
# (40.50000000000001, 47.7)
# (31.183333333333334, 48.0)
# (44.541666666666664, 48.0)
# (44.541666666666664, 48.2)
# (44.541666666666664, 48.2)
# (37.88947368421052, 48.5)
# (51.58695652173913, 48.6)
# (44.541666666666664, 49.3)
# (46.90000000000001, 49.5)
# (58.57272727272729, 49.8)
# (51.58695652173913, 50.0)
# (33.150000000000006, 50.2)
# (37.88947368421052, 50.5)
# (58.57272727272729, 50.8)
# (44.541666666666664, 51.0)
# (44.541666666666664, 51.0)
# (51.58695652173913, 51.6)
# (52.650000000000006, 51.6)
# (58.57272727272729, 51.7)
# (51.58695652173913, 51.8)
# (51.58695652173913, 52.2)
# (51.58695652173913, 52.5)
# (51.58695652173913, 52.7)
# (44.541666666666664, 53.0)
# (44.541666666666664, 53.0)
# (51.58695652173913, 53.7)
# (40.50000000000001, 53.9)
# (51.58695652173913, 54.4)
# (58.57272727272729, 54.4)
# (40.50000000000001, 55.0)
# (44.541666666666664, 55.1)
# (51.58695652173913, 55.2)
# (37.88947368421052, 55.3)
# (44.541666666666664, 55.9)
# (51.58695652173913, 56.3)
# (46.90000000000001, 57.1)
# (51.58695652173913, 57.8)
# (51.58695652173913, 58.0)
# (51.58695652173913, 58.1)
# (58.57272727272729, 58.8)
# (44.541666666666664, 59.6)
# (58.57272727272729, 61.9)
# (51.58695652173913, 62.1)
# (51.58695652173913, 62.2)
# (58.57272727272729, 63.3)
# (74.66666666666667, 63.3)
# (51.58695652173913, 63.9)