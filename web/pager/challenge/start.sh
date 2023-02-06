docker build -t pager .
docker run -it --rm -p 9999:1337 --name pager pager:latest