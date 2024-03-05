import json
from http.server import HTTPServer
from monty_handler import HandleRequests, status

# class JSONServer(HandleRequests):


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
