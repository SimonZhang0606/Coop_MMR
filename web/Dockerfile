# pull official base image
FROM node:16-alpine3.13

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# add app

# mount /app/public for hot refreshes when developing locally
COPY public /app/public
VOLUME /app/public

# mount /app/src for hot refreshes when developing locally
COPY src src
VOLUME /app/src

# start app
CMD ["npm", "start"]
