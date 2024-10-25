import logging
import time
import json

# Configura el logger
logger = logging.getLogger("request_response")


def obfuscate_sensitive_data(data: bytes | dict) -> str:
    """Obfuscate sensitive data from the request/response.

    Args:
        data (bytes | dict): Data to obfuscate (body of request/response).

    Raises:
        Exception: Data must be a bytes or dict.

    Returns:
        str: Obfuscated data with **** or ABC123.
    """
    if isinstance(data, bytes):
        data = json.loads(data.decode("utf-8"))
    elif isinstance(data, dict):
        pass
    else:
        raise Exception(f"Data must be a bytes or dict, not '{type(data)}'.")

    if "username" in data and "password" in data:
        data["password"] = "********"

    if "refresh" in data and "access" in data:
        data["refresh"] = "123.ABC"
        data["access"] = "ABC.123"

    return json.dumps(data)


class LogRequestResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        path = request.get_full_path()

        # Log of the request
        logger.info(f"Request:\t\t{request.method}\t{path}")
        if request.body:
            body = obfuscate_sensitive_data(request.body)
            logger.debug(f"Request body:\t{body}")

        # Get the response
        response = self.get_response(request)
        duration = time.time() - start_time

        # Log of the response
        logger.info(f"Response:\t\t{response.status_code}\t{path} | {duration:.2f}s")
        if hasattr(response, "data"):
            body = obfuscate_sensitive_data(response.data)
            logger.debug(f"Response body:\t{body}")

        return response
