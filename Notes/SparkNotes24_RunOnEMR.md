## Lesson 50, running on the 1m movie ratings on the EMR

Specify memory per executor.
Just use an empty, defualt `SparkConf` on our driver. THis way, we can use the defaults EMR sets up instead, as well as any command-line options we pass into `spark-submit` from our master node. 
In our example, the default executor memory budget of 512MB is insufficient for processing one mill movie ratings. Instead, we have to do the following:
`spark-submit --executor-memory 1g MovieSimilarities1M.py 260` (from the master node of our cluster).
Whether we actually need to change `--executor-memory` will depend on the version of SPark and the hardware we choose. Possible for us to get lucky and not need to do this.
Again, passing in `executor memory 1g` means pass in 1 gigabyte of memory per executor since the defualt memory of 512 megabytes per executor will not suffice. This will also be broken up into 100 partitions for the self join.

Some other options we can pass in as well as `--master yarn` to run a YARN cluster but EMR will set this up automatically. If we run on our own cluster, we may need to pass that in by hand.

Running on a cluster, we want to grab our scripts and data and place them where EMR can easily access them. AWS's S3 is a good choiuce, simply use `s3n://` URL's when specifying file paths and ensure the file permissions make them accessible.
Spin up an EMR cluster for SPark using the AWS console, note that this is wehn the billing starts for us!!
Grab the external DNS name for the master node and log into it using 'Hadoop' user account and the private key file from a couple lessons ago. Ex - using `AWS S3 CP S3://bucket-name/filename ./` 
Run `spark-submit` and wathc the output.
When finished, TERMINATE THE CLUSTER!! Can not forget.

Looking at the example, the 1 million similarities python file has been copied to a Spark bucket on Amazon's S3 service so the Spark cluster can access it. The script itself has also been copued onto the `/sundog-spark/` S3 bucket. After we spin up the cluster, first thing to do is to call the script to copy the movie similarities python file from S3 to the master node.

`aws s3 cp s3://sundog-spark/MovieSimilarities1M.py ./`

Next step is to copy over the `movies.dat` file that will be used to load up and create the movie ID to movie name lookup table that will be used in the final output. 

`aws s3 cp s3://sundog-spark/ml-1m/movies.dat ./`

Last step is what to actually run to execute this job. We want to find similarities to Star Wars and in this dataset, Star Wars is ID 260.

`spark-submit --executor-memory lg MovieSimilarities1M.py 260`

Login to AWS console on the website, click on EMR or search for EMR and then click on it. Next, create a new cluster. Give it a name such as `One Million Sims`. Select the Spark application. In the video it says `Spark: Spark 2.4.7 on Hadoop 2.10.1 YARN and Zeppelin 0.9.0`. Change the instance type to `m3.xlarge`. We can get away with one instance, however, that defeats the purpose of having a cluster. CHange the number of instances to 3 so we can see how this runs across multiple computers. No need for auto scaling or anything fancy so you can leave the other boxes unchecked. 
Select the EC2 keypair to yours which may be named `SundogEC2`. If you need to create a new one, instrucitons are in the link to the right of the drop down menu. Finally, click the blue button on the bottom right to Create the CLuster.

Now simply wait for it to provision, may take several minutes. You will see a `Starting` message at the top indicating that it is starting and not ready to go yet. About 10 minutes later, Frank's cluster is up and running, we can see a `Waiting` message at the top.

Connect to master node: Under `Master public DNS` on the top right, select the link that says `Connect to Master Node using SSH`. Some instructions are given to us. If we have the terminal program PuTTY installed we can click on the link which contains more instructions. Remember that you will need the private key file that we downloaded earlier. Using PuTTY there is an added step of using PuTTY Gen program to convert the key we downlaoded to the PPK format.

Now we need to copy the link in step 4 to the master node. It is an actual external IP address. The example has the following link: `hadoop@ec2-18-207-245-compute-1-amazonaws.com`. Launch PuTTY. Where it says `Host Name (or IP Address)` paste this link in there. Next on the left side, click on the **SSH** drop down menu, go to **Auth**, click the Browse button to select the private key. Find the file path for the private key. Again the name of the key mught be `SundogEC2.ppk`. Back in `Session`, ensure connection type is `SSH`, port 22 is sufficient, then click Open on the bottom right.

In the example we wer not able to connect. About 10 seconds pass and we recieve an error message **Network error COnnection timed out**. There could be this security feature on the masternode that does not allow external connections.

Now, go to the Security group, on the AWS cluster page, under **Security and access**, click the link next to `Security groups for Master`. We will see two different entries. The second one is the master one. WE know this because the security group name and description say Master and not slave. Click on the master's security group ID. Click `Edit Inbound RUles` on the right. Scroll to the bottom and add a new rule. We want to open up port 22, set to My IP which will auto figure it out. Finally, click save rules.

Try PuTTY again with same host name, select private key again, click Open. First time we open this we will recieve a warning in which PuTTY is saying it has not seen this key before, click okay. We should be in now! The terminal should print out ascii text to spell out EMR.

Next in the terminal type in the following command:
```aws s3 cp s3://sundog-spark/MovieSimilarities1M.py ./```
Remember this loads up the python script. The terminal should output:
```download: s3://sun-dog-spark/MovieSimilarities1M.py to ./MovieSimilarities1M.py```
Next up type the following command to translate movie IDs to names:
```aws s3 cp s3://sundog-spark/ml-1m/movies.dat ./```
Termnal output:
```download s3://sundog-spark/ml-lm/movies.dat to ./movies.dat```
We can first check if we have the right script by typing:
```cat MovieSimilarities1M.py```
Output will literally print out the Python file in the command line.
Finally type the last command:
```spark-submit --executor-memory lg MovieSimilarities1M.py 260```
EMR has already configed this cluster so it will use the cluster and not run this locally by default. We do not need to do anything else here.
Note that we did speak about using executor memory as a way to get more performance. However, we should only do this if we really need to. There are cases where we can run out of memory if it gets too high. Safer to let Spark attempt to figure this out first.
The terminal will print out a lot of info messages saying it is getting things started. Goes off, uploads what it has to. Will also tell you when it loads up the movie names from the `movies.dat` file and then it tries to figure out how to schedule everything and distribute all the work across the cluster. This process will take about 20 minutes to finish.
We will see results in next lecture.