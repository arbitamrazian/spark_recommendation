# spark_recommendation
Motivation: To use ALS algorithm on spark to provide movie recommendations (http://dl.acm.org/citation.cfm?id=1608614).
Disclaimer:  This is meant to be an educational introduction to using spark in a recommendation system.  This procedure is not meant to be used in production.  620MB (the size of the database we use) will fit in memory on modern laptops.  Using a distributed system will slow down training drastically when compared with a standalone solution.

## Data
We will use the MovieLens database that contains 22M ratings on 33,000 movies by 240,000 users.  You can download the data from: http://grouplens.org/datasets/movielens/

## Setup
We will deploy our spark cluster on an Amazon EC2 cluster using the spark-ec2 (https://github.com/amplab/spark-ec2) tool.
Please follow these steps to setup spark on your ec2 account:

1. Create a new user inside the amazon control panel (IAM) and download the keypair. 
2. Attach a policy (AmazonEC2FullAccess) that will allow spark-ec2 to make changes (add instances) to your account.
3. Create an Access Key inside the Security Credentials tab and download the content
4. Export access key and access secret as environmental variables.  (Ex.  `export AWS_SECRET_ACCESS_KEY=AaBbCcDdEeFGgHhIiJjKkLlMmNnOoPpQqRrSsTtU; export AWS_ACCESS_KEY_ID=ABCDEFG1234567890123` )
5. Run the following command `./spark-ec2 --key-pair=myuserkeypair --identity-file=myuserkeypair.pem --region=us-east-1 --zone=us-east-1c -s 2 launch mysparkcluster`.  This command will launch 1 spark master along with 2 spark slaves.  It will also run spark UI (http://ec2-XXX-XXX-XXX-XXX.compute-1.amazonaws.com:8080/) and ganglia (http://ec2-XXX-XXX-XXX-XXX.compute-1.amazonaws.com:5080/ganglia/) on your spark master.
6. To login to your spark master run `./spark-ec2 --key-pair=myuserkeypair --identity-file=myuserkeypair.pem --region=us-east-1 --zone=us-east-1c login mysparkcluster`

After you have setup spark you can now download the MovieLens database by running `wget http://files.grouplens.org/datasets/movielens/ml-latest.zip`.  After you unzip the file you should see the ratings.csv file.  We will now insert this file into HDFS using the following steps.

1. Make a new directory that will house the data. `~/ephemeral-hdfs/bin/hadoop fs -mkdir /user/hadoop`
2. Make sure that directory was created by running `~/ephemeral-hdfs/bin/hadoop fs -ls /user/hadoop`
3. Put your file inside the directory by `~/ephemeral-hdfs/bin/hadoop fs -put ratings.csv /user/hadoop`
4. Repeat #3 for the other files inside the data directory
