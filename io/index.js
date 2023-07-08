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