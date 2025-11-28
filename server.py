from urllib.error import URLError
import zmq
import re
import urllib.request
import webbrowser

# Looks for "http://" or "https://", then any amount of subdomains (containing alphanumeric and hyphens only,
#   separated by "."s, ), followed by a top-level domain (again, alphanumerics and hyphens),
#   and finally an optional section containing a "/" and then any sequence of characters (no whitespaces)
# Is NOT guaranteed to produce a valid URL, only a valid protocol and host section.
PATTERN_HOSTNAME = re.compile(
    r"^https?:\/\/(?:[A-z0-9-]+\.)+[A-z0-9-]+(?:\/[^\s]*)?$")

# Searches for "http://" or "https://"
PATTERN_PROTOCOL = re.compile(r"^https?:\/\/")

context = zmq.Context()
PORT = 6702

def is_valid_protocol(input_url):
    match = PATTERN_PROTOCOL.match(input_url)
    return (match is not None)

def is_valid_hostname(input_url):
    match = PATTERN_HOSTNAME.fullmatch(input_url)
    return (match is not None)

def open_url(input_url):
    if not is_valid_protocol(input_url):
        return 'Invalid protocol section (Should look like "http://" or "https://")'
    if not is_valid_hostname(input_url):
        return 'Invalid host section (Should look like "https://www.example.com")'
    if webbrowser.open_new_tab(input_url):
        return "Opened URL"
    return "Invalid path or query"

def server_loop(socket):
    message = socket.recv()
    message = message.decode()
    print(f"Recieved message: {message}")

    response = open_url(message)

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
