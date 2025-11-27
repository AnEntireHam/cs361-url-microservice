import zmq

PORT = 6702
context = zmq.Context()

if __name__ == "__main__":
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{PORT}")
    print(f"Timezone client running on port {PORT}.\n")

    message = "Hello there!"
    print(f"Sending message: {message}")
    socket.send(message.encode())
    response = socket.recv().decode()
    print(f"Received response: {response}\n")

    message = "fine weather we're having today"
    print(f"Sending message: {message}")
    socket.send(message.encode())
    response = socket.recv().decode()
    print(f"Received response: {response}\n")

    message = "et cetera"
    print(f"Sending message: {message}")
    socket.send(message.encode())
    response = socket.recv().decode()
    print(f"Received response: {response}\n")
