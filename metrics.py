from prometheus_client import Counter, Histogram

request_counter = Counter('request_count', 'counts the amount of times a method was called', labelnames=['method'])

request_latency_histogram = Histogram('request_latency_seconds', 'the amount of time it takes a method to respond',
                                      labelnames=['method'], buckets=(.001, .005, .01, .05, .1, 1.0, 10.0))
