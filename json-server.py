import json
from http.server import HTTPServer
from monty_handler import HandleRequests, status

from views import create_tag, create_category, create_post_tag, create_user
from views import get_user_posts, get_all_posts


class JSONServer(HandleRequests):
    """
    Represents a server that handles JSON requests and responses.

    This class extends the functionality provided by the HandleRequests class
    to support JSON data transmission. It implements methods for handling JSON
    requests and generating JSON responses.

    """

    def do_GET(self):
        url = self.parse_url(self.path)
        response_body = ""

        if url["requested_resource"] == "posts":
            if "user_id" in url["query_params"]:
                response_body = get_user_posts(url["query_params"]["user_id"][0])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            
            response_body = get_all_posts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
    def do_POST(self):


        """Handle POST requests from a client"""

        url = self.parse_url(self.path)
        requested_resource = url["requested_resource"]
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)

        if requested_resource == "users":
            user_data = json.loads(request_body)

            new_user_id = create_user(user_data)

            if new_user_id:
                response_body = {"id": new_user_id}
                return self.response(
                    json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value
                )
            else:
                return self.response(
                    "Please fill out the required fields",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

        elif requested_resource == "categories":
            category_data = json.loads(request_body)

            new_category_id = create_category(category_data)

            if new_category_id:
                response_body = {"id": new_category_id}
                return self.response(
                    json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value
                )
            else:
                return self.response(
                    "Please fill out the required fields",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
        elif requested_resource == "tags":
            tag_data = json.loads(request_body)

            new_tag_id = create_tag(tag_data)

            if new_tag_id:
                response_body = {"id": new_tag_id}
                return self.response(
                    json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value
                )
            else:
                return self.response(
                    "Please fill out the required fields",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
        elif requested_resource == "postTags":
            post_tag_data = json.loads(request_body)

            new_post_tag_id = create_post_tag(post_tag_data)

            if new_post_tag_id:
                response_body = {"id": new_post_tag_id}
                return self.response(
                    json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value
                )
            else:
                return self.response(
                    "Please fill out the required fields",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )


# If true/false... More detailed responses for failing to create user





        





def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
