import json
from http.server import HTTPServer
from monty_handler import HandleRequests, status

from views import update_category, edit_tag


class JSONServer(HandleRequests):
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


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
