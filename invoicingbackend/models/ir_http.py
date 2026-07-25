from odoo import models
from odoo.http import request
from odoo.exceptions import AccessError
from odoo.http import SessionExpiredException
import werkzeug.exceptions
import json
from odoo.http import Response


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _handle_exception(cls, exception):
        # Tangkap jika error terjadi di endpoint /api/
        if request.httprequest.path.startswith("/api/"):
            if request.httprequest.method == "OPTIONS":
                return Response(
                    status=200,
                    headers=[
                        (
                            "Access-Control-Allow-Origin",
                            request.httprequest.headers.get("Origin", "*"),
                        ),
                        ("Access-Control-Allow-Credentials", "true"),
                        (
                            "Access-Control-Allow-Methods",
                            "GET, POST, OPTIONS, PUT, DELETE",
                        ),
                        (
                            "Access-Control-Allow-Headers",
                            "Origin, X-Requested-With, Content-Type, Accept, Authorization",
                        ),
                    ],
                )
            if isinstance(exception, SessionExpiredException):
                return Response(
                    json.dumps(
                        {"error": "Session expired or unauthorized", "code": 401}
                    ),
                    status=401,
                    headers=[
                        (
                            "Access-Control-Allow-Origin",
                            request.httprequest.headers.get("Origin", "*"),
                        ),
                        ("Access-Control-Allow-Credentials", "true"),
                        (
                            "Access-Control-Allow-Methods",
                            "GET, POST, OPTIONS, PUT, DELETE",
                        ),
                        (
                            "Access-Control-Allow-Headers",
                            "Origin, X-Requested-With, Content-Type, Accept, Authorization",
                        ),
                    ],
                    content_type="application/json",
                )
            if isinstance(exception, AccessError):
                return Response(
                    json.dumps({"error": "Access Denied", "code": 403}),
                    status=403,
                    headers=[
                        (
                            "Access-Control-Allow-Origin",
                            request.httprequest.headers.get("Origin", "*"),
                        ),
                        ("Access-Control-Allow-Credentials", "true"),
                        (
                            "Access-Control-Allow-Methods",
                            "GET, POST, OPTIONS, PUT, DELETE",
                        ),
                        (
                            "Access-Control-Allow-Headers",
                            "Origin, X-Requested-With, Content-Type, Accept, Authorization",
                        ),
                    ],
                    content_type="application/json",
                )
        # Jika bukan /api/, biarkan Odoo menangani seperti biasa
        return super(IrHttp, cls)._handle_exception(exception)
