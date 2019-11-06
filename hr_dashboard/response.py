import traceback

from rest_framework.views import exception_handler
from rest_framework.response import Response

headers = {"Access-Control-Allow-Origin": "True"}


def hr_exception_handler(exc, context):
    response = exception_handler(exc, context)

    try:
        data = response.data
        message = ""
        for key, value in data.items():
            message += "%s: %s. " % (key, value)
    except:
        message = ""

    if response is not None:
        response.data = {
            'success': False,
            'error': message,
            'message': message,
            'data': {}
        }
    return response


def api_response(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            if res['success']:
                return Response({
                    'data': res.get('data', {}),
                    'success': True,
                    'message': res.get('message', 'success'),
                    'error': res.get('error', ''),
                    'statusCode': res.get('statusCode', 200)
                }, status=res.get('status', 200), headers=headers)
            else:
                return Response({
                    'data': res.get('data', {}),
                    'success': False,
                    'message': res.get('message', ''),
                    'error': res.get('error', ''),
                    'statusCode': res.get('statusCode', 400)
                }, status=res.get('status', 400), headers=headers)
        except Exception as e:
            return Response({
                'data': {},
                'success': False,
                'error': "Something wrong. Please try again after sometime.\nDev Hint(hidden in production): %s" % str(e),
                'exception': str(e),
                'traceback': traceback.format_exc(),
                'statusCode': 500
            }, status=500, headers=headers)
    return wrapper
