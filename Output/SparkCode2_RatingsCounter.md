### Lesson 6 From first activity to run our first Spark program
```
(base) C:\Users\cenzo>cd sparkcourse

(base) C:\Users\cenzo\SparkCourse>dir
 Volume in drive C is OSDISK
 Volume Serial Number is B62F-1342

 Directory of C:\Users\cenzo\SparkCourse

10/25/2022  11:37 AM    <DIR>          .
10/25/2022  11:37 AM    <DIR>          ..
10/20/2022  02:50 PM    <DIR>          ml-100k
10/25/2022  01:48 PM               469 ratings-counter.py
10/20/2022  02:40 PM             1,626 SparkCode1.txt
10/25/2022  01:48 PM             4,117 SparkIntro.txt
               3 File(s)          6,212 bytes
               3 Dir(s)  121,109,966,848 bytes free``
### CHECK IF WE HAVE ML-100K FOLDER AND RATINGS-COUTNER FILE
```
(base) C:\Users\cenzo\SparkCourse>spark-submit ratings-counter.py
1 6110
2 11370
3 27145
4 34174
5 21201
```
### What this tells us, 4 star ratings have the most amount of ratings.
Note that this was PRIOR to me updating directory with folders.