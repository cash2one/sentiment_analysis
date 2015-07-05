How to TEST:

1. start server, 5 process, 9000 port
python server.py 9000 5

2. how to test using a simple client
python client_sample.py localhost 9000 "this is a test string"

3. you can see the logs in logs/sever.log"



How to add apis to server:
1. change algo_bfd.thrift file
2. thrift --gen py algo_bfd.thrift #to gen the py file
3. add model in plugins
4. start the server(use different file directory to test)

Notice: 
Don't use absolute path!
