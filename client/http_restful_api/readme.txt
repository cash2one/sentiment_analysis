This is a RESTful service for the apis that thrift server provides
remember to change the gen-py folder if the thrift file is changed.

1. how to start:
python manage.py runserver 0.0.0.0:8080(port to host the http service)

TEST:
http://192.168.24.45:8080/api/9001/WeiboService/want2Buy/?arg=testChineseStr
