FROM node:latest

ENV HOSTED_URL "http://callback-2.ctf.maplebacon.org"

RUN apt-get update && apt-get install -y chromium 
ENV CHROME_BIN /usr/bin/chromium

COPY . /app
WORKDIR /app/
RUN npm install

ENV PORT 1337
ENV FLAG "maple{d4ng_d4ngl3r_d4ngl1ng_d4ngl3d_h7ml}"

CMD [ "npm", "start" ]

