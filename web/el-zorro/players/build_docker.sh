docker build -t web_zorro . 
docker run -p 9080:9080 --rm --name=web_zorro -it web_zorro
