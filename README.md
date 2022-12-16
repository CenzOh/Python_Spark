# Follow along #
Following Udemy course on Spark with Python and using PySpark technologies:
https://cglearning.udemy.com/course/taming-big-data-with-apache-spark-hands-on/learn/lecture/3708614#questions/5471550

# Topics I leanred #
- Python, JDK, Spark, Dependency installation
- RDDs (Resilient Distributed Datasets) and subtypes such as Key Value Pairs
- Flat Maps
- SparkSQL functions and commands
- DataFrames, DataSets and Schemas
- Degrees of Separation
- Accumulators, Spark version of Breadth First Search algorithm
- CLuster manager, running Spark on a Cluster
- Machine Learning with SparkML, Linear REgression, and Decision Trees
- SPark Streaming

## Setup Instructions: Using Windows enviornment ##

### Python enviornment: ###
We will be using Anaconda, simply go to Anaconda site and download latest version: 
https://www.anaconda.com/
We will also be using **Python 3** with the Anaconda package. 

### JDK: ###
**Must use JDK 1.8**. https://www.oracle.com/java/technologies/downloads/archive/ Tutorial uses JDK version 1.8u131, can use that version if anything.

**Important about the installer:** Should NOT place the JDK file in a location with white space ' ' since the JDK will be unable to read the file. 
In the JDK setup menu, click the **'change'** button to change the location of hte JDK folder. Default may say `'C:\Program Files'` This is NOT good. Can place the JDK folder in its own folder in C drive such as: `'C:\JDK\`' or under user such as: `'C:\Users\user\JDK'`.

### Spark: ###
Can do `'pip install pyspark'` and `'pip install spark'` in the terminal / CMD. Also can download the PySpark on the website: https://spark.apache.org/downloads.html You CAN use the latest version of Spark, I however recommend to use the version in the video which is Spark 2.1.1. You can use the latest version.
Similarly place the Spark folder either in C drive or in user folder and avoid whitespaces in the Path name.

**Note:** In Spark folder, and then in the `conf` subfolder, rename the file `'log4j.properties.tempalte'` file to **remove** the tempalte portion so it would look like: `'log4j.properties'`.
Now, inside that file, open the file in a text editor. Go to the line that displays `'log4j.rootCategory=INFO'` and change this to `'=ERROR'`. If you DO NOT see this, you might instead see something called `'rootLogger.level'` so you can alter this property instead. We do this so we do not have to see all of the text print out in the console for an error I believe. 

### Winutils: ###
Next we need a `winutils.exe` file. We can obtain this with the following link: https://sundog-spark.s3.amazonaws.com/winutils.exe We will put this in its own folder, `'C:\winutils\bin'`. Insert the winutils.exe **INSIDE THE BIN**. We use this file if we do not have Hive downloaded. This is for purposes of testing Spark / PySpark on local host projects NOT in development environment. 

**Command Prompt:**
write the following: 
```
mkdir C:\tmp\hive
cd c:\winutils\bin
dir
winutils.exe chmod 777 \tmp\hive
```

### Edit the Paths: ###
Two ways to find this:
1: Windows button > type control pannel > select it > select system and security > select system, select system settings > select enviornment variables.
2: Windows button > type run > press enter > type in `rundll32.sysdm.cpl` > EditEnviornmentVariables.

Now for the enviornment variables, for the variables in user click new. `Name = SPARK_HOME`, `value = C:\Spark`. The value is the path where the BIN folders are for each of these technologies. So if you have Spark in the user folder you would set value as `C:\Users\user\spark`. 

DO the same for Java; `Name = JAVA_HOME`, `value = C:\java`

For Hadoop, the path is where the winutils file is. `Name = HADOOP_HOME`, `value = C:\winutils`

Since we are using Spark 3 we also have to set the variable for pyspark. For me, I set it to where my pthon is located in Anaconda. `Name = PYSPARK_PYTHON`, `value = C:\Users\user\Anaconda3\python.exe`

Finally, update the PATH variable itself. Select it > click Edit... and a new window should pop up named Edit Enviornment Variables. Now select New so we can add new paths. Add the following Paths:
```
%SPARK_HOME$\bin
%JAVA_HOME%\bin
C:\Users\user\Anaconda3\bin
```