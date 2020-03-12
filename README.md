Usage
=====

### Client
```
$ python client.py http://localhost:8080 -p 10
INFO:__main__:Starting 10 parallel requests to 'http://localhost:8080'
INFO:__main__:HTTP 200 after 0.434459924697876 seconds
INFO:__main__:HTTP 200 after 0.7006819248199463 seconds
INFO:__main__:HTTP 200 after 1.2724850177764893 seconds
...
```

### Server
```
$ python sample.py --port 8000 --bind 0.0.0.0
======== Running on http://0.0.0.0:8000 ========
(Press CTRL+C to quit)
INFO:__main__:delaying request from 127.0.0.1:52968 by 22.23659268095938 seconds.
INFO:__main__:delaying request from 127.0.0.1:52969 by 6.2113996286454745 seconds.
INFO:__main__:delaying request from 127.0.0.1:52971 by 75.05220274780855 seconds.
INFO:__main__:delaying request from 127.0.0.1:52970 by 137.67567535779972 seconds.
```

If you want to set the mean delay and/or maximum delay these can also be set:
```
$ python delay_server.py --mean-delay=5 --max-delay=2
======== Running on http://127.0.0.1:8080 ========
(Press CTRL+C to quit)
INFO:__main__:delaying request from 127.0.0.1:62466 by 2 seconds.
INFO:__main__:delaying request from 127.0.0.1:62468 by 2 seconds.
INFO:__main__:delaying request from 127.0.0.1:62476 by 1.69 seconds.
INFO:__main__:delaying request from 127.0.0.1:62474 by 2 seconds.
```
