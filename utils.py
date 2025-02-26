from flask import jsonify

def build_success_response(message, status=200, data=None):
    """Build a standardized success response."""

    response = jsonify({
        'success': True,
        'message': message,
        'status_code': status,
        'data': data or {}
    })

    # Set the status code using the response object
    response.status_code = status
    return response


def build_error_response(message, status=400, data=None):
    """Build a standardized error response."""

    response = jsonify({
        'success': False,
        'error_message': message,
        'status_code': status,
        'data': data or {}
    })

    response.status_code = status
    return response


def is_valid_lat_lng(lat, lng):
    """Validate latitude and longitude."""

    try:
        lat = float(lat)
        lng = float(lng)

        if -90 <= lat <= 90 and -180 <= lng <= 180:
            return True
        
        return False
    
    except ValueError:
        return False