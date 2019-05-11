## Metablock Stats

A internal website is integrated as a container inside the docker-compose file which runs Metablock. 
You can see in real time files store in the blockchain (key name), and when they were put in.

#### Software used
* Apache (port 80)
* PHP / MySQL / PHPMyAdmin

PHPMyAdmin can be disabled or uninstall for a deployment but currently it gives a visual access to the database and can be used
to export figures in a exploitable format if you want to manipulate them.

#### Integration

A request is launched in the client container, when a thread is started to store a "metadoc" inside the blockchain., and also
when the thread is finished, it helps to evaluate time required for the transaction.

#### Database
There is only one table which contains four fields:
* id
* key_name
* time_insertion
* type

key_name represents the name of the file (like test.txt), time_insertion is a reference time used to have always the same clock.
It's a request on the Redis server.
Type is used to separate requests did before the transaction and after transaction.

#### Features

The main feature is to see a number of transactions with the key_name, time, and time between this transaction and the one
before.

There is a possibility to sort transactions by type (Start/Finish), and to show only 10,20,50 or 100 last transactions.

If you sort by type you have a average of time between all transactions at the bot of the website.

You can also calculate time between two files : the first key_name will be the transaction of "Start" type, and the second 
will be a "Finish" type (it's managed automatically, you just have to write the original key_name).

On the other page "Stats" you can see how many metadata are stored in the Metablock, and in a readability issue, a feature
is available to delete all statistics inside the database (it won't delete metadata in the blockchain). After that, it will
be easier for you to read the last entries table.

#### Issue
One of possible issue is to not be able to reach the statistics container inside the receive_meta_para.py script, in the client container. IP address of the statistics container may change and you must change it in the script file.

#### Screenshots

##### Home
![Home_website_picture](http://nonotools.fr/projets/metablock/home.png)

##### Last entries
![Last_entries_picture](http://nonotools.fr/projets/metablock/last_entries.png)

##### Calculate time
![Calculate_time_picture](http://nonotools.fr/projets/metablock/calculate.png)


##### Stats
![Stats_page_picture](http://nonotools.fr/projets/metablock/statistics.png)
