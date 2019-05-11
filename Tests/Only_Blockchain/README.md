# Metablock Benchmark

You can find result of the utilization of a simulation of requests to evaluate the performance of storage time in the
blockchain without the Recast connection.

### Installation:

Use the Python3 script in this folder and run it on the same container that the client (because it's use the connection
to RabbitMQ server at 127.0.0.1 and username/password allow only on localhost).
In the client script (receive_meta_para.py=, Redis request are disabled

### Command line and parameters

``` bash
python3 benchmark_blockain.py
```

Several number of files were tested:
* Simulation of 100 files (100*4 transactions in blockchain)
* Simulation of 300 files (300*4 transactions in blockchain)
* Simulation of 500 files (500*4 transactions in blockchain)

You can change the file number in the script, at line 26.

### Output:

#### First test
```
Simulation of 100 files (Result come from Metablock Stats)
Average time between two file storage : 0.15872398771421 s       
```


#### Second test
```
Simulation of 300 files (Result come from Metablock Stats)
Average time between two file storage : 0.15292071578495 s           
```


#### Third test

```
Simulation of 500 files (Result come from Metablock Stats)
Average time between two file storage : 0.14081963747441 s        
```

### Results

We can see an average of 0.15 second to store one document.

If we compare this result with a simulation integrating Recast, we obtain an average of 0.28 seconds (based on Apache Bench
and WRK2 benchmark).

Performance of Metablock reaches the theoretical limitation of the blockchain due to the genesis configuration file, around
0.138 second per file. 
