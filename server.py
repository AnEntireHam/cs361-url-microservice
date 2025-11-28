import zmq
import re
import webbrowser

# Looks for "http://" or "https://", then any amount of subdomains (containing alphanumeric and hyphens only,
#   separated by "."s, ), followed by a top-level domain (again, alphanumerics and hyphens),
#   and finally an optional section containing a "/" and then any sequence of non-whitespace characters
# Is NOT guaranteed to produce a valid URL, only a valid protocol and host section.
PATTERN_HOSTNAME = re.compile(
    r"^https?:\/\/(?:[A-z0-9-]+\.)+[A-z0-9-]+(?:\/[^\s]*)?$")
# Looks for "http://" or "https://", then the text "localhost", 1-5 digits,
#   and optionally a "/" followed by any sequence of non-whitespace characters
PATTERN_LOCALHOST = re.compile(
    r"^https?:\/\/localhost:[\d]{1,5}(?:\/[^\s]*)?$")

# Extracts 1-5 contiguous digits from a localhost address
PATTERN_EXTRACT_DIGITS = re.compile(r"(\d+){1,5}")

# Searches for "http://" or "https://"
PATTERN_HTTP = re.compile(r"^https?:\/\/")

context = zmq.Context()
PORT = 6702

def is_valid_protocol(input_url):
    match_http = PATTERN_HTTP.match(input_url)
    return (match_http is not None)

def is_valid_hostname(input_url):
    match_host = PATTERN_HOSTNAME.fullmatch(input_url)
    if match_host is not None:
        return True

    match_localhost = PATTERN_LOCALHOST.fullmatch(input_url)
    print(match_localhost)
    if match_localhost is None:
        return False
    digits = int(PATTERN_EXTRACT_DIGITS.findall(input_url)[0])
    # Max port number is 65535
    return (digits > 0 and digits <= 65535)

def open_url(input_url):
    if not is_valid_protocol(input_url):
        return 'Invalid protocol section (Should look like "http://" or "https://")'
    if not is_valid_hostname(input_url):
        return 'Invalid host section (Should look like "https://www.example.com" or "http://localhost:XXXXX")'
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
