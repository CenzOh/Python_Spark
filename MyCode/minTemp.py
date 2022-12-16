# Lesson 16 My version with comments

#boilerplate
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MinTemperatures")
sc = SparkContext(conf = conf)

def parseLine(line): #Similar to last one, we will parse / map the input data
    fields = line.split(',') #csv file we split rows and cols with commas
    stationID = fields[0] #grab the very first element, element 0 which is the ID field, ITE00.
    entryType = fields[2] #This grabs the THIRD element including TMIN, TMAX, etc.
    temperature = float(fields[3]) * 0.1 * (9.0 / 5.0) + 32.0 #next we calcualte the temperature into Farhenheit with the formula
    # extract numerical field which is index 3, 4th col using fields[3] and cast it to be a floating point number.
    return (stationID, entryType, temperature) #return composite value, or a list which contains these three values.

lines = sc.textFile("file:///C:/Users/CENZO/SparkCourse/CSV/1800.csv") #file to read from. Lines is our new RDD. Load every line here

parsedLines = lines.map(parseLine) #apply the mapping function
#again, output will be (stationID, entryType, temperature)

minTemps = parsedLines.filter(lambda x: "TMIN" in x[1]) #apply the filter to ONLY include TMIN. we do this on index 1 / element 2 because remember, in the new parsedLines RDD the columns read as ID, entryType, Temperature. We will still have ID and temperature, its just that we are including records that ONLY INCLUDE TMIN in entrytype.

stationTemps = minTemps.map(lambda x: (x[0], x[2])) #okay now that we have all the TMIN records, we do not need to display the entry column since they will ALL say TMIN. SO here we do a new map that combines the 0th and 2nd element which are ID and temperature in degrees F. This is a key value pair!!!

minTemps = stationTemps.reduceByKey(lambda x, y: min(x,y)) #finally, we want to find the lowest temperature of the year. Do this by calling reduceByKey. Aggregate every min temp together by station ID. We then call the min() fcn to take the minimum value between these two.
# we will end up with ONE entry for every stationID and that ONE entry will be the absolute lowest temp of that station ID.

results = minTemps.collect() #finally call the collect action so Spark can do something.

for result in results:
    print(result[0] + "\t{:.2f}F".format(result[1])) #iterate and print through Python list. THis format will print the station ID then have a tab and ensure the temp is truncated two decimal points and add F for Fahrenheit.
    