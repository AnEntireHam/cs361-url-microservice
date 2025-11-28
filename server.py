import zmq
import re

# Looks for "http" or "https", then any amount of subdomains (containing alphanumeric and hyphens only,
#   separated by "."s, ), followed by a top-level domain (again, alphanumerics and hyphens),
#   and finally an optional section containing a "/" and then any sequence of characters (no whitespaces)
# Is NOT guaranteed to produce a valid URL, only a valid protocol and host section.
PATTERN_HTTPS = re.compile(r"^https?:\/\/(?:[A-z0-9-]+\.)+[A-z0-9-]+(?:\/[^\s]*)?$")

context = zmq.Context()
PORT = 6702

def is_valid_host(input_url):
    match = PATTERN_HTTPS.fullmatch(input_url)
    return (match is not None)

def server_loop(socket):
    #  Wait for next request from client
    message = socket.recv()
    message = message.decode()
    print(f"Recieved message: {message}")

    is_valid = is_valid_host(message)

    response = message + f" {is_valid}"
    socket.send(response.encode())
    print(f"Sent response: {response}")
    print()

if __name__ == "__main__":
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT}")
    print(f"URL opening microservice running on port {PORT}.\n")

    try:
        while True:
            server_loop(socket)

    except KeyboardInterrupt:
        print("Goodbye!")

    finally:
        socket.close()
