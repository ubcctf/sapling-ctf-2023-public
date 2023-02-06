docker build -t beehive .
docker run -it --rm -p 8888:1337 --name beehive beehive:latest
