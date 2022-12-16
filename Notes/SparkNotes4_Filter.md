## Lesson 16. Filterting RDDs and using Weather Data

Stripping RDDs down into what we care about by making smaller RDDs. This filter() function removes data from our RDD, takes a function, returns a boolean.
EX - filter out entries that DO NOT have TMIN in the first item in the data list. DO the following to filter that out:

``minTemps = parsedLines.filter(lambda x: "TMIN" in x[1])``

We are doing this to gather results that DO HAVE minimum temperatures, this is what we are looking for.

Example source data snippet, min temp in a year:
ITE00, 180001, TMAX, -75,,,E,
ITE00, 180001, TMIN, -148,,,E,
GM000, 180001, PRCP, 0,,,E,
EZE00, 180001, TMAX, -86,,,E,
EZE00, 180001, TMIN, -135,,,E,

So what we want is to include that that ONLY has TMIN within the dataset. Looking for smallest temp in that year. Please refer to mintemp.py and min-temperatures.py to parse / map the input data.
 