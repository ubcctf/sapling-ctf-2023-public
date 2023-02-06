docker build -t general_curl . 
docker run -p 9080:9080 --rm --name=general_curl -it general_curl
