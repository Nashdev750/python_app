const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const cors = require('cors')

const io = new Server(server,{
    cors:{
        origin:'*',
    },
    path:'/io/'
});


app.use(cors())

const PORT = process.env.PORT || 8000


// app.get('/',(req,res)=>{
//     res.status(404).send();
// })


io.on('connection',(socket)=>{
    console.log(socket.id)
    socket.emit('me',socket.id)
    socket.on('progress',(data)=>{
        console.log(data)
        socket.broadcast.emit("data",data)
    })
})

server.listen(PORT,()=>{
    console.log('app running on port on:', PORT)
})

// client_max_body_size 500m;
// root /var/www/python_app/build;
// index index.html index.htm index.nginx-debian.html;
// server_name openmca.com www.openmca.com;
// location / {
//         try_files $uri $uri/ =404;

// }

// location /api {
//         proxy_pass http://127.0.0.1:8000;
//         proxy_set_header Host $host;
//         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
//         proxy_set_header X-Real-IP $remote_addr;

// }
// location /io {
//         proxy_pass http://127.0.0.1:4000;
//         proxy_set_header Host $host;
//         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
//         proxy_set_header X-Real-IP $remote_addr;
// }