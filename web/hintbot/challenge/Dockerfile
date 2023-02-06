FROM node:latest

WORKDIR /app/

ENV HOSTED_URL "http://hintbot.ctf.maplebacon.org"

COPY package*.json /app/

RUN npm install

# copy the rest of the files
COPY . /app/

ENV PORT 1337
ENV FLAG "maple{i_got_robert_on_my_team}"

CMD [ "npm", "start" ]

