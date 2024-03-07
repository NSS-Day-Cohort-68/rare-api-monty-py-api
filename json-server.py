import json
from http.server import HTTPServer
from monty_handler import HandleRequests, status

from views import (
    update_category,
    edit_tag,
    create_tag,
    create_category,
    create_post_tag,
    create_user,
)


class JSONServer(HandleRequests):
    """
    Represents a server that handles JSON requests and responses.

    This class extends the functionality provided by the HandleRequests class
    to support JSON data transmission. It implements methods for handling JSON
    requests and generating JSON responses.

    """

    def do_PUT(self):
        url = self.parse_url(self.path)
        pk = url["pk"]

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "posts":
            if pk != 0:
                successfully_updated = edit_post(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "Success, post updated! :)",
                        status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value,
                    )
                return self.response(
                    "Bad request data. Check yo self!",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

        if url["requested_resource"] == "categories":
            if pk != 0:
                successfully_updated = update_category(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "Success, post updated! :)",
                        status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value,
                    )
                return self.response(
                    "Bad request data. Check yo self!",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

        if url["requested_resource"] == "tags":
            if pk != 0:
                successfully_updated = edit_tag(request_body, pk)
                if successfully_updated:
                    return self.response(
                        "Success, post updated! :)",
                        status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value,
                    )

                return self.response(
                    "Bad request data. Check yo self!",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
        else:
            return self.response(
                "Requested resource not found. Check yo self!",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

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
