import logging
import time
import json

# Configura el logger
logger = logging.getLogger("request_response")


def obfuscate_sensitive_data(data: bytes | dict) -> str:
    """Obfuscate sensitive data from the request/response.

    Args:
        data (str | dict): Data to obfuscate (body of request/response).

    Raises:
        Exception: Data must be a bytes or dict.

    Returns:
        str: Obfuscated data with **** or ABC123.
    """
    if isinstance(data, str):
        data = json.loads(data)
    elif isinstance(data, dict):
        pass
    else:
        raise Exception(f"Data must be a bytes or dict, not '{type(data)}'.")

    for field in ("password", "refresh", "access"):
        if field in data:
            data[field] = "****"

    return json.dumps(data)


class LogRequestResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __log_request(self, request, path):
        logger.info(f"Request:\t\t{request.method}\t{path}")
        if request.body:
            body = request.body.decode("utf-8")
            if "/api/token/" in path:
                body = obfuscate_sensitive_data(body)

            logger.debug(f"Request body:\t{body}")

    def __log_response(self, response, path, duration):
        logger.info(f"Response:\t\t{response.status_code}\t{path} | {duration:.2f}s")
        if hasattr(response, "data"):
            body = response.data
            if "/api/token/" in path:
                body = obfuscate_sensitive_data(body)
                print(body)
            logger.debug(f"Response body:\t{body}")

    def __call__(self, request):
        start_time = time.time()
        path = request.get_full_path()

        # Log of the request
        self.__log_request(request, path)

        # Get the response
        response = self.get_response(request)
        duration = time.time() - start_time

        # Log of the response
        self.__log_response(response, path, duration)

        return response
