# Metablock rebuilding Benchmark

You can find result of the utilization of a simulation of requests to evaluate the performance of rebuilding metadata which
are lost in the Redis database.

### How to do this test:

There is 3 part to execute this test :
* You have to add X files (100 for example) in Recast. You can use GRBT to do it.
* To start the rebuild system, Recast musn't find all metadata in Redis. So you have to erase at least one entry for each
file in Redis database. A script is available in the client_rebuild container, called "delete_entries.py". Please be sure that
name of your PUT request matches with name in the delete script.
* To start the test, you can launch the script in this folder, called "test_get.py". Check the code to configure file number
 and file name.

### Parameters

* Simulation of 100 files
* Simulation of 300 files
* Simulation of 500 files

### Output:

#### First test
```
Simulation of 100 files (Result come from Metablock Stats)
Average time between two file storage : 3.5404450893402 seconds       
```

#### Second test
```
Simulation of 300 files (Result come from Metablock Stats)
Average time between two file storage : 10.956773996353 seconds
```

#### Third test
```
Simulation of 500 files (Result come from Metablock Stats)
Average time between two file storage : 19.15664601326 seconds
```

Detailed results for test 1 and test 3 are available, in this folder, in .sql and .json to reuse it for diagram or other things.

### Results

This benchmark shows us that our reconstruction script is independent of file number and time is linear.

