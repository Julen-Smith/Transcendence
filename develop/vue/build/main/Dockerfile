FROM node:20.10

WORKDIR /Trascendence
COPY package.json package.json
RUN npm install

RUN apt-get update
RUN apt-get install jq -y



CMD ["/bin/bash", "-c", "npm run serve"]

