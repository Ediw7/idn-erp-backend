import json
from odoo.http import Response

class ApiResponse:
    @staticmethod
    def success(data=None, message="Success", status_code=200):
        response_body = {
            "status": "success",
            "message": message
        }
        if data is not None:
            response_body["data"] = data
            
        return Response(
            json.dumps(response_body),
            status=status_code,
            content_type='application/json'
        )

    @staticmethod
    def error(message="An error occurred", status_code=400):
        return Response(
            json.dumps({
                "status": "error",
                "message": message
            }),
            status=status_code,
            content_type='application/json'
        )
