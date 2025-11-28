import zmq

PORT = 6702
context = zmq.Context()

def send_message(message):
    print(f"Sending message: {message}")
    socket.send(message.encode())
    response = socket.recv().decode()
    print(f"Received response: {response}\n")

if __name__ == "__main__":
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{PORT}")
    print(f"Timezone client running on port {PORT}.\n")

    message = "Hello there!"
    send_message(message)

    message = "fine weather we're having today"
    send_message(message)

    message = "et cetera"
    send_message(message)

    message = "http://www.example.com"
    send_message(message)

    message = "https://en.wikipedia.org"
    send_message(message)

    message = "h ttp://en.wikipedia.org"
    send_message(message)

    message = "https://en.wikipedia.org/wiki/Blood_sausage#Asia"
    send_message(message)

    message = "http://localhost:"
    send_message(message)

    message = "http://localhost:/api"
    send_message(message)

    message = "http://localhost:5172"
    send_message(message)

    message = "https://localhost:5172/api"
    send_message(message)

    message = "https://localhost:0"
    send_message(message)

    message = "https://localhost:65535"
    send_message(message)

    message = "https://localhost:65536"
    send_message(message)
