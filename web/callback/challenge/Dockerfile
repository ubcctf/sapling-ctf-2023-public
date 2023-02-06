FROM node:latest

ENV HOSTED_URL "http://callback.ctf.maplebacon.org"

RUN apt-get update && apt-get install -y chromium 
ENV CHROME_BIN /usr/bin/chromium

COPY . /app
WORKDIR /app/
RUN npm install

ENV PORT 1337
ENV FLAG "maple{un54f3_cl13n7_51d3_r357r1c710n5}"

CMD [ "npm", "start" ]

