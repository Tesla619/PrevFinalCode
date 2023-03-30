import socketio

sio = socketio.Server()


# wrap with a WSGI application
app = socketio.WSGIApp(sio)

@sio.event
def message(data):
    print('I received a message!')

@sio.on('my message')
def on_message(data):
    print('I received a message!')