
const io = require('socket.io-client');
const socket = io('https://www.openmca.com',{path:'/io/'});


const message = process.argv[2];

socket.emit('progress',{message})
socket.disconnect();

