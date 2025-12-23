from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': True,
            'message': '',
            'details': {}
        }

        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['message'] = response.data['detail']
            else:
                custom_response_data['details'] = response.data
                if response.data:
                    first_key = list(response.data.keys())[0]
                    first_error = response.data[first_key]
                    if isinstance(first_error, list):
                        custom_response_data['message'] = first_error[0]
                    else:
                        custom_response_data['message'] = str(first_error)
        elif isinstance(response.data, list):
            custom_response_data['message'] = response.data[0] if response.data else 'An error occurred'
        else:
            custom_response_data['message'] = str(response.data)

        response.data = custom_response_data

    return response
