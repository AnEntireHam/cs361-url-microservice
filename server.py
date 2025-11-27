import zmq

context = zmq.Context()
PORT = 6702

def server_loop(socket):
    #  Wait for next request from client
    message = socket.recv()
    message = message.decode()
    print(f"Recieved message: {message}")

    response = message.upper()
    socket.send(response.encode())
    print(f"Sent response: {response}")
    print()

if __name__ == "__main__":
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT}")
    print(f"Timezone conversion microservice running on port {PORT}.\n")

    try:
        while True:
            server_loop(socket)

    except KeyboardInterrupt:
        print("Goodbye!")

    finally:
        socket.close()
