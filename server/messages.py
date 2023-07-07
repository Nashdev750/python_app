import socketio

# Create a Socket.IO client instance
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

def send_message(message):
    sio.emit('progress', {"message":message})

sio.connect('http://localhost:8000')

# sio.wait()
