from flask import request, jsonify
from pydantic import ValidationError


def validate_request(request_model, allow_empty_body=False):
    """Decorator to validate JSON requests using Pydantic models."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if allow_empty_body and request.content_length == 0:
                return func(None, *args, **kwargs)
            try:
                data = request.get_json()
                if data is None:
                    return jsonify({"error": "No JSON data provided"}), 400
                validated_data = request_model(**data)
                return func(validated_data, *args, **kwargs)
            except ValidationError as e:
                return jsonify({"errors": e.errors()}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


def validate_params(request_model):
    """Decorator to validate URL parameters and query parameters using Pydantic models."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                # Combine URL params (kwargs) with query parameters
                data = dict(kwargs)
                data.update(request.args.to_dict())
                validated_data = request_model(**data)
                return func(validated_data, *args, **kwargs)
            except ValidationError as e:
                return jsonify({"errors": e.errors()}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator