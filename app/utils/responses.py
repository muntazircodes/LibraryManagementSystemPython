class Responses:
    @staticmethod
    def success(message, data=None):
        response = {
            "status": "success",
            "message": message,
            "data": data
        }
        return response

    @staticmethod
    def error(message, errors=None):
        response = {
            "status": "error",
            "message": message,
            "errors": errors
        }
        return response

    @staticmethod
    def validation_error(errors):
        response = {
            "status": "fail",
            "message": "Validation errors occurred",
            "errors": errors
        }
        return response

    @staticmethod
    def not_found(resource):
        response = {
            "status": "error",
            "message": f"{resource} not found"
        }
        return response

    @staticmethod
    def unauthorized():
        response = {
            "status": "error",
            "message": "Unauthorized access"
        }
        return response

    @staticmethod
    def forbidden():
        response = {
            "status": "error",
            "message": "Forbidden action"
        }
        return response

    @staticmethod
    def conflict(message):
        response = {
            "status": "error",
            "message": message
        }
        return response

    @staticmethod
    def server_error():
        response = {
            "status": "error",
            "message": "An internal server error occurred. Please try again later."
        }
        return response

    @staticmethod
    def created(resource, data=None):
        response = {
            "status": "success",
            "message": f"{resource} created successfully",
            "data": data
        }
        return response

    @staticmethod
    def updated(resource, data=None):
        response = {
            "status": "success",
            "message": f"{resource} updated successfully",
            "data": data
        }
        return response

    @staticmethod
    def deleted(resource):
        response = {
            "status": "success",
            "message": f"{resource} deleted successfully"
        }
        return response

    @staticmethod
    def bad_request(errors=None):
        response = {
            "status": "fail",
            "message": "Bad request",
            "errors": errors
        }
        return response

    @staticmethod
    def rate_limit_exceeded():
        response = {
            "status": "error",
            "message": "Rate limit exceeded. Please try again later."
        }
        return response

    @staticmethod
    def custom(status, message, data=None, errors=None):
        response = {
            "status": status,
            "message": message,
            "data": data,
            "errors": errors
        }
        return response
