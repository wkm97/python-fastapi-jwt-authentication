class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

class CustomExpiredTokenException(Exception):
    def __init__(self, requestId: str = None, token_type: str = "Token"):
        self.requestId = requestId
        self.token_type = token_type

class CustomInvalidTokenException(Exception):
    def __init__(self, requestId: str = None, token_type: str = "Token"):
        self.requestId = requestId
        self.token_type = token_type

class CustomInvalidClientIdException(Exception):
    def __init__(self, requestId: str = None, client_id: str = "GlobeOSS"):
        self.requestId = requestId
        self.client_id = client_id

class CustomInvalidBasicAuthException(Exception):
    def __init__(self, requestId: str = None):
        self.requestId = requestId

# class CustomException(Exception):
#     def __init__(self, requestId: str, status, str, isValid: bool)

# {
# "requestId": "<uuid>",
# "status: "ok/error",
# "result": {
# "isValid": true
# },
# "errors": [{
# "code": "",
# "message: ""
# }]
# }