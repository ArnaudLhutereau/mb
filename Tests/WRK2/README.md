# WRK2 Benchmark

You can find result of the utilization of [WRK2](https://github.com/giltene/wrk2) to evaluate the performance of storage time.

### Installation:

WRTK2 in the basic configuration doesn't allow to do PUT requests, you can create in wrtk2/scripts/ a file called put.lua
(file available here, in this folder: metablock/Tests/WRRK2/put.lua)

``` bash
-- HTTP PUT script
wrk.method = "PUT"
wrk.body   = "test_put_request"
wrk.headers["Content-Type"] = "text/html"
```
### Command line and parameters

``` bash
#First test
wrk -t4 -c4 -d30s -R10 -s scripts/put.lua http://127.0.0.1:3000/

#Second test
wrk -t4 -c4 -d90s -R10 -s scripts/put.lua http://127.0.0.1:3000/

#Third test
wrk -t4 -c4 -d90s -R10 -s scripts/put.lua http://127.0.0.1:3000/
```

Several parameters were tested:
* 4 threads, 4 connections, 30 seconds running and a maximum of 10 requests per second.
* 4 threads, 4 connections, 90 seconds running and a maximum of 10 requests per second.
* 4 threads, 4 connections, 90 seconds running and a maximum of 10 requests per second.


### Output:

#### First test
```
Running 30s test @ http://127.0.0.1:3000/
  4 threads and 4 connections
  Thread calibration: mean lat.: 3615.312ms, rate sampling interval: 11468ms
  Thread calibration: mean lat.: 4485.193ms, rate sampling interval: 12271ms
  Thread calibration: mean lat.: 4196.571ms, rate sampling interval: 11632ms
  Thread calibration: mean lat.: 4781.568ms, rate sampling interval: 12845ms
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    13.84s     3.81s   20.35s    59.15%
    Req/Sec     0.00      0.00     0.00    100.00%
  100 requests in 30.01s, 11.23KB read
  Socket errors: connect 0, read 0, write 0, timeout 1
Requests/sec:      3.33
Transfer/sec:     383.17B
```

Metablock Stats shows a average around 0.2866 second per file.

#### Second test
```
Running 2m test @ http://127.0.0.1:3000/
  4 threads and 4 connections
  Thread calibration: mean lat.: 3161.898ms, rate sampling interval: 10289ms
  Thread calibration: mean lat.: 3642.112ms, rate sampling interval: 10600ms
  Thread calibration: mean lat.: 3919.488ms, rate sampling interval: 11083ms
  Thread calibration: mean lat.: 3730.212ms, rate sampling interval: 10354ms
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    32.45s    14.99s    0.97m    56.64%
    Req/Sec     0.00      0.00     0.00    100.00%
  318 requests in 1.50m, 35.71KB read
  Socket errors: connect 0, read 0, write 0, timeout 1
Requests/sec:      3.53
Transfer/sec:     406.24B
```

Metablock Stats shows a average around 0.2809 second per file.

#### Third test

This test runs without connection to the blockchain, only Recast runs.
```
Running 2m test @ http://127.0.0.1:3000/
  4 threads and 4 connections
  Thread calibration: mean lat.: 3827.968ms, rate sampling interval: 11771ms
  Thread calibration: mean lat.: 3882.183ms, rate sampling interval: 12296ms
  Thread calibration: mean lat.: 4105.408ms, rate sampling interval: 12230ms
  Thread calibration: mean lat.: 3826.560ms, rate sampling interval: 11771ms
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    32.21s    14.81s    0.96m    58.50%
    Req/Sec     0.08      0.28     1.00    100.00%
  327 requests in 1.50m, 36.72KB read
  Socket errors: connect 0, read 0, write 0, timeout 1
Requests/sec:      3.63
Transfer/sec:     417.69B
```
Time average (3.63 file per second) is almost identical that the test with blockchain

### Results

There is a average around 3 file per second, with a limitation due to Recast performance.
