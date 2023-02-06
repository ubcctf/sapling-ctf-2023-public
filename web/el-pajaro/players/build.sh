#!/bin/bash
docker build --tag=web_pajaro .
docker run -p 3000:3000 --rm --name=web_pajaro -it web_pajaro