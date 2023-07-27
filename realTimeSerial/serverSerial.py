from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import serial
import threading

app = Flask(__name__)
socketio = SocketIO(app)

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

should_read = False

def read_from_serial():
    while True:
        if should_read:
            data = ser.readline().decode('utf-8').strip()
            if data:
                print("Received:", data)
                socketio.emit('serial_data', {'data': data})

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_reading')
def handle_start_reading(data):
    global should_read
    print('Start reading from serial port')
    should_read = True

@socketio.on('stop_reading')
def handle_stop_reading(data):
    global should_read
    print('Stop reading from serial port')
    should_read = False

if __name__ == '__main__':
    threading.Thread(target=read_from_serial).start()
    socketio.run(app, host='0.0.0.0')