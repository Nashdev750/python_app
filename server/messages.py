# import socketio

# # Create a Socket.IO client instance
# sio = socketio.Client()

# @sio.event
# def connect():
#     print("Connected to server")

# @sio.event
# def disconnect():
#     print("Disconnected from server")
import subprocess
def send_message(message):
    command = ['node', '../io/message.js', message]
    subprocess.Popen(command)
    # sio.emit('me', {"message":message})

# # sio.connect('https://www.openmca.com',{"path":"/io/"})
# sio.connect('https://www.openmca.com/io/',namespaces=['/io/'])

# sio.wait()
# sio.conn

send_message('from poor python')