FROM node:latest

WORKDIR /app

ENV HOSTED_URL "https://lover-on-localhost.ctf.maplebacon.org"

RUN apt-get update && apt-get install -y chromium
ENV CHROMIUM_PATH "/usr/bin/chromium"

COPY package*.json /app/

RUN npm install

COPY . /app/

ENV PORT 1337
ENV FLAG "maple{a_dQw4w9WgXcQ_for_you}"

CMD [ "npm", "start" ]
