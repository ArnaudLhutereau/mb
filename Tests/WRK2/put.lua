-- HTTP PUT script

wrk.method = "PUT"
wrk.body   = "test_put_request"
wrk.headers["Content-Type"] = "text/html"