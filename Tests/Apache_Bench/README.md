# Apache Bench test

You can find result of the utilization of Apache Bench to evaluate the performance of storage time.

### Command line:
``` bash
ab -n 500 -c -10 -u test.txt http://127.0.0.1:3000/
```

### Output:
```
  This is ApacheBench, Version 2.3 <$Revision: 1807734 $>
  Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
  Licensed to The Apache Software Foundation, http://www.apache.org/

  Benchmarking 127.0.0.1 (be patient)
  Completed 100 requests
  Completed 200 requests
  Completed 300 requests
  Completed 400 requests
  Completed 500 requests
  Finished 500 requests


  Server Software:        
  Server Hostname:        127.0.0.1
  Server Port:            3000

  Document Path:          /
  Document Length:        36 bytes

  Concurrency Level:      10
  Time taken for tests:   130.521 seconds
  Complete requests:      500
  Failed requests:        0
  Total transferred:      67000 bytes
  Total body sent:        66000
  HTML transferred:       18000 bytes
  Requests per second:    3.83 [#/sec] (mean)
  Time per request:       2610.421 [ms] (mean)
  Time per request:       261.042 [ms] (mean, across all concurrent requests)
  Transfer rate:          0.50 [Kbytes/sec] received
                          0.49 kb/s sent
                          1.00 kb/s total
  Connection Times (ms)
                min  mean[+/-sd] median   max
  Connect:        0    0   0.2      0       2
  Processing:  1271 2577 321.2   2500    3631
  Waiting:     1271 2577 321.2   2500    3631
  Total:       1272 2577 321.1   2500    3631

  Percentage of the requests served within a certain time (ms)
    50%   2500
    66%   2590
    75%   2679
    80%   2734
    90%   2957
    95%   3454
    98%   3512
    99%   3564
   100%   3631 (longest request)
```

### Results

We can see a limitation around 0.2610 seconds for one file request.

This limitation is the same as the limitation we determined with our homemade test (folder Generator_recast_blockchain_test )
which shows that the blockchain can't store more than 19 files (represents 76 transactions to the blockchain) in each block generated.

