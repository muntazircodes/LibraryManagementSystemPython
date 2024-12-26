from flask import jsonify


class Responses:
    
    @staticmethod
    def success(message, data=None, status_code=200):
        response = {
            "status": "success",
            "message": message,
            "data": data
        }
        return jsonify(response), status_code

    @staticmethod
    def created(resource, data=None):
        response = {
            "status": "success",
            "message": f"{resource} created successfully",
            "data": data
        }
        return jsonify(response), 201

    @staticmethod
    def updated(resource, data=None):
        response = {
            "status": "success",
            "message": f"{resource} updated successfully",
            "data": data
        }
        return jsonify(response), 200

    @staticmethod
    def deleted(resource):
        response = {
            "status": "success",
            "message": f"{resource} deleted successfully"
        }
        return jsonify(response), 200


    @staticmethod
    def bad_request(errors=None):
        response = {
            "status": "fail",
            "message": "Bad request",
            "errors": errors
        }
        return jsonify(response), 400

    @staticmethod
    def error(message, errors=None, status_code=400):
        response = {
            "status": "error",
            "message": message,
            "errors": errors
        }
        return jsonify(response), status_code

    @staticmethod
    def missing_fields(fields):
        response = {
            "status": "fail",
            "message": "Missing required fields",
            "fields": fields
        }
        return jsonify(response), 400

    @staticmethod
    def unauthorized():
        response = {
            "status": "error",
            "message": "Unauthorized access"
        }
        return jsonify(response), 401

    @staticmethod
    def forbidden():
        response = {
            "status": "error",
            "message": "Forbidden action"
        }
        return jsonify(response), 403

    @staticmethod
    def not_found(resource):
        response = {
            "status": "error",
            "message": f"{resource} not found"
        }
        return jsonify(response), 404

    @staticmethod
    def conflict(message):
        response = {
            "status": "error",
            "message": message
        }
        return jsonify(response), 409

    @staticmethod
    def validation_error(errors):
        response = {
            "status": "fail",
            "message": "Bad request",
            "errors": errors
        }
        return jsonify(response), 400

    @staticmethod
    def rate_limit_exceeded():
        response = {
            "status": "error",
            "message": "Rate limit exceeded. Please try again later."
        }
        return jsonify(response), 429  # Too Many Requests

    @staticmethod
    def custom(status, message, data=None, errors=None, status_code=200):
        response = {
            "status": status,
            "message": message,
            "data": data,
            "errors": errors
        }
        return jsonify(response), status_code
    

    @staticmethod
    def missing_fields(fields):
        response = {
            "status": "fail",
            "message": "Missing required fields",
            "fields": fields
        }
        return jsonify(response), 400
