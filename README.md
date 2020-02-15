# Secret Room
Web application thats provide private end-to-end GPG encrypted chatting for two people.

## Encription
All messages are encrypted on the client side with a uniq key pair generated for every new room.
SECRET ROOM uses the JavaScript implementation of the OpenPGP protocol [OpenPGP.js](https://github.com/openpgpjs/openpgpjs)

## Tech Stack
Vue.js / Flask / Redis

The application is deployed to Heroku directly from the master branch.
