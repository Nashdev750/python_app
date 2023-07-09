import subprocess
def send_message(message):
    command = ['node', '../io/message.js', message]
    process = subprocess.Popen(command)
    process.wait() 
 