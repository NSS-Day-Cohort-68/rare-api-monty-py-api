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
    get_user_posts,
    get_all_posts,
    delete_post,
    delete_post,
    edit_post,
    delete_a_tag,
    delete_category,
    create_post,
    login_user,
    get_post_by_id,
    get_all_categories
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
                        "",
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
                        "",
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
                        "",
                        status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value,
                    )

                else:
                    return self.response(
                        "Bad request data. Check yo self!",
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )
        else:
            return self.response(
                "Requested resource not found. Check yo self!",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

    def do_GET(self):
        url = self.parse_url(self.path)
        response_body = ""

        if url["requested_resource"] == "posts":
            if "user_id" in url["query_params"]:
                response_body = get_user_posts(url["query_params"]["user_id"][0])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            elif "post_id" in url["query_params"]:
                response_body = get_post_by_id(url["query_params"]["post_id"][0])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = get_all_posts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "users":
            if "user_email" in url["query_params"]:
                response_body = login_user(url["query_params"]["user_email"][0])
                if response_body.get("valid") is True:
                    return self.response(
                        json.dumps(response_body), status.HTTP_200_SUCCESS.value
                    )
                else:
                    return self.response(
                        json.dumps(response_body),
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )
        elif url["requested_resource"] == "categories":
            response_body = get_all_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        else:
            return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

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
                response_body = new_user_id
                return self.response(
                    response_body, status.HTTP_201_SUCCESS_CREATED.value
                )
            else:
                return self.response(
                    "Please fill out the required fields",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

        elif requested_resource == "categories":
            category_data = json.loads(request_body)

            new_category = create_category(category_data)

            if new_category:
                return self.response(
                    "", status.HTTP_201_SUCCESS_CREATED.value
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
        elif requested_resource == "posts":
            post_data = json.loads(request_body)

            new_post_id = create_post(post_data)

            if new_post_id:
                response_body = new_post_id
                return self.response(
                    response_body, status.HTTP_201_SUCCESS_CREATED.value
                )
            else:
                return self.response(
                    "Please fill out the required fields",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
        # If true/false... More detailed responses for failing to create user

    def do_DELETE(self):

        url = self.parse_url(self.path)
        requested_resource = url["requested_resource"]
        pk = url["pk"]

        if requested_resource == "tags":
            if pk != 0:
                successfully_deleted = delete_a_tag(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        if requested_resource == "posts":
            if pk != 0:
                successfully_deleted = delete_post(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        if requested_resource == "categories":
            if pk != 0:
                successfully_deleted = delete_category(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
