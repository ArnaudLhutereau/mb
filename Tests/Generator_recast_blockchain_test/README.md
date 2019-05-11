## Generator Recast Blockchain Test

A generator tool for test performances of Recast with an implemented blockchain 


#### What does it do?

GRBT can create automatically a script file and execute it himself to simulate a massive upload of files, and you can configure some parameters to personalized the test, according to your context.

![Menu](http://nonotools.fr/projets/metablock/menu1.png)

#### How to use it?

Clone the git or download just the file, and run it with Python :

```python
python3 test_generation.py
```

#### Parameters

In the configure menu, you can choose your own parameters:

![Parameters](http://nonotools.fr/projets/metablock/menu2.png)

File number will be the number of requests that the script will do. It creates X files in the same directory that the GRBT script: be careful when you choose a big number.

You can choose the sending time between two requests. There are three possible modes: 

* As fast as possible: no delay between each request
* Random time : A random time (1 to 4 seconds) is apply between two requests
* Fixed time: A fixed time decided is apply, which will be the same all the same

#### Generation and execution

GRBT gives the possibility to generate the script for a mono-thread execution, exported in the same directory in a file called script.sh. You can execute it once generated, directly in the tools.

The second possibility is to run it in parallel, with a multi-threading execution. To do it, you have to choose the option “3” in the main menu.

The number of threads used cannot be modified in the application but you can change it in the code, and change the global variable at the top of the script, “number_thread = 8” (line 31).

It will generate X script.sh files, according to your number of threads defined, and will run it automatically after the generation.

#### Current problems

- GRBT does not verify your entries, so be careful when you choose a number, if you write a string, the tool fails.
- Display after the execution of the script crashes the application. If you want to test again, you have to run it again.


## Test

#### Parameters
- 500 requests
- Parallel sending: 8 threads

#### Results

First request started
![First](http://nonotools.fr/projets/metablock/first.png)
Last request finished
![Second](http://nonotools.fr/projets/metablock/last.png)

We get the time needed to store 500 files:

1531813674.957352-1531813526.696937

= 148.260414839

= 148.260414839 / 500

= 0.29652082967 second per file

More you send files (100, 200, 500), more it will be fast for one file until a limit around 0.28 second that we can't exceed with the basic configuration of Recast.

But according to the genesis file which defined the blockchain and smart contract developed here, the theoritical limit is around 0.14 second per file.
