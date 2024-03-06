import json
from http.server import HTTPServer
from monty_handler import HandleRequests, status
from views import get_user_posts, get_all_posts

class JSONServer(HandleRequests):

    def do_GET(self):
        url = self.parse_url(self.path)
        response_body = ""

        if url["requested_resource"] == "posts":
            if "user_id" in url["query_params"]:
                response_body = get_user_posts(url["query_params"]["user_id"][0])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            
            response_body = get_all_posts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        





def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
