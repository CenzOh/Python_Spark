## Lesson 47, Setting up the AWS account and Elastic Map Reduce account and connecting to cluster like PuTTY

Getting started with Elastic Map Reduce (EMR).
High level steps:
- Create account with Amazon Web Servies (AWS)
- Create EC2 key pair and download the `.pem` file
- (on Windows of course) We require a terminal like `PUTTY`. We need to convert the `.pem` to a `.ppk` private key file

AWS website: https://aws.amazon.com/
Can get a sense of the current pricing by selecting the pricing tab > Products and services > EC2. There should be an area to scroll down that shows pricing. 
Default EMR cluster for Sparc will spin up `m3.xlarge` instance. In the lecture, Frank shows us that for him that it is 4 CPU's, 15 gigabytes a piece of isntances (so these are quite beefy) and costs $0.26 per hour. Doesn't sound like a lot, but adds up quick. Thats a reasonable rate for a computer THAT powerful. Think about this, if we run 10 of these in a cluster then all of a sudden the price is $2.60 an hour! Run ten of these for ten hours, thats $26. MAKE SURE YOU SHUT IT DOWN WHEN DONE.

Sign into console on the top right > login / create new account > AWS console screen. Lots of options like compute, database, networking etc. Is also always available by clicking a cube icon on the Top left.
Under analytics > EMR. Not just mass produced, it is actulaly a managed Hadoop framework so it spins up a Hadoop cluster for us and it incldes Spark as well. EMR is not jsut for map reduce. We can use Yarn component of Hadoop as a cluster manager that Spark runs on top of.

First we need a way to connect to the instances. We need login authentication credentials with a private and public key pair for signing into the EMR cluster.
Under compute > Click EC2 service. THis is the Elastic COmpute Cloud which is the underlying service that EMR uses to actually spin up the differnet computers in the cluster. 
After clicking on it > Network & Security > click Key Pairs > click Create Key Pair. Name it something you will remember like `sparkkey` > click Create. It will download to our downloads folder a `sparkkey.pem` file which contains the public and private key pair. Keep this file safe and back it up somewhere. This is a one time download can not redownload it for security reasons. Can always create a new one if we need it. 
We also need a terminal to login. We can use a program called `PuTTY`. We could install full windows file but the part that we really need is `putty.exe` which is the terminal app itself as well as `puttygen.exe`. 
Next, click on `puttygen.exe` > click Load > change the drop down for the file filter to 'all files' > select `sparkkey.pem` > save as a `.ppk` file that putty can use > use as a private key by leaving 'key passphrase' empty. As long as we have good physical security for the desktop, then we do not have to worry about any of this > click save > save as `sparkkey.ppk`. 
Use ppk file in Putty. Open Putty > click SSH tab > click Auth > under authentication parameters, select the ppk file > go back to Session > enter the Host Name of the master node of our cluster and login automatically without having to sign in with user and pass.
