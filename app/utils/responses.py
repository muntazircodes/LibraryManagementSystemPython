from flask import jsonify

class Responses:

    @staticmethod
    def to_serializable(data):
        if hasattr(data, "to_dict"):
            return data.to_dict()
        elif isinstance(data, list):
            return [item.to_dict() if hasattr(item, "to_dict") else item for item in data]
        elif isinstance(data, (dict, str, int, float, bool, type(None))):
            return data
        else:
            return str(data)

    @staticmethod
    def success(message, data=None):
        response = {
            "status": "success",
            "message": message,
            "data": Responses.to_serializable(data)
        }
        return jsonify(response), 200

    @staticmethod
    def bad_request(errors=None):
        response = {
            "status": "fail",
            "message": "Bad request",
            "errors": Responses.to_serializable(errors)
        }
        return jsonify(response), 400

    @staticmethod
    def conflict(message):
        response = {
            "status": "error",
            "message": message
        }
        return jsonify(response), 409

    @staticmethod
    def created(resource, data=None):
        response = {
            "status": "success",
            "message": f"{resource} created successfully",
            "data": Responses.to_serializable(data)
        }
        return jsonify(response), 201

    @staticmethod
    def custom(status, message, data=None, errors=None, status_code=200):
        response = {
            "status": status,
            "message": message,
            "data": Responses.to_serializable(data),
            "errors": Responses.to_serializable(errors)
        }
        return jsonify(response), status_code

    @staticmethod
    def deleted(resource):
        response = {
            "status": "success",
            "message": f"{resource} deleted successfully"
        }
        return jsonify(response), 200

    @staticmethod
    def error(message, errors=None, status_code=400):
        response = {
            "status": "error",
            "message": message,
            "errors": Responses.to_serializable(errors)
        }
        return jsonify(response), status_code

    @staticmethod
    def forbidden():
        response = {
            "status": "error",
            "message": "Forbidden action"
        }
        return jsonify(response), 403

    @staticmethod
    def image_uploaded(data):
        response = {
            "status": "success",
            "message": "Image uploaded successfully",
            "data": Responses.to_serializable(data)
        }
        return jsonify(response), 201

    @staticmethod
    def missing_fields(fields):
        response = {
            "status": "fail",
            "message": "Missing required fields",
            "fields": Responses.to_serializable(fields)
        }
        return jsonify(response), 400

    @staticmethod
    def not_found(resource):
        response = {
            "status": "error",
            "message": f"{resource} not found"
        }
        return jsonify(response), 404

    @staticmethod
    def profile_not_found():
        response = {
            "status": "error",
            "message": "Profile not found"
        }
        return jsonify(response), 404

    @staticmethod
    def rate_limit_exceeded():
        response = {
            "status": "error",
            "message": "Rate limit exceeded. Please try again later."
        }
        return jsonify(response), 429

    @staticmethod
    def server_error():
        response = {
            "status": "error",
            "message": "Internal server error"
        }
        return jsonify(response), 500

    @staticmethod
    def updated(resource, data=None):
        response = {
            "status": "success",
            "message": f"{resource} updated successfully",
            "data": Responses.to_serializable(data)
        }
        return jsonify(response), 200

    @staticmethod
    def unauthorized():
        response = {
            "status": "error",
            "message": "Unauthorized access"
        }
        return jsonify(response), 401

    @staticmethod
    def validation_error(errors):
        response = {
            "status": "fail",
            "message": "Bad request",
            "errors": Responses.to_serializable(errors)
        }
        return jsonify(response), 400

